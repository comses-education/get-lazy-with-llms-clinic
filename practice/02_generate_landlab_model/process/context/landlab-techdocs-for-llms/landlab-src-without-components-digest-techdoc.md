Okay, here is a detailed technical document section based on the `landlab-src-without-components-digest`.

```markdown
# Landlab Core Framework: Grids, Fields, Utilities, and I/O

## 1. Introduction

This document details the core functionalities of the Landlab framework, focusing on the foundational elements necessary to build and run landscape models. It covers the creation and manipulation of various grid types, the management of data fields associated with these grids, essential utilities for calculations and grid operations, input/output capabilities, and the basic structure for model components and interoperability.

This section specifically excludes the detailed process components (like erosion, flow routing algorithms, etc.) found in `landlab.components`. It focuses on the underlying machinery that these components utilize. Understanding these core concepts is crucial for both using existing Landlab components and developing new ones.

Key areas covered:

*   **Grids:** Creating and interacting with different grid types (Raster, Hex, Voronoi, Radial, Network, FramedVoronoi).
*   **Fields:** Storing and accessing data associated with grid elements (nodes, links, patches, cells, etc.).
*   **Core Utilities:** Functions for common grid operations, calculations (gradients, divergence, mapping), boundary condition handling, and geometric analysis.
*   **Data Structures:** Specialized structures for handling time-series data (`DataRecord`) and layered stratigraphy (`EventLayers`, `MaterialLayers`).
*   **Input/Output:** Reading and writing grid data in various formats (ESRI ASCII, NetCDF, VTK, Native Landlab).
*   **Plotting:** Basic visualization tools for grids and fields.
*   **Cellular Automata Framework:** Tools for building continuous-time stochastic cellular automata models.
*   **Basic Model Interface (BMI):** Landlab's implementation for model interoperability.
*   **Framework Foundation:** Base classes, parameter loading, and command-line tools.

## 2. Core Concepts

### 2.1. The Model Grid (`landlab.grid`)

The `ModelGrid` is the central object in Landlab, representing the spatial domain of your model. All other Landlab elements (fields, components) operate on or interact with a grid object. Landlab provides several grid types inheriting from `ModelGrid`.

**Key Base Class:** `landlab.grid.base.ModelGrid`

While you typically instantiate specific grid types (like `RasterModelGrid`), understanding the base class properties is useful:

*   **Grid Elements:** Landlab grids are composed of elements like nodes, links, patches, cells, faces, and corners. The availability depends on the grid type (e.g., `RasterModelGrid` has nodes, links, patches, cells, faces, corners; `NetworkModelGrid` primarily has nodes and links).
*   **Coordinates:** Access node coordinates via properties like `grid.x_of_node`, `grid.y_of_node`, `grid.xy_of_node`.
*   **Connectivity:** Information about how elements connect (e.g., `grid.nodes_at_link`, `grid.links_at_node`, `grid.patches_at_node`).
*   **Geometric Properties:** Properties like `grid.length_of_link`, `grid.area_of_cell`.
*   **Boundary Conditions:** Nodes have statuses (core, fixed value, fixed gradient, closed, looped) accessed via `grid.status_at_node`. Link statuses (`grid.status_at_link`) are derived from node statuses. See Section 5.3 for details.

### 2.2. Fields (`landlab.field`)

Data associated with a model grid (like elevation, water depth, erosion rate) are stored in *fields*. Fields are attached to specific grid elements (nodes, links, patches, cells, etc.).

**Key Class:** `landlab.field.graph_field.GraphFields` (Used internally by `ModelGrid`)

You interact with fields primarily through the grid object using dictionary-like accessors:

*   `grid.at_node`: Dictionary of fields defined at nodes.
*   `grid.at_link`: Dictionary of fields defined at links.
*   `grid.at_patch`: Dictionary of fields defined at patches.
*   `grid.at_cell`: Dictionary of fields defined at cells.
*   `grid.at_face`: Dictionary of fields defined at faces.
*   `grid.at_corner`: Dictionary of fields defined at corners.
*   `grid.at_grid`: Dictionary for grid-wide scalar values.

**Accessing Fields:**

```python
import numpy as np
from landlab import RasterModelGrid

# Create a grid
grid = RasterModelGrid((3, 4))

# Add a field of zeros at nodes
grid.add_zeros('topographic__elevation', at='node')

# Access the field as a NumPy array
elevation_array = grid.at_node['topographic__elevation']
print(elevation_array)
# Output: [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]

# Modify the field
grid.at_node['topographic__elevation'] += 1.0
print(grid.at_node['topographic__elevation'])
# Output: [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
```

See Section 4 for more details on creating and managing fields.

## 3. Creating and Using Grids (`landlab.grid`)

### 3.1. Creating Grids (`landlab.grid.create.create_grid`)

The most common way to create a grid is using the `create_grid` function, often reading parameters from a file or dictionary.

```python
from landlab import create_grid
from io import StringIO

# Define grid parameters in a YAML-like string
grid_params_string = """
grid:
  RasterModelGrid:
    - [4, 5] # Shape (rows, cols)
    - xy_spacing: [2, 3] # Spacing (dy, dx)
    - xy_of_lower_left: [10, 20] # Coordinates of lower-left node
"""

