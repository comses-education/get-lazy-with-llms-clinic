Okay, here is a detailed technical document section focusing on the Landlab Process Components, based on the provided `landlab-components-digest.txt`.

---

## Landlab Process Components

This section details the various process components available within the Landlab framework. Components are modular units that represent specific physical processes (e.g., erosion, flow routing, vegetation dynamics) and operate on a Landlab model grid. They interact primarily through shared data fields stored on the grid.

### Overview

Landlab components generally follow a common structure:

1.  **Instantiation:** Components are initialized with a reference to the model grid and process-specific parameters. During instantiation, they typically:
    *   Identify required input fields on the grid.
    *   Create necessary output fields on the grid if they don't exist.
    *   Store references to relevant grid fields and parameters internally.
2.  **Execution:** The core logic of a component is usually executed via a `run_one_step(dt)` method (or a similarly named method like `update`), where `dt` is the duration of the timestep. This method updates the relevant grid fields based on the component's process representation.
3.  **Field Interaction:** Components read input data from grid fields (e.g., `topographic__elevation`) and write output data back to grid fields (e.g., `drainage_area`, updated `topographic__elevation`). This allows components to be easily coupled together in a model.
4.  **Metadata:** Components provide metadata about their required and produced fields via the `_info` dictionary attribute and associated properties like `input_var_names` and `output_var_names`.

### Using Components

A typical workflow involves:

1.  Importing the desired component class (e.g., `from landlab.components import StreamPowerEroder`).
2.  Instantiating the component, passing the grid and necessary parameters (e.g., `sp = StreamPowerEroder(grid, K_sp=0.001)`).
3.  Ensuring all required input fields are present on the grid (e.g., `topographic__elevation`, `drainage_area`). Often, these are created by other components run earlier in the timestep (like `FlowAccumulator`).
4.  Calling the component's `run_one_step(dt)` method within a time loop.

---

### Component Reference

The following subsections detail the major process components available in `landlab.components`, categorized roughly by process type.

#### Flow Routing Components

These components determine the pathways water takes across the landscape, calculate accumulated flow (drainage area and/or discharge), and often identify drainage network structures. They typically require `topographic__elevation` as input and produce fields like `flow__receiver_node`, `drainage_area`, and `surface_water__discharge`.

##### FlowDirector Components (`flow_director/`)

These components calculate flow directions based on topography. They are often used internally by `FlowAccumulator` but can be used standalone.

*   **`FlowDirectorSteepest`:** Calculates single-path flow directions to the steepest downslope neighbor (D4 on rasters).
*   **`FlowDirectorD8`:** Calculates single-path flow directions to the steepest downslope neighbor among 8 neighbors (rasters only).
*   **`FlowDirectorMFD`:** Calculates multiple flow directions to all lower neighbors, partitioning flow usually based on slope.
*   **`FlowDirectorDINF`:** Calculates multiple flow directions using the D-infinity method (Tarboton, 1997), partitioning flow between two neighbors based on aspect (rasters only).

**Common Output Fields:**
*   `flow__receiver_node`: ID of the node receiving flow (or array of IDs for MFD/DINF).
*   `topographic__steepest_slope`: Slope along the flow path(s).
*   `flow__link_to_receiver_node`: ID of the link along the flow path(s).
*   `flow__sink_flag`: Boolean indicating if a node is a local depression.
*   `flow__receiver_proportions` (MFD/DINF only): Fraction of flow sent to each receiver.

**Example (Conceptual - usually used via FlowAccumulator):**

```python
from landlab import RasterModelGrid
from landlab.components import FlowDirectorD8

grid = RasterModelGrid((5, 5))
z = grid.add_field("topographic__elevation", grid.x_of_node + grid.y_of_node, at="node")
# ... (set boundary conditions) ...

fd = FlowDirectorD8(grid, 'topographic__elevation')
fd.run_one_step()

# Access results:
receivers = grid.at_node['flow__receiver_node']
slopes = grid.at_node['topographic__steepest_slope']
```

##### FlowAccumulator (`flow_accum/`)

