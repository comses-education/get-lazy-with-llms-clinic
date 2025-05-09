#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt

from landlab.components.overland_flow import OverlandFlow
from landlab.io import esri_ascii


def main(h_init: float, run_time: float):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OverlandFlow simulation.")
    parser.add_argument("--h-init", type=float, default=0.1, help="Initial water depth (m)")
    parser.add_argument("--run-time", type=float, default=100.0, help="Total run time (s)")
    args = parser.parse_args()

    main(h_init=args.h_init, run_time=args.run_time)