# Create the grid
grid = create_grid(StringIO(grid_params_string), section="grid")

print(grid.shape)
# Output: (4, 5)
print(grid.dy, grid.dx)
# Output: 2.0 3.0
print(grid.xy_of_lower_left)
# Output: (10.0, 20.0)

# Grid creation can also include initial fields and boundary conditions
grid_params_string_with_extras = """
grid:
  RasterModelGrid:
    - [4, 5]
    - xy_spacing: 1.0
    - fields:
        node:
          topographic__elevation:
            plane:
              - point: [1, 1, 1]
                normal: [0, 0, 1] # Horizontal plane at z=1
            units:
              - units: "meters"
    - boundary_conditions:
        - set_closed_boundaries_at_grid_edges:
            - True  # right
            - False # top
            - True  # left
            - False # bottom
"""
grid_with_extras = create_grid(StringIO(grid_params_string_with_extras), section="grid")
print("Elevation field exists:", 'topographic__elevation' in grid_with_extras.at_node)
# Output: Elevation field exists: True
print("Elevation units:", grid_with_extras.field_units("topographic__elevation", at="node"))
# Output: Elevation units: meters
print("Boundary statuses (first row):", grid_with_extras.status_at_node[:5])
# Output: Boundary statuses (first row): [4 1 1 1 4]
```

### 3.2. Specific Grid Types

#### 3.2.1. Raster Grids (`landlab.grid.raster.RasterModelGrid`)

Uniform rectilinear grids are the most common type.

**Instantiation:**

```python
from landlab import RasterModelGrid

# Basic grid with 4 rows, 5 columns, unit spacing
grid = RasterModelGrid((4, 5))

# Grid with specified spacing and origin
grid_spaced = RasterModelGrid((4, 5), xy_spacing=(2.0, 3.0), xy_of_lower_left=(10.0, 20.0))

# Grid with specific boundary conditions set at creation
grid_bc = RasterModelGrid((4, 5), bc={'top': 'closed', 'left': 'closed'})
```

**Key Properties/Methods:**

*   `grid.shape`: Tuple `(n_rows, n_cols)`.
*   `grid.dx`, `grid.dy`: Node spacing in x and y.
*   `grid.xy_of_lower_left`: Coordinates of the bottom-left node.
*   `grid.number_of_nodes`, `grid.number_of_links`, etc.
*   `grid.nodes_at_edge('top')`, `grid.nodes_at_bottom_edge`, etc.: Get node IDs along specific edges.
*   `grid.core_nodes`, `grid.boundary_nodes`: Get IDs of core or boundary nodes.
*   `grid.active_links`, `grid.fixed_links`: Get IDs of links based on status.
*   `grid.neighbors_at_node`, `grid.active_neighbors_at_node`: Get neighbor node IDs (D4 connectivity).
*   `grid.diagonal_neighbors_at_node`: Get diagonal neighbor IDs (D8 connectivity).
*   `grid.node_vector_to_raster()`: Reshape a node array to the grid's 2D shape.
*   See Section 5 for boundary condition methods like `set_closed_boundaries_at_grid_edges`.
*   See Section 5 for gradient, divergence, and mapping methods applicable to rasters.

#### 3.2.2. Hexagonal Grids (`landlab.grid.hex.HexModelGrid`)

Grids composed of hexagonal cells (nodes are centers) and triangular patches.

**Instantiation:**

```python
from landlab import HexModelGrid

# Basic hexagonal layout
grid_hex = HexModelGrid((5, 3), node_layout='hex') # 5 rows deep, 3 nodes wide at center

# Rectangular layout, vertical orientation
grid_rect_vert = HexModelGrid((4, 3), node_layout='rect', orientation='vertical')
```

**Key Properties/Methods:**

*   Similar connectivity properties as `RasterModelGrid`, but adapted for hex geometry (e.g., up to 6 links/neighbors per node).
*   `grid.orientation`: 'horizontal' or 'vertical'.
*   `grid.node_layout`: 'hex' or 'rect'.
*   See Section 5 for gradient, divergence, and mapping methods applicable to hex grids.

#### 3.2.3. Voronoi-Delaunay Grids (`landlab.grid.voronoi.VoronoiDelaunayGrid`)

Unstructured grids based on Voronoi cells and their dual Delaunay triangulation.

**Instantiation:**

```python
import numpy as np
from landlab import VoronoiDelaunayGrid

# Create from random points
x_coords = np.random.rand(50)
y_coords = np.random.rand(50)
grid = VoronoiDelaunayGrid(x_coords, y_coords)

# Create from structured points (useful for comparison)
x_rect, y_rect = np.meshgrid(np.arange(5.), np.arange(4.))
grid_rect = VoronoiDelaunayGrid(x_rect.flatten(), y_rect.flatten())
```

**Key Properties/Methods:**

*   Nodes are exactly at the input `(x, y)` coordinates.
*   Links connect Delaunay neighbors.
*   Patches are Delaunay triangles.
*   Cells are Voronoi polygons.
*   Corners are Voronoi vertices.
*   Faces are Voronoi edges shared between cells.
*   Includes properties for both the primary (Delaunay) and dual (Voronoi) graph structures.

#### 3.2.4. Radial Grids (`landlab.grid.radial.RadialModelGrid`)

Grids composed of nodes arranged in concentric circles.

**Instantiation:**

```python
from landlab import RadialModelGrid