*   **`FlowAccumulator`:** The primary component for calculating drainage area and discharge. It uses an internal `FlowDirector` (specified during instantiation) to determine flow paths and then efficiently calculates accumulation using the methods of Braun & Willett (2013). Can optionally handle depressions using an internal `DepressionFinder`.

    *   **Purpose:** Calculate drainage area and/or surface water discharge by accumulating flow across the grid based on topography.
    *   **Key Parameters:**
        *   `grid`: The model grid.
        *   `surface`: Field name or array for the topographic surface.
        *   `flow_director`: Specifies the flow directing method ('Steepest', 'D8', 'MFD', 'DINF', or a FlowDirector class/instance).
        *   `runoff_rate`: Spatially/temporally constant rate or field name for spatially/temporally variable rates (`water__unit_flux_in`).
        *   `depression_finder`: Optional component or string name ('DepressionFinderAndRouter', 'LakeMapperBarnes') to handle depressions.
    *   **Key Output Fields:**
        *   `drainage_area`: Drainage area at each node.
        *   `surface_water__discharge`: Water discharge at each node.
        *   `flow__upstream_node_order`: Downstream-to-upstream ordered node IDs (the drainage stack).
        *   (Plus fields created by the internal `FlowDirector`)
    *   **Core Method:** `run_one_step()`
    *   **Example:**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import FlowAccumulator

        grid = RasterModelGrid((5, 5), xy_spacing=10.0)
        z = grid.add_field("topographic__elevation", grid.x_of_node, at="node")
        grid.set_closed_boundaries_at_grid_edges(True, True, True, False) # Outlet at node 0

        fa = FlowAccumulator(grid, flow_director='D8')
        fa.run_one_step()

        print(grid.at_node['drainage_area'].reshape(grid.shape))
        # Output shows accumulated area flowing towards the outlet
        ```

*   **`LossyFlowAccumulator`:** Similar to `FlowAccumulator`, but allows for discharge to be lost or gained along flow paths via a user-defined function.

    *   **Purpose:** Accumulate flow while allowing for transmission losses or gains (e.g., infiltration, evaporation, channel seepage).
    *   **Key Parameters:** Same as `FlowAccumulator`, plus:
        *   `loss_function`: A Python function defining how discharge changes along a link (e.g., `f(Qw, nodeID, linkID, grid)`).
    *   **Key Output Fields:** Same as `FlowAccumulator`, plus:
        *   `surface_water__discharge_loss`: Discharge lost at each node.
    *   **Core Method:** `run_one_step()`
    *   **Example:**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import LossyFlowAccumulator

        grid = RasterModelGrid((3, 5), xy_spacing=10.0)
        z = grid.add_field("topographic__elevation", grid.x_of_node, at="node")
        grid.set_closed_boundaries_at_grid_edges(True, True, True, False)

        # Loss function: lose 10% per unit distance (dx=10)
        def loss_func(Qw, nodeID, linkID, grid):
            loss_fraction_per_m = 0.01 # 10% loss over 10m link
            distance = grid.length_of_link[linkID]
            return Qw * (1.0 - loss_fraction_per_m * distance)

        fa = LossyFlowAccumulator(grid, loss_function=loss_func, runoff_rate=1.0)
        fa.run_one_step()

        print(grid.at_node['surface_water__discharge'].reshape(grid.shape))
        # Output shows discharge decreasing downstream due to losses
        ```

##### PriorityFloodFlowRouter (`priority_flood_flow_router/`)

*   **`PriorityFloodFlowRouter`:** An alternative, highly efficient component for depression filling/breaching and flow routing on *raster grids only*, based on the RichDEM library (Barnes et al., 2016, 2017). It combines depression handling, flow directing, and accumulation.

    *   **Purpose:** Efficiently handle depressions (fill or breach) and route flow on large raster grids.
    *   **Key Parameters:**
        *   `grid`: Raster model grid.
        *   `surface`: Topographic field name or array.
        *   `flow_metric`: RichDEM flow metric ('D8', 'Rho8', 'Quinn', 'Freeman', 'Holmgren', 'Dinf').
        *   `depression_handler`: Method to handle depressions ('fill' or 'breach').
        *   `separate_hill_flow`: Boolean to calculate a secondary set of flow metrics (often for hillslope processes).
    *   **Key Output Fields:** Similar to `FlowAccumulator`, plus:
        *   `depression_free_elevation`: Topography after filling/breaching.
        *   (Optional secondary 'hill_*' fields if `separate_hill_flow` is True)
    *   **Core Method:** `run_one_step()`
    *   **Example:**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import PriorityFloodFlowRouter
        import numpy as np

        grid = RasterModelGrid((5, 5), xy_spacing=10.0)
        z = grid.add_field("topographic__elevation", grid.x_of_node + grid.y_of_node, at="node")
        # Create a depression
        z[grid.core_nodes] -= 5
        z[12] -= 5 # Deepest point
        grid.set_closed_boundaries_at_grid_edges(True, True, True, False) # Outlet at node 0

        pfr = PriorityFloodFlowRouter(grid, depression_handler='fill', flow_metric='D8')
        pfr.run_one_step()

        # Check the filled elevation
        print(grid.at_node['depression_free_elevation'][12]) # should be higher than original z[12]
        # Check drainage area
        print(grid.at_node['drainage_area'].max()) # Should drain entire grid (minus boundaries)
        ```

##### PotentialityFlowRouter (`potentiality_flowrouting/`)

*   **`PotentialityFlowRouter`:** Routes flow based on a potential field method (Voller, Hobley, Paola), solving for a potential field that conserves mass and ensures downhill flow. Does not return connectivity information. *Note: Marked as research-grade.*

    *   **Purpose:** Route flow using a potential field method, suitable for modeling diffusive surface processes like overland flow or sediment transport on fans.
    *   **Key Parameters:**
        *   `grid`: The model grid.
        *   `flow_equation`: 'default' (slope-based), 'Manning', or 'Chezy'.
    *   **Key Output Fields:**
        *   `flow__potential`: The calculated potential field.
        *   `surface_water__discharge`: Outgoing discharge at nodes.
        *   `surface_water__depth` (if `flow_equation` is not 'default').
    *   **Core Method:** `run_one_step()`
    *   **Example:**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import PotentialityFlowRouter

        grid = RasterModelGrid((5, 5), xy_spacing=10.0)
        z = grid.add_field("topographic__elevation", grid.x_of_node, at="node")
        qin = grid.add_ones("water__unit_flux_in", at="node")
        grid.set_closed_boundaries_at_grid_edges(True, True, True, False) # Outlet at node 0

        pfr = PotentialityFlowRouter(grid)
        pfr.run_one_step()

        print(grid.at_node['flow__potential'].reshape(grid.shape))
        # Output shows the potential field decreasing towards the outlet
        ```

#### Depression Handling Components

These components specifically deal with topographic depressions (sinks or pits). They are often used in conjunction with flow routers.

##### DepressionFinderAndRouter (`depression_finder/`)

