### FILE: Dockerfile
# Use Python 3.9 slim image as a base
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND="Agg"

# Add metadata labels
LABEL maintainer="Your Name <youremail@example.com>"
LABEL version="0.1.0"
LABEL description="Landlab Overland Flow Simulation"

# Set working directory
WORKDIR /app

# Copy only pyproject.toml first to leverage Docker cache for dependencies
COPY pyproject.toml .

# Install dependencies using pip and pyproject.toml
# --no-cache-dir reduces image size
# -e . installs the project in editable mode, which also installs dependencies from pyproject.toml
RUN pip install --no-cache-dir -e .

# Copy the rest of the application code
COPY . .

# Create a non-root user and switch to it for security
RUN useradd -m appuser
USER appuser

# Command to run the simulation script
# The script will save plots to "output_plots" directory inside /app
CMD ["python", "overland_flow_simulation.py"]