# Grid with 3 rings, 6 nodes in the first ring (plus center node)
grid = RadialModelGrid(n_rings=3, nodes_in_first_ring=6)
```

**Key Properties/Methods:**

*   `grid.number_of_rings`.
*   `grid.spacing_of_rings`.
*   `grid.xy_of_center`.
*   Based on `VoronoiDelaunayGrid`, so has similar properties.

#### 3.2.5. Network Grids (`landlab.grid.network.NetworkModelGrid`)

Grids representing networks, primarily composed of nodes and links, often used for river networks.

**Instantiation:**

```python
from landlab import NetworkModelGrid

y_of_node = (0, 1, 2, 2)
x_of_node = (0, 0, -1, 1)
nodes_at_link = ((1, 0), (2, 1), (3, 1)) # (tail, head)
grid = NetworkModelGrid((y_of_node, x_of_node), links=nodes_at_link)
```

**Key Properties/Methods:**

*   Designed for 1D connectivity along links.
*   Does not typically have patches or cells defined inherently (unless imported).
*   Often created using `read_shapefile` (see Section 7).

#### 3.2.6. Framed Voronoi Grids (`landlab.grid.framed_voronoi.FramedVoronoiGrid`)

A hybrid grid with a Voronoi-Delaunay interior and a structured perimeter, useful for specific boundary condition types or coupling structured and unstructured domains.

**Instantiation:**

```python
from landlab import FramedVoronoiGrid

# Create a 5x6 grid with some randomization of interior nodes
grid = FramedVoronoiGrid((5, 6), xy_min_spacing=0.7, seed=123)
```

**Key Properties/Methods:**

*   Combines features of `RasterModelGrid` (perimeter) and `VoronoiDelaunayGrid` (interior).
*   Boundary nodes are fixed on a rectangular lattice.
*   Interior nodes are based on the lattice but randomly perturbed.

### 3.3. Graph Topology (`landlab.graph`)

Underlying the user-facing `grid` objects are `graph` objects that define the connectivity and basic geometry. Users typically don't interact directly with these unless developing new grid types or components needing low-level topology access.

**Key Concepts:**

*   **Primary Graph:** Typically nodes, links, and patches (often Delaunay triangles). Represented by classes like `Graph`, `StructuredQuadGraph`, `DelaunayGraph`, `TriGraph`.
*   **Dual Graph:** Represents the connectivity of cells, faces, and corners (often Voronoi polygons). Represented by classes like `DualGraph`, `DualStructuredQuadGraph`, `DualVoronoiGraph`, `DualHexGraph`.
*   The user-facing `grid` objects often inherit from both a primary and a dual graph type (e.g., `RasterModelGrid` inherits from `DualUniformRectilinearGraph`, which inherits from `DualGraph` and `UniformRectilinearGraph`).
*   Accessing the dual graph: `grid.dual` (for grids that have a dual).

## 4. Working with Fields (`landlab.field`)

As introduced in Section 2.2, fields store data on grid elements.

### 4.1. Adding Fields

Several methods exist to add fields to a grid:

```python
from landlab import RasterModelGrid
import numpy as np

grid = RasterModelGrid((3, 4))

# Add a field initialized to zeros (most common)
grid.add_zeros('soil__depth', at='node', dtype=float)
print(grid.at_node['soil__depth'])
# Output: [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]

# Add a field initialized to ones
grid.add_ones('vegetation__cover_fraction', at='node')
print(grid.at_node['vegetation__cover_fraction'])
# Output: [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]

# Add a field initialized to a constant value
grid.add_full('bedrock__elevation', -10.0, at='node')
print(grid.at_node['bedrock__elevation'])
# Output: [-10. -10. -10. -10. -10. -10. -10. -10. -10. -10. -10. -10.]

# Add a field using an existing NumPy array (creates a *reference*)
my_data = np.arange(grid.number_of_nodes)
grid.add_field('my_node_data', my_data, at='node')
print(grid.at_node['my_node_data'][5])
# Output: 5.0

# Add a field using a *copy* of an existing NumPy array
my_other_data = np.linspace(0, 1, grid.number_of_links)
grid.add_field('my_link_data', my_other_data, at='link', copy=True)

# Attempting to add a field that already exists raises an error...
try:
    grid.add_zeros('soil__depth', at='node')
except FieldError as e:
    print(e)
    # Output: soil__depth

# ...unless you use clobber=True
grid.add_zeros('soil__depth', at='node', clobber=True)
```

### 4.2. Accessing Fields

Access fields like dictionary items:

```python
# grid defined above

# Get the whole array
elev = grid.at_node['topographic__elevation'] # Assuming this exists

# Get a single value
elev_at_node_5 = grid.at_node['topographic__elevation'][5]

# Get a slice
elev_slice = grid.at_node['topographic__elevation'][3:7]
```

### 4.3. Checking for Fields

```python
# grid defined above

if grid.has_field('topographic__elevation', at='node'):
    print("Node elevation field exists.")
else:
    print("Node elevation field does not exist.")
# Output: Node elevation field exists.

