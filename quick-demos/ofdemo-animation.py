import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
frames = []
rmg.at_node["surface_water__depth"][:] = h_init

while elapsed_time < run_time:
    dt = of.calc_time_step()
    of.overland_flow()
    elapsed_time += dt
    frames.append(rmg.at_node["surface_water__depth"].copy())

fig, ax = plt.subplots()
x, y = rmg.node_x.reshape(rmg.shape), rmg.node_y.reshape(rmg.shape)
depth = frames[0].reshape(rmg.shape)
mesh = ax.pcolormesh(x, y, depth, cmap="Blues", shading="auto")
title = ax.set_title("")

def update(i):
    mesh.set_array(frames[i].reshape(-1))
    title.set_text(f"timestep {i}")
    return mesh,

ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=50)
ani.save("ofanimation.gif", writer="pillow", fps=10)

print("Saved ofanimation.gif")
