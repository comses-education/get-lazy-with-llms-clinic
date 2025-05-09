### FILE: Makefile
# Define default image name and output directory
IMAGE_NAME ?= landlab-overland-flow-demo
OUTPUT_DIR_HOST ?= ./output_plots
OUTPUT_DIR_CONTAINER ?= /app/output_plots

.PHONY: all build run up down shell clean clean-output logs help

all: build run

help:
	@echo "Makefile for Landlab Overland Flow Simulation Docker application"
	@echo ""
	@echo "Usage:"
	@echo "  make build            Build the Docker image."
	@echo "  make run              Run the simulation using docker compose up (shows logs, then exits)."
	@echo "                        Equivalent to 'make up'."
	@echo "  make up               Start the service defined in docker compose.yml."
	@echo "  make down             Stop and remove containers, networks defined in docker compose.yml."
	@echo "  make shell            Open a bash shell inside a new container instance."
	@echo "  make clean-output     Remove the local output_plots directory."
	@echo "  make clean            Stop containers and remove local output_plots directory."
	@echo "  make logs             Follow logs from the running service (if detached)."
	@echo ""
	@echo "Variables:"
	@echo "  IMAGE_NAME          Override Docker image name (default: $(IMAGE_NAME))"
	@echo "  OUTPUT_DIR_HOST     Host directory for plots (default: $(OUTPUT_DIR_HOST))"

# Build the Docker image using docker compose
build:
	@echo "Building Docker image..."
	docker compose build

# Run the simulation using docker compose up
# This will create the output directory on the host if it doesn't exist due to the volume mount.
run: up

up:
	@echo "Running simulation via docker compose up..."
	@echo "Output plots will be saved to $(OUTPUT_DIR_HOST)"
	mkdir -p $(OUTPUT_DIR_HOST) # Ensure host output directory exists
	docker compose up --remove-orphans

# Stop and remove containers, networks, etc.
down:
	@echo "Stopping and removing containers..."
	docker compose down -v

# Open a bash shell in a new container instance
shell:
	@echo "Opening bash shell in a new container instance..."
	docker compose run --rm app bash

# Remove the local output directory
clean-output:
	@echo "Removing local output directory: $(OUTPUT_DIR_HOST)"
	rm -rf $(OUTPUT_DIR_HOST)

# Clean everything: stop containers and remove output
clean: down clean-output

# Follow logs (useful if 'docker compose up -d' was used)
logs:
	@echo "Following logs..."
	docker compose logs -f