print("Cell elevation field exists:", grid.has_field('topographic__elevation', at='cell'))
# Output: Cell elevation field exists: False
```

### 4.4. Field Metadata

You can associate units with fields:

```python
# grid defined above

grid.add_zeros('precipitation_rate', at='grid', units='mm/hr')
print(grid.field_units('precipitation_rate', at='grid'))
# Output: mm/hr

# Check all field units
print(grid.units) # For the base ModelGrid, might be empty or just coordinates
```

## 5. Grid Utilities

Landlab provides numerous functions attached to grid objects for common tasks.

### 5.1. Mappers (`landlab.grid.mappers`)

Map values from one grid element type to another (e.g., from nodes to links).

```python
from landlab import RasterModelGrid
import numpy as np

grid = RasterModelGrid((3, 4))
grid.add_zeros('node_values', at='node')
grid.at_node['node_values'][:] = np.arange(grid.number_of_nodes)

# Map the value at the head node of each link to the link
head_node_values = grid.map_link_head_node_to_link('node_values')
print(head_node_values[[0, 1, 2, 3, 4]]) # First 5 links
# Output: [1. 2. 3. 4. 5.]

# Map the mean value of the two nodes defining a link to the link
mean_node_values = grid.map_mean_of_link_nodes_to_link('node_values')
print(mean_node_values[[0, 1, 2, 3, 4]]) # First 5 links
# Output: [0.5 1.5 2.5 2.  3. ]

# Map the minimum value of the links touching a node to the node
grid.add_zeros('link_values', at='link')
grid.at_link['link_values'][:] = np.arange(grid.number_of_links)
min_link_values = grid.map_min_of_node_links_to_node('link_values')
print(min_link_values)
# Output: [ 0.  0.  1.  2.  3.  4.  5.  6.  7.  8.  9. 13.]
```

Specific mappers exist for different grid types (e.g., `map_link_vector_components_to_node` has different implementations for Raster and Hex grids accessed via the grid object).

### 5.2. Gradients and Divergence (`landlab.grid.gradients`, `landlab.grid.divergence`)

Calculate gradients (node values -> link values) and divergences (link fluxes -> node values).

```python
from landlab import RasterModelGrid
import numpy as np

grid = RasterModelGrid((3, 4))
grid.add_zeros('elevation', at='node')
grid.at_node['elevation'][:] = grid.x_of_node + grid.y_of_node

# Calculate elevation gradient at links
grad_at_link = grid.calc_grad_at_link('elevation')
print(np.round(grad_at_link, 2))
# Output: [1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]

# Assume 'grad_at_link' represents a flux potential gradient, calculate flux divergence
# (using unit flux = -gradient for illustration)
flux_div_at_node = grid.calc_flux_div_at_node(-grad_at_link)
print(np.round(flux_div_at_node, 2))
# Output: [-0. -0. -0. -0. -0. -2. -2. -0. -0. -0. -0. -0.]

# Calculate slope and aspect at nodes (based on surrounding patches)
slope_mag, (slope_x, slope_y) = grid.calc_slope_at_node('elevation', return_components=True)
print("Slope magnitude (radians):", np.round(slope_mag[5], 2))
# Output: Slope magnitude (radians): 0.95
print("Slope x-component (radians):", np.round(slope_x[5], 2))
# Output: Slope x-component (radians): 0.69
print("Slope y-component (radians):", np.round(slope_y[5], 2))
# Output: Slope y-component (radians): 0.69
```

### 5.3. Boundary Conditions (`landlab.grid.nodestatus`, `landlab.grid.linkstatus`, `landlab.grid.raster_set_status`)

Control the behavior of grid edges.

**Node Status Codes:**

*   `NodeStatus.CORE` (0): Interior node.
*   `NodeStatus.FIXED_VALUE` (1): Boundary node where the value is held constant.
*   `NodeStatus.FIXED_GRADIENT` (2): Boundary node where the gradient is held constant.
*   `NodeStatus.LOOPED` (3): Boundary node that wraps around to the opposite side.
*   `NodeStatus.CLOSED` (4): Boundary node where no flux is allowed.

**Accessing and Setting Node Status:**

```python
from landlab import RasterModelGrid, NodeStatus

grid = RasterModelGrid((3, 4))

# Default status (core nodes are 0, boundary nodes are 1)
print(grid.status_at_node)
# Output: [1 1 1 1 1 0 0 1 1 1 1 1]

# Set the top edge to be closed
grid.status_at_node[grid.nodes_at_top_edge] = NodeStatus.CLOSED
print(grid.status_at_node)
# Output: [1 1 1 1 1 0 0 1 4 4 4 4]

