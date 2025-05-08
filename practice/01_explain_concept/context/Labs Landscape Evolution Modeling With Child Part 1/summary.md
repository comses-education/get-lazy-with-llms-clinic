# Landscape Evolution Modeling: Understanding Earth's Surface Changes Over Time

Landscape Evolution Models (LEMs) are sophisticated numerical tools that simulate how terrain changes over time through various natural processes. This summary explores the core concepts, history, and applications of these powerful models with a focus on the CHILD model.

## What is a Landscape Evolution Model?

A landscape evolution model is a physically-based numerical model that simulates changing terrain over time. These models calculate the dynamic evolution of a topographic surface (represented as z(x,y,t)) through processes like fluvial and hillslope erosion and sediment transport. LEMs track how landscapes respond to:

- Glacial or fluvial erosion
- Sediment transport and deposition
- Regolith (loose surface material) production
- Slow movement of material on hillslopes
- Intermittent events like rockfalls, debris flows, and landslides
- Surface uplift and subsidence

These changes occur in response to land surfaces being uplifted above sea level by surface uplift, and also respond to subsidence.

## Historical Development

The evolution of landscape modeling reflects advances in both geomorphic understanding and computing power:

- 1960s: First one-dimensional profile models emerged (Culling used diffusion equations to describe escarpment relaxation)
- Early 1970s: More sophisticated models by Ahnert and Kirkby included diffusive soil creep, fluvial downcutting, and weathering processes
- Mid-1970s: First fully two-dimensional landscape evolution models appeared (notably Ahnert's 1976 model)
- Late 1980s-mid 1990s: Beginning of the "modern era" of landscape evolution models
- 1970s onward: Early models simulated water flow across a mesh with cell elevations changed based on calculated erosional power

As computing power increased, LEM capabilities expanded dramatically. Modern landscape evolution models can leverage graphics processing units and other acceleration hardware and software to run more quickly.

## How LEMs Represent Terrain

LEMs divide landscapes into discrete elements to make calculations manageable:

- Most models use square grid cells, but some (like CASCADE and CHILD) use irregular polygons
- CHILD specifically uses hexagonal Voronoi cells, with nodes at cell centers connected by edges of the Delaunay triangulation
- A "cell" is a patch of ground with boundaries called "faces," while a "node" is the point inside where elevation is tracked
- In irregular meshes, each cell represents the area closer to its node than to any other node (known as Voronoi cells or Thiessen polygons)

The model represents not just the surface but also vegetation, channelized cells, and soil/sediment layers above bedrock.

## Core Principles: Continuity of Mass

At the heart of LEMs is the principle of mass continuity. A typical mass continuity equation for a column of soil or rock is:

∂η/∂t = B - ∇q⃗_s

Where:
- η is the elevation of the land surface
- t is time
- B represents vertical motion relative to baselevel (tectonic uplift/subsidence)
- q⃗_s is sediment flux per unit width

For discrete elements in the model, this becomes:

dηi/dt = B + (1/Λi) ∑(j=1 to N) qsj λj

Where:
- Λi is the horizontal surface area of cell i
- N is the number of faces surrounding the cell
- qsj is the unit flux across face j
- λj is the length of face j

This equation expresses a finite-volume method, computing fluxes in and out along the boundaries of a finite volume of space.

## Key Processes Modeled

LEMs incorporate various geomorphic processes:

### Hillslope Processes
- Linear diffusion for gentle slopes: q⃗_s = -D∇η (where D is a transport coefficient)
- Nonlinear diffusion for steeper slopes: q⃗_s = -D∇z/(1-|∇z/Sc|²)
- Soil creep, frost heave, and sometimes landsliding

### Fluvial Processes
- Erosion and deposition by flowing water
- Channel formation and evolution

### Other Processes
- Weathering of bedrock into regolith
- Tectonic uplift (typically for longer timescales)
- Sediment transport by water, wind, and ice

## The CHILD Model

CHILD (Channel-Hillslope Integrated Landscape Development) is a prominent landscape evolution model:

- Developed in 1997 by Nicole Gasparini, Stephen Lancaster, and Greg Tucker at MIT under Rafael Bras
- Uses irregular polygons (Voronoi cells) for terrain discretization
- Includes stochastic rainfall simulation capabilities
- Continues to be developed with contributions from researchers worldwide

CHILD computes the time evolution of a topographic surface through fluvial and hillslope erosion and sediment transport processes.

## Real-World Applications

LEMs have diverse practical applications:

### Example Simulations
- **Fault Block Uplift and Subsidence**: Simulating a pair of normal-fault blocks separated by a vertical fault, showing how fan-delta complexes prograde as relief and sediment flux increase
- **River Valley Evolution**: Modeling stratigraphy and geoarchaeology under different scenarios including steady aggradation and incision/aggradation histories

### Practical Uses
- Forecasting mine-spoil degradation
- Estimating erosion risk to buried hazardous waste
- Applications ranging from soil erosion to continental collision
- Land management decision support for degraded landscapes

## Visual Understanding of Landscape Evolution

G.K. Gilbert, a 19th-century geologist, provided eloquent "word pictures" that still inform our understanding:

"We have seen that the declivity over which water flows bears an inverse relation to the quantity of water. If we follow a stream from its mouth upward... we find its volume gradually less and less and its grade steeper and steeper, until finally at its head we reach the steepest grade of all."

This creates river profiles that are "concave upward and with the greatest curvature at the upper end." Similarly, "mountains are steepest at their crests" with profiles that are "concave outward" when taken along drainage lines.

## Community Modeling Through CSDMS

The Community Surface Dynamics Modeling System (CSDMS) provides resources for researchers to access and use landscape evolution models:

- Web Modeling Tool (WMT) for configuring and running models
- Shared supercomputing resources
- Visualization tools and educational materials
- A collaborative community for model development and sharing

As LEMs continue to improve, they increasingly serve as valuable tools for both scientific research and practical land management applications.
