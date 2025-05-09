Okay, the new build failure is a classic "dependency hell" scenario, amplified by the `--no-binary :all:` flag. This flag forces `pip` to try and build *everything* from source, including the build tools themselves (like `setuptools`, `meson-python`, `ninja`, `hatchling`, `importlib-metadata`). This can lead to circular dependencies or situations where a tool needed to build a package is itself being built from source.

The specific error `LookupError: ... importlib_metadata ... is already being built ...` indicates that `pip` got into a state where it was trying to build `importlib-metadata` as a dependency for one package, while simultaneously trying to build it again as a dependency for another (possibly a build-tool for the first package).

**The primary solution is to be more selective with `--no-binary` and ensure build tools and pip itself are up-to-date.**

Here's a revised `Dockerfile` that aims to fix this:

1.  **Upgrade `pip`, `setuptools`, and `wheel` first:** This ensures you're using recent versions with bug fixes and better dependency resolution. These will be installed from wheels.
2.  **Install necessary OS-level build dependencies:** You already had `build-essential` and `python3-dev`. For `matplotlib` and `scipy` (a likely transitive dependency of `landlab`), you often need more, like `pkg-config`, `libfreetype6-dev`, `libpng-dev` (for Matplotlib) and `gfortran`, `liblapack-dev`, `libblas-dev` (for SciPy).
3.  **Use targeted `--no-binary`:** Instead of `:all:`, specify only the packages that are causing the ABI issue (`numpy`) or benefit from being built against local system libraries (`matplotlib`, `scipy`). `landlab` might also need this if its wheels are problematic with the version of NumPy/SciPy built.

```dockerfile
### FILE: Dockerfile
# Use Python 3.9 slim image as a base
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND="Agg" # For headless matplotlib, plots will be saved to files

# Add metadata labels
LABEL maintainer="Your Name <youremail@example.com>"
LABEL version="0.1.0"
LABEL description="Landlab Overland Flow Simulation"

# --- Install OS build dependencies ---
# build-essential, python3-dev: for C extensions
# pkg-config: helps find other libraries
# libfreetype6-dev, libpng-dev: for matplotlib
# gfortran, liblapack-dev, libblas-dev: for scipy (often a dependency of landlab)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    pkg-config \
    libfreetype6-dev \
    libpng-dev \
    gfortran \
    liblapack-dev \
    libblas-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --- Upgrade pip, setuptools, and wheel ---
# Using up-to-date build tools can resolve many issues.
# These will be installed from wheels by default.
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Copy only pyproject.toml first to leverage Docker cache for dependencies
COPY pyproject.toml .

# Install dependencies using pip and pyproject.toml
# --no-cache-dir reduces image size
# --no-binary <packages>: Force specified packages to be built from source.
#   - numpy: Crucial for resolving the original ABI incompatibility.
#   - scipy: Often linked with numpy and can have similar ABI issues. Landlab depends on it.
#   - matplotlib: Building from source ensures it links correctly against system freetype/png.
# For 'landlab' itself, we'll let pip try its wheel first. If the numpy error
# re-appears specifically for landlab, then add 'landlab' to this --no-binary list.
RUN pip install --no-cache-dir \
    --no-binary numpy,scipy,matplotlib \
    -e .

# Copy the rest of the application code
COPY . .

# Create a non-root user and switch to it for security
RUN useradd -m appuser
USER appuser

# Command to run the simulation script
CMD ["python", "overland_flow_simulation.py"]

**Explanation of Key Changes:**

*   **OS Dependencies:** Added `pkg-config`, `libfreetype6-dev`, `libpng-dev`, `gfortran`, `liblapack-dev`, `libblas-dev`. These are common requirements for building `matplotlib` and `scipy` (which `landlab` depends on) from source.
*   **Upgraded `pip`, `setuptools`, `wheel`:** This happens *before* installing your project dependencies.
*   **Targeted `--no-binary`:** Changed `RUN pip install --no-cache-dir --no-binary :all: -e .` to `RUN pip install --no-cache-dir --no-binary numpy,scipy,matplotlib -e .`.
    *   This tells `pip` to build `numpy`, `scipy`, and `matplotlib` from their source distributions. This is important for `numpy` to fix the original ABI error, and good for `scipy` and `matplotlib` to ensure they link correctly with the system libraries and the specific `numpy` version you're building.
    *   Crucially, other packages (including build tools like `meson-python`, `ninja`, `hatchling`, `importlib-metadata` that `matplotlib` or other dependencies might pull in as *their* build requirements) will now be allowed to install from wheels if available. This should prevent the `LookupError: ... is already being built` problem.
*   **`landlab` Installation:** `landlab` itself is not initially in the `--no-binary` list. We're hoping that once `numpy` and `scipy` are correctly built from source, the `landlab` wheel (if one is used) will be compatible, or if `landlab` is built from source (if no wheel is available or suitable), it will build correctly against the already-compiled `numpy`/`scipy`. If the `numpy.dtype size changed` error reappears and the traceback points to `landlab`, then you would add `landlab` to the `--no-binary` list: `--no-binary numpy,scipy,matplotlib,landlab`.

**To apply this:**

1.  Replace your `Dockerfile` content with the new version above.
2.  Remove the `version: '3.8'` line from your `docker-compose.yml` file as it's obsolete and the warning suggests. It's not critical for the error but good practice.
    Your `docker-compose.yml` would start like:
    ```yaml
    services:
      app:
        build:
          context: .
          dockerfile: Dockerfile
        # ... rest of your docker-compose.yml
    ```
3.  Rebuild the image, preferably without cache to ensure all steps use the new instructions:
    ```bash
    docker compose build --no-cache
    ```
4.  Try running it again:
    ```bash
    make run
    ```
    or
    ```bash
    docker compose up
    ```

This approach should be more robust. The build might take a bit longer because `numpy`, `scipy`, and `matplotlib` are being compiled from source, but it's the most reliable way to handle these types of C-extension and ABI compatibility issues in complex scientific Python stacks.