# Use helper function for raster grids
grid = RasterModelGrid((3, 4))
grid.set_closed_boundaries_at_grid_edges(False, True, False, True) # R, T, L, B
print(grid.status_at_node)
# Output: [4 4 4 4 1 0 0 1 4 4 4 4]
```

**Link Status Codes:**

*   `LinkStatus.ACTIVE` (0): Link allows flux, typically connects two core nodes or a core and fixed-value node.
*   `LinkStatus.FIXED` (2): Link where gradient is fixed, typically connects a core and fixed-gradient node.
*   `LinkStatus.INACTIVE` (4): Link does not allow flux, typically connects two boundary nodes or involves a closed node.

**Accessing Link Status:**

Link status is derived from node status and accessed via `grid.status_at_link`.

```python
# grid from previous example (top and bottom closed)
print(grid.status_at_link)
# Output: [4 4 4 4 0 0 4 4 0 0 4 4 4 4 4 4 4]
```

### 5.4. Other Utilities (`landlab.utils`)

*   **Halo Operations (`add_halo`):** Add a buffer of nodes around a raster grid, often useful for boundary condition handling in numerical methods.
*   **Watershed Delineation (`watershed`):** Functions like `get_watershed_mask`, `get_watershed_nodes`, `get_watershed_outlet` based on flow directions (requires flow routing component outputs).
*   **Flow Distance (`flow__distance`):** Calculate distance along flow paths to outlets (`calculate_flow__distance`).
*   **Source Tracking (`source_tracking_algorithm`):** Track the origin of material or flow (`track_source`).
*   **Window Statistics (`window_statistic`):** Calculate statistics within a moving window around nodes (`calculate_window_statistic`).

```python
from landlab import RasterModelGrid
from landlab.components import FlowAccumulator
from landlab.utils import get_watershed_mask, calculate_flow__distance
import numpy as np

# Example: Watershed delineation requires flow fields first
grid = RasterModelGrid((5, 5))
grid.at_node['topographic__elevation'] = grid.x_of_node + grid.y_of_node
# Set boundary conditions: closed N, E, W; fixed value (outlet) S
grid.set_closed_boundaries_at_grid_edges(True, True, True, False)
grid.status_at_node[1] = grid.BC_NODE_IS_FIXED_VALUE # Outlet at node 1

# Run flow routing (component not detailed here, just showing setup)
fr = FlowAccumulator(grid)
fr.run_one_step()

# Get watershed mask for outlet node 1
ws_mask = get_watershed_mask(grid, 1)
print(ws_mask.reshape(grid.shape))
# Output:
# [[False False False False False]
#  [False  True  True  True False]
#  [False  True  True  True False]
#  [False  True  True  True False]
#  [False  True  True  True False]]

# Calculate flow distance to the outlet
dist = calculate_flow__distance(grid)
print(np.round(dist.reshape(grid.shape), 1))
# Output:
# [[0.  0.  0.  0.  0. ]
#  [0.  4.  3.  2.  0. ]
#  [0.  3.  2.  1.  0. ]
#  [0.  2.  1.  0.  0. ]
#  [0.  1.  0.  0.  0. ]]
```

## 6. Data Handling (`landlab.data_record`, `landlab.layers`)

### 6.1. DataRecord (`landlab.data_record.DataRecord`)

Manages time-series or item-based data associated with a grid. Useful for tracking cohorts of particles, clasts, or other discrete elements over time and space.

**Creating a DataRecord:**

```python
from landlab import RasterModelGrid
from landlab.data_record import DataRecord
import numpy as np

grid = RasterModelGrid((3, 3))

# Record tracking items (e.g., clasts) at specific nodes at time 0
initial_items = {
    "grid_element": np.array([["node"], ["node"]]), # Both items are at nodes
    "element_id": np.array([[1], [4]])           # IDs of the nodes they are at
}
initial_data = {
    "clast__size": (["item_id", "time"], np.array([[10.0], [20.0]])) # Size varies by item and time
}

dr = DataRecord(grid, time=[0.0], items=initial_items, data_vars=initial_data)

print(dr.dataset)
# Output:
# <xarray.Dataset>
# Dimensions:       (item_id: 2, time: 1)
# Coordinates:
#   * time          (time) float64 0.0
#   * item_id       (item_id) int64 0 1
# Data variables:
#     grid_element  (item_id, time) <U4 'node' 'node'
#     element_id    (item_id, time) int64 1 4
#     clast__size   (item_id, time) float64 10.0 20.0
```

**Adding Records/Items:**

```python
# Add data for a new time step for existing items
dr.add_record(time=[1.0], item_id=[0, 1], new_record={
    "clast__size": (["item_id", "time"], np.array([[9.0], [19.0]]))
})

# Add a completely new item at time 1.0
dr.add_item(time=[1.0], new_item={
    "grid_element": np.array([["link"]]), # This one is on a link
    "element_id": np.array([[5]])
}, new_item_spec={
    "clast__size": (["item_id", "time"], [[15.0]]) # Its size
})

print(dr.dataset)
# Output (shows NaNs where data wasn't added for a specific item/time):
# <xarray.Dataset>
# Dimensions:       (item_id: 3, time: 2)
# Coordinates:
#   * time          (time) float64 0.0 1.0
#   * item_id       (item_id) int64 0 1 2
# Data variables:
#     grid_element  (item_id, time) object 'node' nan nan 'link' nan 'link'
#     element_id    (item_id, time) float64 1.0 nan nan 5.0 nan 5.0
#     clast__size   (item_id, time) float64 10.0 9.0 20.0 19.0 nan 15.0

