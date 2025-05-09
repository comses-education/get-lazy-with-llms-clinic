import matplotlib.pyplot as plt

from landlab.components.overland_flow import OverlandFlow
from landlab.io import esri_ascii

run_time = 100  # total simulation duration (s)
h_init = 0.1  # initial water depth (m)
n = 0.01  # Manning's n
g = 9.8  # gravity (m/s^2)
alpha = 0.7  # time-step factor
u = 0.4  # constant velocity

with open("Square_TestBasin.asc") as fp:
    rmg = esri_ascii.load(fp, name="topographic__elevation", at="node")

rmg.set_closed_boundaries_at_grid_edges(True, True, True, True)
my_outlet_node = 100
rmg.status_at_node[my_outlet_node] = 1
rmg.add_zeros("surface_water__depth", at="node")
rmg.at_node["surface_water__depth"] += h_init

of = OverlandFlow(rmg, steep_slopes=True)

elapsed_time = 1.0
while elapsed_time < run_time:
    dt = of.calc_time_step()
    of.overland_flow()
    elapsed_time += dt

elapsed_time = 1.0
rmg.at_node["surface_water__depth"][:] = h_init

while elapsed_time < run_time:
    dt = of.calc_time_step()
    of.overland_flow()
    elapsed_time += dt

rmg.imshow("surface_water__depth", cmap="Blues")

plt.show()