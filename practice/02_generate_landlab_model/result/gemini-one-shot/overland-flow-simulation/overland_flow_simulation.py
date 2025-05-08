import numpy as np
import matplotlib.pyplot as plt

from landlab import RasterModelGrid
from landlab.components import OverlandFlow
from landlab.plot import imshow_grid

# --- 1. Model Grid Parameters ---
nrows = 20  # Number of rows
ncols = 30  # Number of columns
dx = 10.0  # Grid cell spacing [m]

# --- 2. Simulation Time Parameters ---
rainfall_intensity_mmhr = 50.0  # Rainfall intensity [mm/hr]
simulation_duration_hr = 0.5   # Total simulation duration [hours]
output_interval_hr = 0.1       # How often to print status or plot (optional)

# Convert to SI units for calculations
rainfall_intensity_ms = rainfall_intensity_mmhr / (1000.0 * 3600.0)  # [m/s]
simulation_duration_s = simulation_duration_hr * 3600.0             # [s]
output_interval_s = output_interval_hr * 3600.0                     # [s]

# --- 3. OverlandFlow Component Parameters ---
manning_n_value = 0.03  # Manning's roughness coefficient (e.g., for bare soil or short grass)
h_init = 0.001    # Initial water depth [m] (small non-zero value can help stability)
alpha = 0.7       # Runoff component time-step coefficient (0.2-0.7, Courant-Friedrichs-Lewy condition)
                  # Lower alpha means smaller, more stable timesteps.
steep_slopes = True # Use an algorithm for steeper slopes if necessary

# --- 4. Create Grid ---
print("Creating grid...")
mg = RasterModelGrid((nrows, ncols), dx)

# --- 5. Create Topography ---
# Create a simple tilted plane (sloping towards x=0, the left edge)
print("Creating topography...")
z = mg.add_zeros('topographic__elevation', at='node')
z[:] = (ncols - 1 - mg.x_of_node / dx) * 0.1  # Slope factor of 0.1 m per cell column
# You can make this more complex, e.g., z += 0.05 * mg.y_of_node for a compound slope

# Add a small random perturbation to avoid perfectly flat areas if desired
# z += np.random.rand(mg.number_of_nodes) * 0.01

# --- 6. Set Boundary Conditions ---
# Outlet on the left edge (x=0), closed on other three edges
print("Setting boundary conditions...")
mg.set_closed_boundaries_at_grid_edges(right_is_closed=True,
                                       top_is_closed=True,
                                       bottom_is_closed=True,
                                       left_is_closed=False) # Left edge is open (outlet)

# --- 7. Initialize Fields ---
# Water depth field (OverlandFlow will create it if it doesn't exist,
# but initializing helps if you want to specify h_init)
print("Initializing water depth...")
water_depth = mg.add_zeros('surface_water__depth', at='node')
water_depth[:] = h_init

# --- 8. Instantiate OverlandFlow Component ---
print("Instantiating OverlandFlow component...")
overland_flow = OverlandFlow(mg,
                             h_init=h_init,
                             alpha=alpha,
                             mannings_n=manning_n_value, # CORRECTED KEYWORD HERE
                             steep_slopes=steep_slopes)

# --- 9. Plot Initial Topography ---
plt.figure("Initial Topography")
imshow_grid(mg, 'topographic__elevation', cmap='terrain',
            grid_units=('m', 'm'), var_name="Elevation (m)")
plt.title("Initial Topographic Elevation")
plt.show(block=False) # Use block=False for non-blocking plot in some environments

# --- 10. Run Simulation ---
print(f"Starting simulation for {simulation_duration_hr} hours ({simulation_duration_s} s)...")
current_time = 0.0
next_output_time = output_interval_s

model_dt = 10.0  # seconds - OverlandFlow will adjust this internally if needed

while current_time < simulation_duration_s:
    dt_this_iteration = min(model_dt, simulation_duration_s - current_time)
    if dt_this_iteration <= 0:
        break

    mg.at_node['surface_water__depth'][mg.core_nodes] += rainfall_intensity_ms * dt_this_iteration
    overland_flow.run_one_step(dt_this_iteration)
    current_time += dt_this_iteration

    if current_time >= next_output_time or current_time >= simulation_duration_s:
        print(f"Time: {current_time/3600.0:.2f} hours / {simulation_duration_hr:.2f} hours")
        next_output_time += output_interval_s

        # --- Optional: Intermediate Plot ---
        # plt.figure(f"Water Depth at {current_time/3600.0:.2f} hr")
        # imshow_grid(mg, 'surface_water__depth', cmap='Blues', vmin=0,
        #             grid_units=('m', 'm'), var_name="Water Depth (m)")
        # plt.title(f"Water Depth at {current_time/3600.0:.2f} hours")
        # plt.show(block=False)
        # plt.pause(0.1) # Allow plot to update

print("Simulation finished.")

# --- 11. Plot Final Water Depth ---
plt.figure("Final Water Depth")
imshow_grid(mg, 'surface_water__depth', cmap='Blues', vmin=0,
            grid_units=('m', 'm'), var_name="Water Depth (m)")
plt.title(f"Final Water Depth after {simulation_duration_hr} hours")
plt.show() # block=True for the final plot

print("Script complete.")