*   **`DepressionFinderAndRouter`:** Identifies depressions and finds outlets, modifying flow directions and accumulations (calculated by a `FlowAccumulator` or `FlowDirector`) to route flow across them.

    *   **Purpose:** Locate and route flow across topographic depressions.
    *   **Key Parameters:**
        *   `grid`: The model grid.
        *   `routing`: 'D8' or 'D4' (for rasters) to determine connectivity.
        *   `reroute_flow`: Boolean (default True) to modify existing flow fields (`flow__receiver_node`, etc.).
    *   **Key Output Fields:**
        *   `depression__depth`: Depth of depression below its spill point.
        *   `depression__outlet_node`: ID of the node where the depression spills.
        *   `flood_status_code`: Integer code indicating node status (flooded, pit, etc.).
    *   **Core Method:** `map_depressions()` (aliased as `run_one_step()`)
    *   **Example:** (See `FlowAccumulator` example for usage with depression finding enabled)
        ```python
        from landlab import RasterModelGrid
        from landlab.components import FlowAccumulator, DepressionFinderAndRouter

        grid = RasterModelGrid((5, 5))
        z = grid.add_field("topographic__elevation", grid.x_of_node + grid.y_of_node, at="node")
        # Create a depression
        z[grid.core_nodes] -= 5
        z[12] -= 5 # Deepest point
        grid.set_closed_boundaries_at_grid_edges(True, True, True, False)

        # Run FlowAccumulator first (it will get stuck)
        fa = FlowAccumulator(grid)
        fa.run_one_step()
        print("Sinks before:", grid.at_node['flow__sink_flag'][grid.core_nodes].sum())

        # Now run the DepressionFinder
        df = DepressionFinderAndRouter(grid)
        df.run_one_step() # or map_depressions()

        # Re-run FlowAccumulator (or not, as df modified the fields if reroute_flow=True)
        fa.accumulate_flow(update_flow_director=False) # Use existing directions
        print("Sinks after:", grid.at_node['flow__sink_flag'][grid.core_nodes].sum())
        ```

##### SinkFiller / SinkFillerBarnes (`sink_fill/`, `lake_fill/`)

*   **`SinkFiller` / `SinkFillerBarnes`:** Fills depressions in the topography either to a flat surface or with a slight gradient towards the outlet. `SinkFillerBarnes` uses the more efficient Barnes et al. (2014) algorithm. These are typically used for *preprocessing* topography, not for dynamic lake filling during a run (use `LakeMapperBarnes` for that, which is the same underlying component but exposed via `depression_finder` argument in `FlowAccumulator`).

    *   **Purpose:** Preprocess a DEM to remove depressions by filling them.
    *   **Key Parameters:**
        *   `grid`: The model grid.
        *   `surface`: Field name or array for the topography to fill.
        *   `apply_slope`/`fill_flat`: Boolean to control whether the filled surface is flat or slightly sloped.
    *   **Key Output Fields:**
        *   `sediment_fill__depth`: The depth of fill added at each node.
        *   Modifies the input `topographic__elevation` field in place.
    *   **Core Method:** `run_one_step()` (or `fill_pits()`)
    *   **Example:**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import SinkFillerBarnes
        import numpy as np

        grid = RasterModelGrid((5, 5))
        z = grid.add_field("topographic__elevation", grid.x_of_node + grid.y_of_node, at="node")
        z_original = z.copy()
        # Create a depression
        z[grid.core_nodes] -= 5
        z[12] -= 5 # Deepest point
        grid.set_closed_boundaries_at_grid_edges(True, True, True, False)

        sf = SinkFillerBarnes(grid, fill_flat=True)
        sf.run_one_step()

        print("Original elevation at pit:", z_original[12])
        print("Filled elevation at pit:", z[12])
        print("Fill depth at pit:", grid.at_node['sediment_fill__depth'][12])
        ```

#### Surface Process Components (Erosion, Deposition, Transport)

These components modify the `topographic__elevation` field (and often related fields like `soil__depth` and `bedrock__elevation`) based on rules for erosion, transport, and deposition. They typically require flow information (area, discharge, slope) from a flow routing component.

##### Linear Diffusion (`diffusion/`)

*   **`LinearDiffuser`:** Simulates 2D linear hillslope diffusion, where sediment flux is proportional to the topographic gradient.

    *   **Purpose:** Model hillslope creep and soil transport under a linear diffusion law (flux ~ -K * slope).
    *   **Key Parameters:**
        *   `grid`: The model grid.
        *   `linear_diffusivity`: The diffusion coefficient *K* (can be float, array, or field name).
    *   **Key Input Fields:** `topographic__elevation`.
    *   **Key Output Fields:** Modifies `topographic__elevation`, `hillslope_sediment__unit_volume_flux` (at links), `topographic__gradient` (at links).
    *   **Core Method:** `run_one_step(dt)`
    *   **Example:**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import LinearDiffuser
        import numpy as np

        grid = RasterModelGrid((5, 5), xy_spacing=1.0)
        z = grid.add_zeros("topographic__elevation", at="node")
        # Create a central bump
        z[12] = 1.0
        grid.set_closed_boundaries_at_grid_edges(True, True, True, True)

        ld = LinearDiffuser(grid, linear_diffusivity=0.1)
        ld.run_one_step(dt=1.0)

        print("Max elevation after diffusion:", z.max()) # Should be slightly less than 1.0
        ```

##### Depth-Dependent Diffusion (`depth_dependent_diffusion/`, `depth_dependent_taylor_soil_creep/`)