# Note: Using ffill helps fill gaps based on previous state
dr.ffill_grid_element_and_id() # Fills element_id and grid_element forward in time
print(dr.dataset['element_id'])
# Output:
# <xarray.DataArray 'element_id' (item_id: 3, time: 2)> Size: 48B
# array([[ 1.,  1.],
#        [ 4.,  4.],
#        [nan,  5.]])
# Coordinates:
#   * time     (time) float64 0.0 1.0
#   * item_id  (item_id) int64 0 1 2
```

**Aggregating Data:**

`DataRecord` includes methods (`calc_aggregate_value`) to calculate statistics (sum, mean, count) of item properties grouped by the grid element they reside on. See `landlab.data_record.aggregators`.

### 6.2. Layers (`landlab.layers`)

Track stratigraphy or other layered phenomena at grid cells.

**Key Classes:**

*   `EventLayers`: Each call to `add()` creates a new layer, even for erosion (thickness zero). Useful for detailed chronostratigraphy.
*   `MaterialLayers`: Only creates new layers for deposition if the material properties differ from the surface layer. Erosion removes material from the top. More memory efficient if detailed event history isn't needed.

**Usage (MaterialLayers example):**

```python
from landlab import RasterModelGrid
from landlab.layers import MaterialLayers # Or EventLayers

grid = RasterModelGrid((1, 5)) # 1 row of cells
layers = MaterialLayers(grid.number_of_cells) # One stack per cell

# Add initial layers with properties
layers.add(1.0, age=100.0, type='sand')
layers.add(0.5, age=50.0, type='mud')

print("Number of layers:", layers.number_of_layers)
# Output: Number of layers: 2
print("Thicknesses:\n", layers.dz)
# Output:
# Thicknesses:
# [[1. 1. 1.]
#  [0.5 0.5 0.5]]
print("Ages:\n", layers['age'])
# Output:
# Ages:
# [[100. 100. 100.]
#  [ 50.  50.  50.]]

# Add more 'mud' - combines with the top layer
layers.add(0.2, age=50.0, type='mud')
print("Number of layers:", layers.number_of_layers)
# Output: Number of layers: 2
print("Thicknesses:\n", layers.dz)
# Output:
# Thicknesses:
# [[1.  1.  1. ]
#  [0.7 0.7 0.7]]

# Erode some material
layers.add(-0.3)
print("Thicknesses:\n", layers.dz)
# Output:
# Thicknesses:
# [[1.  1.  1. ]
#  [0.4 0.4 0.4]]

# Add a different material - creates a new layer
layers.add(0.6, age=20.0, type='gravel')
print("Number of layers:", layers.number_of_layers)
# Output: Number of layers: 3
print("Thicknesses:\n", layers.dz)
# Output:
# Thicknesses:
# [[1.  1.  1. ]
#  [0.4 0.4 0.4]
#  [0.6 0.6 0.6]]
print("Types:\n", layers['type'])
# Output:
# Types:
# [[  0.   0.   0.] # Assuming default fill for 'type' was 0
#  [  1.   1.   1.] # Assuming default fill for 'type' was 1
#  [  2.   2.   2.]]# Assuming default fill for 'type' was 2
# Note: Actual string/float tracking depends on initial setup.
```

## 7. Input/Output (`landlab.io`)

Landlab supports reading and writing grids and fields in several formats.

### 7.1. ESRI ASCII (`landlab.io.esri_ascii`)

Used for raster data, common in GIS.

**Loading:**

```python
from landlab.io import esri_ascii
from io import StringIO

# Example ASCII content
ascii_data = """
NCOLS 4
NROWS 3
XLLCORNER 10.0
YLLCORNER 20.0
CELLSIZE 2.0
NODATA_VALUE -9999
1 2 3 4
5 6 7 8
9 10 11 12
"""

# Load grid and data field
grid = esri_ascii.load(StringIO(ascii_data), name='elevation')

print(grid.shape)
# Output: (3, 4)
print(grid.dx, grid.dy)
# Output: 2.0 2.0
print(grid.xy_of_lower_left)
# Output: (10.0, 20.0)
print(grid.at_node['elevation'].reshape(grid.shape))
# Output:
# [[ 9. 10. 11. 12.]
#  [ 5.  6.  7.  8.]
#  [ 1.  2.  3.  4.]]
```

**Dumping:**

```python
# grid defined above
output_string = esri_ascii.dump(grid, name='elevation')
print(output_string.strip().split('\n')[0]) # Just show first line
# Output: NROWS 3
```

### 7.2. NetCDF (`landlab.io.netcdf`)

A common format for scientific data, supports metadata and multiple variables.

**Writing:**

```python
from landlab import RasterModelGrid
from landlab.io.netcdf import to_netcdf
import os
import tempfile
import xarray as xr

grid = RasterModelGrid((3, 4))
grid.add_zeros('elevation', at='node')
grid.add_zeros('temp', at='cell')

# Need a real file path for NetCDF
temp_dir = tempfile.mkdtemp()
file_path = os.path.join(temp_dir, 'my_grid.nc')

# Write all fields
to_netcdf(grid, file_path, format='NETCDF4')

# Write only node fields
# to_netcdf(grid, file_path, include='at_node:*', format='NETCDF4')
```

**Reading:**

```python
from landlab.io.netcdf import from_netcdf

# Read the grid back (assuming file_path exists from writing example)
loaded_grid = from_netcdf(file_path)

