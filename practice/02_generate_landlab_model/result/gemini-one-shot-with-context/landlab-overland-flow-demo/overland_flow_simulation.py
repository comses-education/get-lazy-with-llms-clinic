import numpy as np
import matplotlib.pyplot as plt
from landlab import RasterModelGrid, imshow_grid
from landlab.components import OverlandFlow
from landlab.grid.nodestatus import NodeStatus

# --- 1. Grid Setup and Topography ---
# Create a 20x30 raster grid with 10m spacing
nrows = 20
ncols = 30
dx = 10.0  # m
mg = RasterModelGrid((nrows, ncols), xy_spacing=dx)

# Create a simple sloped topography (sloping towards x=0, node 0)
# Elevation decreases from right to left
z = mg.add_zeros("topographic__elevation", at="node")
z[:] = (mg.x_of_node / (ncols * dx)) * 10  # Max 10m elevation at right edge
z[:] = 10.0 - z[:] # Slope towards x=0

# Set boundary conditions
# Outlet at the left edge, center row (or simply node 0 if it's a corner)
# For simplicity, let's make the entire left edge an outlet (fixed value)
# and other edges closed.
mg.status_at_node[mg.nodes_at_left_edge] = NodeStatus.FIXED_VALUE
mg.status_at_node[mg.nodes_at_right_edge] = NodeStatus.CLOSED
mg.status_at_node[mg.nodes_at_top_edge] = NodeStatus.CLOSED
mg.status_at_node[mg.nodes_at_bottom_edge] = NodeStatus.CLOSED

# Ensure outlet nodes have the lowest elevation along their edge, or are at least reasonable
# For a simple ramp, this should be fine. If outlet is just one node:
# outlet_node_id = 0 # For example, if bottom-left is outlet
# mg.status_at_node[outlet_node_id] = NodeStatus.FIXED_VALUE
# z[outlet_node_id] = 0.0 # Ensure outlet is lowest

# --- 2. Initialize Water Depth Field ---
# Add the surface_water__depth field and initialize with a very small value
# This helps with numerical stability.
h = mg.add_zeros("surface_water__depth", at="node")
h[:] = 1.0e-12  # m, a very thin veneer of water

# --- 3. Instantiate OverlandFlow Component ---
# Default mannings_n is 0.01 if not specified. steep_slopes=True is often a good idea.
# alpha (adaptive timestep weight, default 0.7) and theta (de Almeida scheme weight, default 0.8)
# can be tuned, but defaults are often fine for starting.
overland_flow = OverlandFlow(mg, mannings_n=0.01, steep_slopes=True)

# --- 4. Simulation Parameters ---
total_sim_time = 3600.0  # seconds (1 hour)
storm_duration = 1800.0  # seconds (30 minutes of rain)
# Rainfall intensity in m/s (e.g., 20 mm/hr = 20/1000/3600 m/s)
rainfall_intensity_m_per_s = 20.0 / (1000.0 * 3600.0)

# Plotting parameters
plot_interval = 600.0  # seconds (plot every 10 minutes)
next_plot_time = plot_interval

# --- 5. Simulation Loop ---
elapsed_time = 0.0
plt.figure(figsize=(10, 8)) # Create a figure for plotting

plot_count = 1

print("Starting simulation...")
while elapsed_time < total_sim_time:
    # Determine current rainfall rate for the component
    if elapsed_time < storm_duration:
        overland_flow.rainfall_intensity = rainfall_intensity_m_per_s
    else:
        overland_flow.rainfall_intensity = 0.0

    # Calculate adaptive timestep
    # The component itself caps dt if adaptive_dt is True (default)
    # but we might want to cap it further for plotting or to not overshoot total_sim_time
    dt = overland_flow.calc_time_step()

    # Ensure dt doesn't overshoot next_plot_time or total_sim_time
    if elapsed_time + dt > next_plot_time:
        dt = next_plot_time - elapsed_time
    if elapsed_time + dt > total_sim_time:
        dt = total_sim_time - elapsed_time

    # Run the overland flow component for one timestep
    overland_flow.overland_flow(dt=dt)

    # Update elapsed time
    elapsed_time += dt

    # Plotting
    if elapsed_time >= next_plot_time or elapsed_time >= total_sim_time:
        print(f"Time: {elapsed_time:.2f} s / {total_sim_time:.2f} s, Rainfall: {overland_flow.rainfall_intensity > 0}")
        
        plt.subplot(2, 2, plot_count)
        imshow_grid(
            mg,
            "surface_water__depth",
            plot_name=f"Water Depth at {elapsed_time/60.0:.1f} min",
            var_name="Water Depth (m)",
            var_units="m",
            grid_units=("m", "m"),
            cmap="Blues",
            vmin=0, vmax=0.1 # Adjust vmax as needed based on expected depths
        )
        plot_count += 1
        if elapsed_time < total_sim_time: # Avoid setting next_plot_time beyond total_sim_time
             next_plot_time += plot_interval
        if plot_count > 4: # Reset for next figure or stop if too many plots
            plt.tight_layout()
            plt.show()
            if elapsed_time < total_sim_time: # Only make new figure if simulation continues
                plt.figure(figsize=(10, 8))
                plot_count = 1


    # Break if total simulation time is reached
    if elapsed_time >= total_sim_time:
        break

if plot_count > 1 and plot_count <=4: # Ensure the last plot is shown if not a full figure
    plt.tight_layout()
    plt.show()

print("Simulation finished.")

# --- Optional: Plot final topography and hydrograph at outlet ---
# To plot a hydrograph, you would typically:
# 1. Identify an outlet link or node.
# 2. In the loop, get discharge at that link/node using:
#    discharge_at_links = mg.at_link['surface_water__discharge']
#    # or map to nodes:
#    # discharge_at_nodes = overland_flow.discharge_mapper(overland_flow.q, convert_to_volume=True)
# 3. Store time and discharge values in lists.
# 4. Plot after the loop.

# Example of plotting final topography
plt.figure()
imshow_grid(mg, "topographic__elevation", plot_name="Final Topography", cmap="terrain")
plt.show()