*   **`DepthDependentDiffuser` / `DepthDependentTaylorDiffuser`:** Implement hillslope diffusion where the diffusivity depends on soil depth, often decreasing as soil thins. The Taylor version uses a more complex, potentially more stable numerical scheme. These often work in conjunction with a weathering component that produces soil.

    *   **Purpose:** Model hillslope soil transport where the efficiency depends on the soil thickness.
    *   **Key Parameters:**
        *   `grid`: The model grid.
        *   `linear_diffusivity` / `soil_transport_velocity`: Coefficient controlling transport rate.
        *   `soil_transport_decay_depth`: Characteristic depth scale over which transport efficiency changes.
        *   (Taylor version has additional stability parameters).
    *   **Key Input Fields:** `topographic__elevation`, `soil__depth`, `soil_production__rate`.
    *   **Key Output Fields:** Modifies `topographic__elevation`, `soil__depth`, `bedrock__elevation`, `soil__flux` (at links).
    *   **Core Method:** `run_one_step(dt)`
    *   **Example:**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import DepthDependentDiffuser, ExponentialWeatherer
        import numpy as np

        grid = RasterModelGrid((5, 5), xy_spacing=1.0)
        z = grid.add_zeros("topographic__elevation", at="node")
        br = grid.add_zeros("bedrock__elevation", at="node")
        soil = grid.add_zeros("soil__depth", at="node")
        soil[:] = 1.0 # Initial soil depth
        z[:] = br + soil
        grid.add_zeros("soil_production__rate", at="node") # Needed by diffuser
        grid.set_closed_boundaries_at_grid_edges(True, True, True, True)
        z[12] = 3.0 # Create a bump

        dd_diff = DepthDependentDiffuser(grid, linear_diffusivity=0.1, soil_transport_decay_depth=0.5)
        dd_diff.run_one_step(dt=1.0)

        print("Max elevation after diffusion:", z.max()) # Should be slightly less than 3.0
        print("Soil depth at center:", soil[12]) # Soil depth might change slightly
        ```

##### Nonlinear Diffusion (`nonlinear_diffusion/`, `taylor_nonlinear_hillslope_flux/`, `transport_length_diffusion/`)

*   **`PerronNLDiffuse`:** Implements nonlinear hillslope diffusion based on Perron (2011), where flux depends nonlinearly on slope, often approaching a maximum at a critical slope (`S_crit`). *Note: Marked as having potential stability issues.*
*   **`TaylorNonLinearDiffuser`:** Implements nonlinear hillslope diffusion using a Taylor series expansion approach (Ganti et al., 2012), similar in concept to `PerronNLDiffuse`.
*   **`TransportLengthHillslopeDiffuser`:** Implements hillslope diffusion based on a transport length concept (Carretier et al., 2016; Davy & Lague, 2009), where erosion rate depends on slope and deposition depends on incoming flux and slope relative to a critical slope.

    *   **Purpose:** Model hillslope transport where the flux is a nonlinear function of slope, often representing processes that become less efficient or saturate at high slopes.
    *   **Key Parameters:**
        *   `grid`: The model grid.
        *   `linear_diffusivity` / `nonlinear_diffusivity` / `erodibility`: Coefficient controlling transport/erosion rate.
        *   `slope_crit` / `S_crit`: Critical slope parameter.
        *   (Specific parameters vary by component).
    *   **Key Input Fields:** `topographic__elevation`, flow direction fields (for `TransportLengthHillslopeDiffuser`).
    *   **Key Output Fields:** Modifies `topographic__elevation`, often calculates `soil__flux` (at links) or related fields.
    *   **Core Method:** `run_one_step(dt)`
    *   **Example (TaylorNonLinearDiffuser):**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import TaylorNonLinearDiffuser
        import numpy as np

        grid = RasterModelGrid((5, 5), xy_spacing=1.0)
        z = grid.add_zeros("topographic__elevation", at="node")
        # Create a parabolic hill
        center_x, center_y = 2.0, 2.0
        z[:] = 5.0 - ((grid.x_of_node - center_x)**2 + (grid.y_of_node - center_y)**2) * 0.5
        grid.set_closed_boundaries_at_grid_edges(True, True, True, True)

        nl_diff = TaylorNonLinearDiffuser(grid, linear_diffusivity=0.1, slope_crit=0.8)
        nl_diff.run_one_step(dt=1.0)

        print("Max elevation after diffusion:", z.max()) # Should be slightly lower
        ```

##### Stream Power Components (`stream_power/`)

These components model channel incision based on the stream power law (E ~ K A^m S^n) or variations thereof. They typically require drainage area and slope from a flow router.