print(loaded_grid.shape)
# Output: (3, 4)
print('elevation' in loaded_grid.at_node)
# Output: True
print('temp' in loaded_grid.at_cell)
# Output: True

# Clean up temporary file/directory if necessary
# import shutil
# shutil.rmtree(temp_dir)
```

### 7.3. Legacy VTK (`landlab.io.legacy_vtk`)

Format for visualization software like ParaView or VisIt.

```python
from landlab import RasterModelGrid
from landlab.io.legacy_vtk import write_legacy_vtk
import io

grid = RasterModelGrid((3, 4))
grid.add_zeros('elevation', at='node')

# Write to a string buffer for demonstration
vtk_buffer = io.StringIO()
write_legacy_vtk(vtk_buffer, grid, fields=['elevation'])
vtk_content = vtk_buffer.getvalue()
print(vtk_content.splitlines()[0])
# Output: # vtk DataFile Version 2.0
```

### 7.4. Shapefile (`landlab.io.shapefile`)

Read network geometry from polyline shapefiles to create `NetworkModelGrid`. Can optionally merge attributes from point shapefiles located at junctions.

```python
from landlab.io.shapefile import read_shapefile
# Assuming 'network.shp' and 'network.dbf' exist,
# and optionally 'junctions.shp' and 'junctions.dbf' exist.

# grid = read_shapefile('network.shp', points_shapefile='junctions.shp')
# print(grid.number_of_nodes, grid.number_of_links)
# Field data from the shapefiles would be loaded into grid.at_link and grid.at_node
```
*(Note: Running the shapefile example requires actual files, which are not part of the digest)*

### 7.5. Native Landlab Format (`landlab.io.native_landlab`)

Uses Python's `pickle` to save/load entire grid objects, including fields and state. Convenient but potentially fragile between Landlab versions.

```python
from landlab import RasterModelGrid
from landlab.io.native_landlab import save_grid, load_grid
import os
import tempfile

grid = RasterModelGrid((3, 4))
grid.add_zeros('elevation', at='node')

temp_dir = tempfile.mkdtemp()
file_path = os.path.join(temp_dir, 'my_native_grid.grid')

save_grid(grid, file_path)
loaded_grid = load_grid(file_path)

print(loaded_grid.shape)
# Output: (3, 4)
print('elevation' in loaded_grid.at_node)
# Output: True

# Clean up
# import shutil
# shutil.rmtree(temp_dir)
```

## 8. Plotting (`landlab.plot`)

Basic visualization tools.

**Key Functions:**

*   `imshow_grid`: Plot grid data as colored cells (works for nodes or cells).
*   `imshowhs_grid`: Like `imshow_grid` but adds hillshading (primarily for rasters).
*   `plot_graph`: Plot the structure of the grid (nodes, links, patches).
*   `plot_layers`: Plot cross-sections of layer data.
*   `plot_network_and_parcels`: Specific plotter for `NetworkSedimentTransporter` outputs.

**Example (`imshow_grid`):**

```python
from landlab import RasterModelGrid
from landlab.plot import imshow_grid
import matplotlib.pyplot as plt

grid = RasterModelGrid((5, 6))
grid.add_zeros('elevation', at='node')
grid.at_node['elevation'][:] = grid.x_of_node

plt.figure()
imshow_grid(grid, 'elevation', cmap='viridis', colorbar_label='Elevation (m)')
# plt.show() # Uncomment to display plot interactively
```

## 9. Cellular Automata Framework (`landlab.ca`)

Tools for building Continuous-Time Stochastic (CTS) Cellular Automata models based on Narteau et al. (2002, 2009) and Rozier & Narteau (2014).

**Core Concepts:**

*   **States:** Nodes have discrete integer states.
*   **Transitions:** Defined between pairs of adjacent node states (links). Transitions have a rate (1/T). Actual transition time is stochastic (exponential distribution).
*   **Lattices:** Supports Raster (`RasterCTS`, `OrientedRasterCTS`), Hex (`HexCTS`, `OrientedHexCTS`). "Oriented" versions allow transition rates to depend on link orientation (e.g., horizontal vs. vertical).

**Key Classes:**

*   `landlab.ca.celllab_cts.CellLabCTSModel`: Base class.
*   `landlab.ca.celllab_cts.Transition`: Defines a transition rule (from_state, to_state, rate).
*   Specific grid types: `RasterCTS`, `OrientedRasterCTS`, `HexCTS`, `OrientedHexCTS`.

**Example (Simple Raster CA):**

```python
from landlab import RasterModelGrid
from landlab.ca.celllab_cts import Transition
from landlab.ca.raster_cts import RasterCTS
import numpy as np

# 1. Define Grid
grid = RasterModelGrid((5, 5))

# 2. Define Node States (dictionary: state_code -> state_name)
node_state_dict = {0: 'off', 1: 'on'}

# 3. Define Transitions (list of Transition objects)
# Rule: If an 'off' node (0) is next to an 'on' node (1),
#       it transitions to 'on' (1) at rate 1.0.
#       Here, orientation doesn't matter (code 0).
transitions = [
    Transition((0, 1, 0), (1, 1, 0), 1.0, name='spreading'),
    Transition((1, 0, 0), (1, 1, 0), 1.0, name='spreading_rev')
]

