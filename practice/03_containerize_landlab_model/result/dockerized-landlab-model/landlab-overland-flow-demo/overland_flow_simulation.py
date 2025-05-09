import numpy as np
import matplotlib.pyplot as plt
from landlab import RasterModelGrid, imshow_grid
from landlab.components import OverlandFlow
from landlab.grid.nodestatus import NodeStatus
import os # Added for path operations and creating directory

# --- 0. Output Directory Setup ---
output_dir = "output_plots" # Define output directory name
# Create the directory if it doesn't exist.
# Docker will map a host volume to this path later.
os.makedirs(output_dir, exist_ok=True)

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
mg.status_at_node[mg.nodes_at_left_edge] = NodeStatus.FIXED_VALUE
mg.status_at_node[mg.nodes_at_right_edge] = NodeStatus.CLOSED
mg.status_at_node[mg.nodes_at_top_edge] = NodeStatus.CLOSED
mg.status_at_node[mg.nodes_at_bottom_edge] = NodeStatus.CLOSED

# --- 2. Initialize Water Depth Field ---
h = mg.add_zeros("surface_water__depth", at="node")
h[:] = 1.0e-12  # m, a very thin veneer of water

# --- 3. Instantiate OverlandFlow Component ---
overland_flow = OverlandFlow(mg, mannings_n=0.01, steep_slopes=True)

# --- 4. Simulation Parameters ---
total_sim_time = 3600.0  # seconds (1 hour)
storm_duration = 1800.0  # seconds (30 minutes of rain)
rainfall_intensity_m_per_s = 20.0 / (1000.0 * 3600.0) # 20 mm/hr

# Plotting parameters
plot_interval = 600.0  # seconds (plot every 10 minutes)
next_plot_time = plot_interval # Initialize next_plot_time

# --- 5. Simulation Loop ---
elapsed_time = 0.0
print("Starting simulation...")
while elapsed_time < total_sim_time:
    # Determine current rainfall rate
    if elapsed_time < storm_duration:
        overland_flow.rainfall_intensity = rainfall_intensity_m_per_s
    else:
        overland_flow.rainfall_intensity = 0.0

    # Calculate adaptive timestep (dt)
    # Start with the component's suggested dt
    dt_component = overland_flow.calc_time_step()
    dt = dt_component

    # Cap dt: first by total_sim_time
    if elapsed_time + dt > total_sim_time:
        dt = total_sim_time - elapsed_time
    
    # Then, cap dt by next_plot_time (if relevant and earlier than total_sim_time cap)
    # This ensures plotting occurs close to the desired next_plot_time.
    if next_plot_time <= total_sim_time and (elapsed_time + dt > next_plot_time):
        dt = next_plot_time - elapsed_time
    
    # Ensure dt is positive. If dt is zero (e.g. already at next_plot_time),
    # overland_flow might do nothing. The loop structure should handle this:
    # plot, advance next_plot_time, then next iteration will get a new dt_component.
    if dt <= 1e-9: # If dt is effectively zero
        if elapsed_time >= total_sim_time: # If at the end, dt=0 is fine, loop will break
            pass
        elif elapsed_time >= next_plot_time: # If at a plot time, dt=0 is fine, plot will occur
            pass
        else: # dt is zero unexpectedly, try to advance with a small step or component's step
              # This case should be rare with the above dt logic.
              # Forcing a minimal dt if not at a target time might be an option if issues arise.
              # For now, assume overland_flow handles dt=0 gracefully (likely by doing nothing).
              pass


    # Run the overland flow component for one timestep
    overland_flow.overland_flow(dt=dt)

    # Update elapsed time
    elapsed_time += dt

    # Plotting
    if elapsed_time >= next_plot_time or elapsed_time >= total_sim_time:
        print(f"Time: {elapsed_time:.2f} s / {total_sim_time:.2f} s, Rainfall: {overland_flow.rainfall_intensity > 0}. Plotting...")
        
        plt.figure(figsize=(8, 6)) # Create a new figure for each plot
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
        plot_filename = f"water_depth_simtime{elapsed_time:.0f}s.png"
        plt.savefig(os.path.join(output_dir, plot_filename))
        plt.close() # Close the figure to free memory
        print(f"Saved plot: {os.path.join(output_dir, plot_filename)}")
        
        if elapsed_time < total_sim_time:
             next_plot_time += plot_interval
        # If elapsed_time == total_sim_time, loop will terminate after this.
        # next_plot_time is not advanced further, which is correct.

    # Break if total simulation time is reached
    if elapsed_time >= total_sim_time:
        break

print("Simulation finished.")

# Plot final topography and save it
plt.figure(figsize=(8,6))
imshow_grid(mg, "topographic__elevation", plot_name="Final Topography", cmap="terrain")
topography_filename = "final_topography.png"
plt.savefig(os.path.join(output_dir, topography_filename))
plt.close()
print(f"Saved final topography to: {os.path.join(output_dir, topography_filename)}")