*   **`StreamPowerEroder`:** Basic implementation of the stream power law with an optional erosion threshold. Uses an implicit numerical scheme (based on FastscapeEroder).
*   **`FastscapeEroder`:** Highly efficient implementation of the stream power law using the implicit Fastscape algorithm (Braun & Willett, 2013). Does *not* support a threshold.
*   **`StreamPowerSmoothThresholdEroder`:** Implements stream power erosion with a mathematically smooth threshold function, avoiding numerical issues associated with abrupt thresholds.
*   **`SedDepEroder`:** Implements sediment-flux-dependent incision, where erosion rate is modulated by the ratio of sediment supply (Qs) to transport capacity (Qc), following models like those of Davy & Lague (2009) or Hobley et al. (2011). Can use either power-law or Meyer-Peter Muller based formulations for transport capacity.

    *   **Purpose:** Model channel incision based on stream power or related concepts, potentially including thresholds and sediment effects.
    *   **Key Parameters:**
        *   `grid`: The model grid.
        *   `K_sp` / `K_sed` / `K_br`: Erodibility coefficient(s).
        *   `m_sp`, `n_sp`: Exponents on area/discharge and slope.
        *   `threshold_sp` / `sp_crit_sed` / `sp_crit_br`: Erosion threshold(s).
        *   (Specific parameters vary by component, e.g., `SedDepEroder` has parameters for sediment flux function shape and transport capacity calculation).
    *   **Key Input Fields:** `topographic__elevation`, `drainage_area` (or `surface_water__discharge`), flow direction fields.
    *   **Key Output Fields:** Modifies `topographic__elevation`. `SedDepEroder` also calculates sediment flux fields.
    *   **Core Method:** `run_one_step(dt)`
    *   **Example (FastscapeEroder):**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import FlowAccumulator, FastscapeEroder
        import numpy as np

        grid = RasterModelGrid((5, 5), xy_spacing=100.0)
        z = grid.add_zeros("topographic__elevation", at="node")
        z[:] = grid.x_of_node * 0.1 # Initial slope
        grid.set_closed_boundaries_at_grid_edges(True, True, True, False) # Outlet at node 0

        fa = FlowAccumulator(grid, flow_director='D8')
        fs = FastscapeEroder(grid, K_sp=0.001, m_sp=0.5, n_sp=1.0)

        dt = 1000.0
        for _ in range(10):
            fa.run_one_step()
            fs.run_one_step(dt=dt)
            z[grid.core_nodes] += 0.01 * dt # Uplift core nodes

        print(z.reshape(grid.shape)) # Shows channel incision
        ```

##### SPACE Components (`space/`)

*   **`Space` / `SpaceLargeScaleEroder`:** Implements the Stream Power with Alluvium Conservation and Entrainment (SPACE) model (Shobe et al., 2017). This model explicitly tracks both bedrock erosion and the erosion/deposition of a sediment layer (alluvium) based on sediment supply and transport capacity. The `SpaceLargeScaleEroder` is a version optimized for larger timesteps and better mass conservation.

    *   **Purpose:** Model coupled bedrock incision and sediment transport/deposition in channels, explicitly tracking soil/alluvium thickness.
    *   **Key Parameters:**
        *   `grid`: The model grid.
        *   `K_sed`, `K_br`: Erodibility coefficients for sediment and bedrock.
        *   `F_f`: Fraction of fines produced from bedrock erosion.
        *   `phi`: Sediment porosity.
        *   `H_star`: Characteristic sediment thickness for erosion scaling.
        *   `v_s`: Effective sediment settling velocity.
        *   `m_sp`, `n_sp`: Stream power exponents.
        *   `sp_crit_sed`, `sp_crit_br`: Critical stream power thresholds for sediment and bedrock.
    *   **Key Input Fields:** `topographic__elevation`, `soil__depth`, `drainage_area` (or `surface_water__discharge`), flow direction fields.
    *   **Key Output Fields:** Modifies `topographic__elevation`, `soil__depth`, `bedrock__elevation`. Calculates `sediment__flux`, `sediment__influx`, `sediment__outflux`, `sediment__erosion_flux`, `sediment__deposition_flux`, `bedrock__erosion_flux`.
    *   **Core Method:** `run_one_step(dt)`
    *   **Example:**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import FlowAccumulator, SpaceLargeScaleEroder
        import numpy as np

        grid = RasterModelGrid((5, 5), xy_spacing=100.0)
        z = grid.add_field("topographic__elevation", grid.x_of_node * 0.1 + 10.0, at="node")
        soil = grid.add_zeros("soil__depth", at="node")
        soil[:] = 1.0 # Start with 1m soil
        br = grid.add_field("bedrock__elevation", z - soil, at="node")
        grid.set_closed_boundaries_at_grid_edges(True, True, True, False)

        fa = FlowAccumulator(grid, flow_director='D8')
        space = SpaceLargeScaleEroder(grid, K_sed=0.01, K_br=0.001, v_s=0.1, H_star=0.5)

        dt = 100.0
        for _ in range(10):
            fa.run_one_step()
            space.run_one_step(dt=dt)
            br[grid.core_nodes] -= 0.001 * dt # Uplift bedrock

        print("Final Topography:\n", z.reshape(grid.shape))
        print("Final Soil Depth:\n", soil.reshape(grid.shape))
        ```

##### Other Transport/Erosion Components

