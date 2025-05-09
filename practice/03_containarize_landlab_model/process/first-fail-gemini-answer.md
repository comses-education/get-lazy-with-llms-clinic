This is a classic `numpy` binary incompatibility issue. It typically happens when a package with C extensions (like `landlab` or one of its dependencies, often `scipy`) was compiled against one version/build of NumPy's C-API, but at runtime, a different, incompatible version/build of NumPy is being used.

The error message `ValueError: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject` is the key. It means the C code (likely from a Cython extension in `landlab.utils._matrix.pyx`) expects a `numpy.dtype` struct of a certain size (96 bytes), but the NumPy library loaded at runtime has a `numpy.dtype` struct of a different size (88 bytes).

Here's how to fix it, by ensuring that `landlab` and its dependencies are compiled against the NumPy version that will be present in the final image:

**Primary Solution: Modify `Dockerfile` to install build tools and build C extensions from source**

The `python:3.9-slim-buster` image is minimal and doesn't include build tools (like a C compiler) by default. When `pip` installs packages like `landlab` or `scipy`, it often prefers pre-compiled binary "wheels". If these wheels were built against a slightly different NumPy ABI than the one `pip` ultimately installs or resolves for your environment, you get this error.

The solution is to:
1.  Install necessary build tools (`build-essential`, `python3-dev`).
2.  Tell `pip` to not use binary wheels for packages that might cause this issue (or for all packages, to be safe, using `--no-binary :all:`), forcing it to download source distributions and compile them within the Docker build environment. This ensures they are built against the exact NumPy version being installed.

Here's the modified `Dockerfile`:

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

# --- Install build dependencies ---
# These are needed to compile Python C extensions from source,
# which helps resolve NumPy ABI compatibility issues.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only pyproject.toml first to leverage Docker cache for dependencies
COPY pyproject.toml .

# Install dependencies using pip and pyproject.toml
# --no-cache-dir reduces image size
# --no-binary :all: forces compilation from source for packages that have wheels,
# ensuring compatibility with the NumPy version installed in this environment.
# -e . installs the project in editable mode, which also installs dependencies from pyproject.toml
RUN pip install --no-cache-dir --no-binary :all: -e .

# Copy the rest of the application code
COPY . .

# Create a non-root user and switch to it for security
RUN useradd -m appuser
USER appuser

# Command to run the simulation script
# The script will save plots to "output_plots" directory inside /app
CMD ["python", "overland_flow_simulation.py"]
```

**Explanation of Changes:**

1.  **Install Build Tools:**
    ```dockerfile
    RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*
    ```
    *   `apt-get update`: Refreshes the package list.
    *   `apt-get install -y --no-install-recommends build-essential python3-dev`: Installs the C/C++ compiler (`build-essential`) and Python development headers (`python3-dev`) which are necessary for compiling Python C extensions.
    *   `rm -rf /var/lib/apt/lists/*`: Cleans up apt cache to keep the image size smaller.

2.  **Modified `pip install` command:**
    ```dockerfile
    RUN pip install --no-cache-dir --no-binary :all: -e .
    ```
    *   `--no-binary :all:`: This is the crucial part. It tells `pip` to avoid using pre-compiled binary wheels for *all* packages and instead download their source distributions (sdist) and compile them locally within the Docker image. This ensures that any C extensions (like those in `landlab`, `numpy`, `scipy`, etc.) are built against the exact versions of their dependencies (especially NumPy's C-API) present in the Docker image during the build process.

**Steps to Apply the Fix:**

1.  Replace the content of your existing `Dockerfile` with the modified version above.
2.  Rebuild your Docker image. It's good practice to build without cache to ensure all layers are fresh, especially when troubleshooting:
    ```bash
    make clean # if you want to remove old containers/output first
    docker compose build --no-cache
    ```
    or if you don't have `make clean` target doing this:
    ```bash
    docker compose down -v # Stop and remove containers, volumes
    # Optionally remove ./output_plots
    docker compose build --no-cache
    ```
3.  Run the simulation again:
    ```bash
    make run
    ```
    or
    ```bash
    docker compose up
    ```

This should resolve the NumPy binary incompatibility error. The build process might take a bit longer because packages are being compiled from source, but it leads to a more robust environment.

If you still encounter issues, please share the content of your `pyproject.toml` file, as it might contain specific version pins that could interact with this. However, the `--no-binary :all:` approach is generally very effective for this class of problem.