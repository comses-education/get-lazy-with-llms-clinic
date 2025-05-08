from landlab import RasterModelGrid
from landlab.components import OverlandFlow
import numpy as np
from landlab.plot import imshow_grid
import matplotlib.pyplot as plt

# Create synthetic grid
grid = RasterModelGrid((50, 50), xy_spacing=30)  # 30m resolution
# Add elevation field with a depression in the center
elev = grid.x_of_node + grid.y_of_node
center = grid.node_y == grid.node_y.mean()
elev[center] -= 10  # Create a small depression along the center row
grid.add_field('topographic__elevation', elev, at='node')

# Set boundary conditions (open north boundary)
grid.set_closed_boundaries_at_grid_edges(True, True, True, True)

# Initialize water depth
grid.add_zeros('surface_water__depth', at='node')

# Create OverlandFlow instance
of = OverlandFlow(grid,
                  steep_slopes=True,
                  mannings_n=0.03,
                  rainfall_intensity=0.0)

# Storm parameters
storm_duration = 10800  # 3 hours in seconds
total_run_time = 14400  # 4 hours total
rainfall_mmhr = 5.0  # rainfall

# Simulation loop
elapsed_time = 0
while elapsed_time < total_run_time:
    of.dt = of.calc_time_step()

    # Apply rainfall during storm period
    if elapsed_time < storm_duration:
        of.rainfall_intensity = rainfall_mmhr * 2.77778e-7  # Convert mm/hr to m/s
    else:
        of.rainfall_intensity = 0.0

    of.overland_flow()
    elapsed_time += of.dt

# Plotting the surface water depth
imshow_grid(grid, 'surface_water__depth', colorbar_label='Water Depth (m)')
plt.show()

if __name__ == "__main__":
    print("Running overland flow simulation...")
    print("Simulation complete. Displaying results.")