*   **`AreaSlopeTransporter` (`area_slope_transporter/`):** A simplified transport-limited model where sediment flux is a power-law function of drainage area and slope (Qs ~ K A^m S^n). Does not explicitly model bedrock erosion.
*   **`DischargeDiffuser` (`discharge_diffuser/`):** Experimental component simulating sediment diffusion where diffusivity is proportional to local water discharge, based on Voller et al. *Note: Marked as research-grade.*
*   **`ErosionDeposition` (`erosion_deposition/`):** Base class implementing the Davy & Lague (2009) style erosion-deposition framework, where erosion rate depends on stream power and is modulated by sediment flux relative to capacity (similar conceptual basis to SPACE, but often simpler implementation).
*   **`GravelBedrockEroder` (`gravel_bedrock_eroder/`):** Models bedrock incision and gravel transport/abrasion, assuming gravel-bedded channels where width adjusts to maintain near-threshold shear stress (Wickert & Schildgen, 2019). Includes both plucking and abrasion of bedrock.
*   **`GravelRiverTransporter` (`gravel_river_transporter/`):** Models transport-limited gravel transport with abrasion, using the Wickert & Schildgen (2019) transport law. Similar to `GravelBedrockEroder` but without the bedrock erosion component.
*   **`LateralEroder` (`lateral_erosion/`):** Simulates lateral channel migration and bank erosion based on local channel curvature and stream power (Langston & Tucker, 2018). Can use undercutting-slump or total-block-erosion mechanisms.
*   **`NetworkSedimentTransporter` (`network_sediment_transporter/`):** A Lagrangian model that transports discrete sediment parcels through a river network. Tracks parcel size, location, volume, etc. Includes helper classes (`BedParcelInitializer*`, `SedimentPulser*`) for setting up initial bed conditions and introducing sediment pulses.
*   **`SimpleSubmarineDiffuser` (`marine_sediment_transport/`):** Models marine sediment transport as a diffusion process where diffusivity depends on water depth, wave base, and tidal range.
*   **`ThresholdEroder` (`threshold_eroder/`):** A simple erosion component where slopes above a critical threshold are instantaneously cut back to that threshold, assuming material dissolves or is removed.

    *   **Purpose, Parameters, Fields, Methods:** Vary significantly. Refer to individual component docstrings for details.
    *   **Example (AreaSlopeTransporter):**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import FlowAccumulator, AreaSlopeTransporter

        grid = RasterModelGrid((5, 5), xy_spacing=100.0)
        z = grid.add_field("topographic__elevation", grid.x_of_node * 0.1, at="node")
        grid.set_closed_boundaries_at_grid_edges(True, True, True, False)

        fa = FlowAccumulator(grid)
        ast = AreaSlopeTransporter(grid, transport_coefficient=0.01, area_exponent=1.0, slope_exponent=1.0)

        dt = 1000.0
        for _ in range(10):
            fa.run_one_step()
            ast.run_one_step(dt=dt)
            z[grid.core_nodes] += 0.01 * dt # Add material to transport

        print(z.reshape(grid.shape)) # Shows transport and deposition
        ```

#### Mass Wasting Components

These components simulate slope failures and the subsequent runout of material.

*   **`BedrockLandslider` (`bedrock_landslider/`):** Simulates episodic bedrock landsliding based on the Culmann criterion (local slope compared to a critical angle defined by cohesion and friction angle). Includes runout calculation.
*   **`LandslideProbability` (`landslides/`):** Calculates the probability of failure at each node based on the infinite slope stability model, considering topographic slope, soil properties, and groundwater recharge (often simulated stochastically).
*   **`MassWastingRunout` (`mass_wasting_runout/`):** A cellular automata model that routes an initial mass wasting body (defined by `mass__wasting_id` field) across the landscape, calculating erosion and deposition depths and tracking regolith attributes.

    *   **Purpose, Parameters, Fields, Methods:** Vary significantly. Refer to individual component docstrings for details.
    *   **Example (BedrockLandslider):**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import PriorityFloodFlowRouter, BedrockLandslider
        import numpy as np

        grid = RasterModelGrid((5, 5), xy_spacing=1.0)
        z = grid.add_zeros("topographic__elevation", at="node")
        soil = grid.add_zeros("soil__depth", at="node")
        bedrock = grid.add_zeros("bedrock__elevation", at="node")
        bedrock[:] = 10.0 # Plateau
        bedrock[grid.nodes_at_left_edge] = 0.0 # Create a scarp
        z[:] = bedrock + soil
        grid.set_status_at_node_on_edges(
            right=4, top=4, left=1, bottom=4 # Outlet at left edge
        )

        pfr = PriorityFloodFlowRouter(grid, separate_hill_flow=True, suppress_out=True)
        bl = BedrockLandslider(grid, landslides_return_time=1.0) # Force slide

        pfr.run_one_step()
        bl.run_one_step(dt=1.0)

        print("Elevation after landslide:\n", z.reshape(grid.shape))
        # Output shows modified topography due to landslide
        ```

#### Hydrology Components

These components simulate aspects of the hydrological cycle beyond basic flow routing.

