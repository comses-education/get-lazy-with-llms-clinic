# Dockerizing the Landlab Overland Flow Simulation

Based on your application's structure, here are the best practices for creating an effective Docker container:

## Choosing the Right Base Image

Use Python's official slim image rather than Alpine for scientific computing:

```dockerfile
FROM python:3.9-slim-buster
```

The slim variant offers a good balance between size and functionality. Avoid Alpine for scientific Python applications as it can make builds up to 50× slower due to compiling dependencies from source instead of using pre-built wheels.

## Optimizing Layer Structure

Minimize the number of layers to reduce image size by combining related commands:

```dockerfile
# Inefficient approach
RUN pip install numpy
RUN pip install matplotlib 
RUN pip install landlab

# Better approach
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .
```

Group similar operations together to reduce image size and build time.

## Managing Dependencies Properly

Use your existing `pyproject.toml` file to manage dependencies:

```dockerfile
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .
COPY . .
```

This approach leverages your existing dependency management while ensuring packages are cached efficiently.

## Handling Matplotlib Visualization

Since your application uses matplotlib for visualization, you'll need to configure it for a headless environment:

```dockerfile
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND="Agg"
```

For interactive visualizations, you'll need to:
1. Set up X11 forwarding with appropriate volumes and environment variables
2. Configure X11 authentication properly

## Complete Dockerfile Example

Here's a complete Dockerfile following best practices:

```dockerfile
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND="Agg"

# Set working directory
WORKDIR /app

# Copy dependency files first (for better caching)
COPY pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Run as non-root user for security
RUN useradd -m appuser
USER appuser

# Command to run the simulation
CMD ["python", "overland_flow_simulation.py"]
```

## Running the Container

Run the container with:

```bash
# For non-interactive mode (saving plots to files)
docker run -v $(pwd)/output:/app/output your-image-name

# For interactive visualization (X11 forwarding on Linux)
docker run --rm -it -v $(pwd):/app \
  --net=host -e DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  your-image-name
```

## Additional Best Practices

1. **Volume mounting**: Mount data and output directories to persist results between runs.

2. **Managing large datasets**: If your simulations involve large datasets, consider using Docker volumes instead of binding mounts for better performance.

3. **Use unprivileged containers**: Run your application as a non-root user for better security.

4. **Include metadata**: Add descriptive labels to your image:
   ```dockerfile
   LABEL maintainer="Your Name"
   LABEL version="1.0"
   LABEL description="Landlab Overland Flow Simulation"
   ```

5. **Optimize for CI/CD**: Consider multi-stage builds if you need to include build tools that aren't needed at runtime.

6. **Save output to files**: Modify your code to save plots to files rather than displaying them interactively for better container compatibility.