# 4. Define Initial Node States
initial_states = np.zeros(grid.number_of_nodes, dtype=int)
initial_states[grid.core_nodes[0]] = 1 # Turn on one core node

# 5. Instantiate CA model
ca = RasterCTS(grid, node_state_dict, transitions, initial_states)

# 6. Run the model
ca.run(run_to=1.0) # Run for 1 time unit

# Check resulting states (will vary due to stochasticity)
print(ca.node_state.reshape(grid.shape))
```

## 10. Basic Model Interface (BMI) (`landlab.bmi`)

Implements the Basic Model Interface specification for interoperability with other modeling frameworks (e.g., CSDMS pymt).

**Key Functions/Classes:**

*   `wrap_as_bmi(LandlabComponentClass)`: Decorator/function to automatically add BMI methods to a Landlab component class. Landlab components already follow a similar structure, so this is often straightforward.
*   `TimeStepper`: Helper class to manage time stepping within a BMI context.

**Usage Concept:**

```python
# Conceptual example - requires a Landlab component class
from landlab.bmi import wrap_as_bmi
from landlab.components import YourLandlabComponent # Hypothetical component

# Wrap the component
BmiWrappedComponent = wrap_as_bmi(YourLandlabComponent)

# Instantiate the BMI version
bmi_comp = BmiWrappedComponent()

# Use BMI methods (typically called by a framework like pymt)
# bmi_comp.initialize('config_file.yaml')
# bmi_comp.update()
# value_array = np.empty(bmi_comp.get_grid_size(0))
# bmi_comp.get_value('variable_name', value_array)
# bmi_comp.finalize()
```

The BMI wrapper maps Landlab grid elements (node, link, patch, cell, face, corner) to BMI elements (node, edge, face) and handles initialization from configuration files. See `bmi/bmi_bridge.py` documentation for details on the mapping.

## 11. Core Framework Elements (`landlab.core`, `landlab.framework`)

### 11.1. Parameter Loading (`landlab.core.model_parameter_loader.load_params`)

Load model parameters from YAML-formatted files or strings.

```python
from landlab.core import load_params
from io import StringIO

param_string = """
diffusion_coefficient: 0.1
uplift_rate: 0.001
grid_setup:
  shape: [10, 10]
  spacing: 100.0
"""

params = load_params(StringIO(param_string))
print(params['diffusion_coefficient'])
# Output: 0.1
print(params['grid_setup']['shape'])
# Output: [10, 10]
```

### 11.2. Component Base Class (`landlab.core.model_component.Component`)

The base class from which all Landlab process components inherit (components detailed in a separate document section).

**Key Attributes (Class Level):**

*   `_info`: A dictionary defining the input and output fields of the component, including their names, locations (`at_node`, `at_link`, etc.), units, data types, and descriptions. This is crucial for component coupling and validation.
*   `_name`: Name of the component.
*   `input_var_names`: Tuple of required input field names.
*   `output_var_names`: Tuple of output field names generated/updated by the component.
*   `optional_var_names`: Tuple of optional input/output field names.

Components are typically instantiated with a grid object and keyword arguments for parameters:

```python
# Conceptual - Requires a specific component class
# from landlab.components import Diffuser
# from landlab import RasterModelGrid
# grid = RasterModelGrid((5, 5))
# diffuser = Diffuser(grid, D=0.01)
```

### 11.3. Citation Registry (`landlab._registry`)

Tracks instantiated Landlab components and the core library itself for citation purposes.

```python
from landlab import registry, RasterModelGrid
# from landlab.components import Diffuser # Hypothetical

grid = RasterModelGrid((5,5))
# diffuser = Diffuser(grid, D=0.01) # Instantiating adds it to the registry

print("Registered components:", registry.registered)
# Output might be: ('landlab', 'Diffuser')

# Print citation info
# print(registry.format_citations())
```

### 11.4. Command Line Interface (`landlab.cmd`)

Landlab provides a command-line tool (`landlab`) for certain tasks, such as inspecting components or managing author lists (`landlab authors ...`). See `landlab --help` for details. (Requires installation with entry points enabled).

### 11.5. Error Handling (`landlab.core.errors`, `landlab.field.errors`)

Defines custom exception classes (e.g., `MissingKeyError`, `FieldError`, `GroupError`) for more specific error reporting within the framework.

## 12. Conclusion

This section covered the core Landlab framework, providing the foundation for building sophisticated landscape models. Key takeaways include:

*   The `ModelGrid` and its variants (`RasterModelGrid`, `HexModelGrid`, etc.) are central to defining the spatial domain.
*   Data is stored in `fields` associated with grid elements (`grid.at_node`, `grid.at_link`, etc.).
*   A rich set of utilities exists for grid calculations, boundary conditions, and data manipulation.
*   Specialized data structures (`DataRecord`, `EventLayers`, `MaterialLayers`) handle specific data types.
*   I/O functions allow interaction with common file formats.
*   Basic plotting functions aid visualization.
*   Frameworks for Cellular Automata and BMI enable specific modeling paradigms and interoperability.

With this foundation, you can proceed to explore and utilize the specific process components detailed in other sections of the Landlab documentation.
```