*   **`GroundwaterDupuitPercolator` (`groundwater/`):** Simulates shallow, unconfined groundwater flow using the Dupuit-Forcheimer approximation (Boussinesq equation). Calculates water table elevation and groundwater discharge.
*   **`OverlandFlow` / `OverlandFlowBates` / `KinwaveImplicitOverlandFlow` / `KinwaveOverlandFlowModel` / `KinematicWaveRengers` / `LinearDiffusionOverlandFlowRouter` (`overland_flow/`):** A suite of components for simulating overland flow (sheet flow) using various approximations of the shallow water equations (e.g., kinematic wave, diffusion wave, different numerical schemes like Bates et al. (2010) or de Almeida et al. (2012)). Calculate water depth and discharge.
*   **`SoilInfiltrationGreenAmpt` (`soil_moisture/`):** Calculates infiltration of surface water into the soil using the Green-Ampt method. Updates `soil_water_infiltration__depth` and modifies `surface_water__depth`.
*   **`SoilMoisture` (`soil_moisture/`):** Simulates root-zone average soil moisture based on potential evapotranspiration (PET), leaf area index (LAI), vegetation cover, and rainfall. Calculates actual evapotranspiration (AET), runoff, leakage, and vegetation water stress based on the Laio et al. (2001) framework.

    *   **Purpose, Parameters, Fields, Methods:** Vary significantly. Refer to individual component docstrings for details.
    *   **Example (GroundwaterDupuitPercolator):**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import GroundwaterDupuitPercolator
        import numpy as np

        grid = RasterModelGrid((5, 5), xy_spacing=10.0)
        z = grid.add_field("topographic__elevation", grid.x_of_node * 0.01 + 10, at="node")
        base = grid.add_field("aquifer_base__elevation", grid.x_of_node * 0.01, at="node")
        wt = grid.add_field("water_table__elevation", z.copy(), at="node") # Start saturated
        grid.set_closed_boundaries_at_grid_edges(True, True, True, False) # Outlet at node 0

        gdp = GroundwaterDupuitPercolator(grid, hydraulic_conductivity=0.01, porosity=0.2, recharge_rate=1e-7)

        dt = 1000.0 # seconds
        for _ in range(10):
            gdp.run_one_step(dt)

        print("Water table elevation:\n", wt.reshape(grid.shape))
        # Output shows water table dropping due to drainage
        ```

#### Vegetation Dynamics Components

These components simulate the growth, competition, and mortality of plants.

*   **`Vegetation` (`vegetation_dynamics/`):** Simulates net primary productivity (NPP), biomass (live and dead), and leaf area index (LAI) based on inputs like soil moisture (via water stress) and potential evapotranspiration (PET). Based on Zhou et al. (2013).
*   **`VegCA` (`plant_competition_ca/`):** A cellular automata model simulating spatial competition between different plant functional types (e.g., grass, shrub, tree) based on establishment rules, mortality factors (drought, age, background), and potentially allelopathic effects. Based on CATGraSS (Zhou et al., 2013).

    *   **Purpose, Parameters, Fields, Methods:** Vary significantly. Refer to individual component docstrings for details.
    *   **Example (Vegetation):**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import Vegetation
        import numpy as np

        grid = RasterModelGrid((5, 5), xy_spacing=100.0)
        # Add required input fields (often from other components like SoilMoisture, PET)
        grid.add_field("vegetation__plant_functional_type", np.zeros(grid.number_of_cells, dtype=int), at="cell") # All grass
        grid.add_field("surface__evapotranspiration", np.full(grid.number_of_cells, 0.1), at="cell")
        grid.add_field("surface__potential_evapotranspiration_rate", np.full(grid.number_of_cells, 0.5), at="cell")
        grid.add_field("surface__potential_evapotranspiration_30day_mean", np.full(grid.number_of_cells, 0.5), at="cell")
        grid.add_field("vegetation__water_stress", np.zeros(grid.number_of_cells), at="cell")

        veg = Vegetation(grid, Blive_init=10.0, Bdead_init=10.0) # Low initial biomass
        veg.run_one_step() # dt defaults implicitly to 1 day

        print("Live Biomass:\n", grid.at_cell['vegetation__live_biomass'].reshape((3,3)))
        # Output should show slightly increased biomass due to growth
        ```

#### Tectonics and Lithosphere Components

These components simulate tectonic processes like faulting, flexure, and manage subsurface lithology.

*   **`Flexure` / `Flexure1D` (`flexure/`, `gflex/`):** Models lithospheric flexure in 2D or 1D in response to surface loads (e.g., sediment, ice). Calculates vertical deflection. `gFlex` is a wrapper for the external gFlex library (Wickert, 2016), while `Flexure` and `Flexure1D` are native Landlab implementations.
*   **`NormalFault` (`normal_fault/`):** Simulates relative rock motion along a normal fault defined by a trace and dip angle. Can be driven by a specified throw rate history or by discrete earthquake events. Modifies specified surface(s).
*   **`ListricKinematicExtender` (`tectonics/`):** Simulates kinematic extension along a listric (curved) normal fault, advecting material horizontally and vertically. Tracks `hangingwall__thickness`.
*   **`Lithology` / `LithoLayers` (`lithology/`):** Manage subsurface stratigraphy and spatially variable rock properties. `Lithology` is the base class, allowing definition of layers with specific thicknesses, IDs, and attributes (e.g., erodibility). `LithoLayers` provides a convenient way to define parallel layers with potentially complex geometries (e.g., dipping, folded) based on a reference surface function. Updates surface properties based on erosion/deposition exposing different layers.

    *   **Purpose, Parameters, Fields, Methods:** Vary significantly. Refer to individual component docstrings for details.
    *   **Example (Lithology):**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import Lithology
        import numpy as np

        grid = RasterModelGrid((5, 5))
        z = grid.add_zeros("topographic__elevation", at="node")

        # Define layers: top layer (1m, type 1), middle (2m, type 2), bottom (3m, type 1)
        thicknesses = [1.0, 2.0, 3.0]
        ids = [1, 2, 1]
        attrs = {"K_sp": {1: 0.01, 2: 0.001}} # Erodibility for each type

        lith = Lithology(grid, thicknesses, ids, attrs)

        # Initial surface K should be for type 1
        print("Initial K:", grid.at_node['K_sp'][grid.core_nodes[0]])

        # Simulate erosion
        z[:] -= 1.5 # Erode 1.5m

        lith.run_one_step() # Update lithology based on new elevation

        # Surface K should now be for type 2
        print("K after erosion:", grid.at_node['K_sp'][grid.core_nodes[0]])
        ```

#### Utility and Analysis Components

These components perform calculations based on grid properties or other component outputs, often for analysis or input to other components.

*   **`AdvectionSolverTVD` (`advection/`):** Solves the advection equation numerically using a Total Variation Diminishing (TVD) scheme. Used internally by `ListricKinematicExtender` but potentially useful for other advection problems.
*   **`ChannelProfiler` / `Profiler` / `TrickleDownProfiler` (`profiler/`):** Extract profiles along channel networks (`ChannelProfiler`), user-defined paths (`Profiler`), or downstream from specified points (`TrickleDownProfiler`). Store node IDs and distances along profiles.
*   **`ChiFinder` (`chi_index/`):** Calculates the chi index (χ), an integral metric related to drainage area and concavity, often used in channel profile analysis (Perron & Royden, 2013).
*   **`ConcentrationTrackerForDiffusion` / `ConcentrationTrackerForSpace` (`concentration_tracker/`):** Track the concentration of a user-defined property (e.g., cosmogenic nuclides, pollutants) as it is transported by hillslope diffusion (`...ForDiffusion`) or fluvial processes modeled by SPACE (`...ForSpace`). Uses a mass balance approach. *Note: Requires specific coupling pattern (start_tracking/stop_tracking) instead of `run_one_step`.*
*   **`DimensionlessDischarge` (`dimensionless_discharge/`):** Calculates dimensionless discharge based on Tang et al. (2019), potentially useful for debris flow initiation prediction.
*   **`DrainageDensity` (`drainage_density/`):** Calculates drainage density based on the distance-to-channel method (Tucker et al., 2001), requiring a channel mask or a threshold definition.
*   **`FractureGridGenerator` (`fracture_grid/`):** Creates a 2D grid field (`fracture_at_node`) representing a network of randomly generated fractures (nodes marked 1 if fractured, 0 otherwise).
*   **`HackCalculator` (`hack_calculator/`):** Calculates Hack's law parameters (L = C A^h) relating channel length to drainage area for specified watersheds.
*   **`HeightAboveDrainageCalculator` (`hand_calculator/`):** Calculates the elevation difference between each node and its nearest downstream drainage node (HAND), based on Nobre et al. (2011). Requires a channel mask.
*   **`PotentialEvapotranspiration` (`pet/`):** Calculates potential evapotranspiration (PET) using various methods ('Constant', 'PriestleyTaylor', 'MeasuredRadiationPT', 'Cosine') based on inputs like temperature, radiation, and latitude.
*   **`Radiation` (`radiation/`):** Calculates daily incident shortwave radiation, considering factors like latitude, time of year, topography (slope, aspect), and optional atmospheric parameters.
*   **`SpeciesEvolver` (`species_evolution/`):** A framework component for simulating the evolution, speciation, extinction, and dispersal of taxa across the landscape. Designed to work with user-defined `Taxon` subclasses (like the provided `ZoneTaxon`). Includes helper classes `Zone` and `ZoneController`.
*   **`SteepnessFinder` (`steepness_index/`):** Calculates channel steepness index (ksn), a metric often used in tectonic geomorphology, typically defined as ksn = S * A^(ref_theta). Allows for different discretization methods (Wobus et al., 2006).
*   **`TidalFlowCalculator` (`tidal_flow/`):** Calculates cycle-averaged tidal flow velocity fields using the method of Mariotti (2018), based on solving a diffusion equation for water surface elevation driven by tidal inundation/drainage rates.

    *   **Purpose, Parameters, Fields, Methods:** Very diverse. Refer to individual component docstrings for details.
    *   **Example (ChiFinder):**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import FlowAccumulator, ChiFinder
        import numpy as np

        grid = RasterModelGrid((5, 5), xy_spacing=100.0)
        z = grid.add_field("topographic__elevation", grid.x_of_node, at="node")
        grid.set_closed_boundaries_at_grid_edges(True, True, True, False)

        fa = FlowAccumulator(grid)
        fa.run_one_step()

        cf = ChiFinder(grid, min_drainage_area=10000.0, reference_concavity=0.5)
        cf.calculate_chi()

        print(grid.at_node['channel__chi_index'].reshape(grid.shape))
        # Output shows chi values calculated for channel nodes
        ```

#### Climate and Weathering Components

*   **`ExponentialWeatherer` / `ExponentialWeathererIntegrated` (`weathering/`):** Models bedrock weathering into soil using an exponential decay function where weathering rate decreases with increasing soil depth. The `Integrated` version uses an analytical solution for better accuracy over longer timesteps.
*   **`PrecipitationDistribution` (`uniform_precip/`):** Generates a time series of precipitation events (storm duration, interstorm duration, storm depth/intensity) based on Poisson distributions for timing and gamma distributions for depth (Eagleson, 1978). Produces spatially uniform rainfall for each event.
*   **`SpatialPrecipitationDistribution` (`spatial_precip/`):** Generates spatially resolved precipitation events following the stochastic methods of Singer & Michaelides (2017, 2018). Models storm duration, area, interarrival time, and intensity based on statistical distributions, often calibrated to specific climates (e.g., desert southwest monsoon default). Can include orographic effects.

    *   **Purpose, Parameters, Fields, Methods:** Vary. Refer to individual component docstrings for details.
    *   **Example (ExponentialWeatherer):**
        ```python
        from landlab import RasterModelGrid
        from landlab.components import ExponentialWeatherer
        import numpy as np

        grid = RasterModelGrid((5, 5))
        soil = grid.add_field("soil__depth", np.linspace(0, 2, grid.number_of_nodes), at="node")
        rate = grid.add_zeros("soil_production__rate", at="node")

        ew = ExponentialWeatherer(grid, soil_production_maximum_rate=0.001, soil_production_decay_depth=0.5)
        ew.run_one_step()

        print(rate) # Shows weathering rate decreasing with increasing soil depth
        ```

#### Specialized Components

*   **`CarbonateProducer` (`carbonate/`):** Calculates marine carbonate production and deposition based on water depth and light availability, following Bosscher & Schlager (1992). Updates `topographic__elevation` and `carbonate_thickness`.

---

This concludes the reference for components found in the `landlab/components` directory. For more details on specific parameters, methods, and underlying theory, consult the individual component documentation within Landlab. Remember that these components are designed to be combined to create sophisticated landscape evolution models.