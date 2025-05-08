Okay, here is a detailed section for the technical document based on the `landlab-docs-digest`. This section focuses on understanding Landlab through its documentation, tutorials, examples, and contribution guidelines.

```markdown
# Landlab Documentation, Tutorials, and Contribution Guide

This section provides a comprehensive guide to navigating and utilizing the Landlab documentation, tutorials, and examples. It also outlines the process for contributing to the Landlab project, based on the information contained within the project's documentation structure.

## 1. Overview of Landlab (Based on Documentation)

Landlab is an open-source Python package designed for numerical modeling of Earth surface dynamics. Key features highlighted in the documentation include:

*   **Gridding Engine:** Supports both regular (raster, hex) and irregular (Voronoi, network) grids to represent model domains.
*   **Component Library:** Offers a collection of pre-built process components (e.g., flow routing, erosion, diffusion) with standardized interfaces that can be combined to build custom models.
*   **Utilities:** Provides tools for numerical methods, file I/O, and visualization.
*   **Tutorials:** Includes Jupyter notebooks demonstrating core concepts and usage examples.

The primary goal is to save researchers time by providing reusable, standardized building blocks for landscape modeling, fostering a collaborative development environment.

**(Source: `README.md`, `docs/source/index.md`)**

## 2. Getting Started with Landlab

This part guides new users through installation and initial exploration.

### 2.1. Installation

Landlab can be installed using common Python package managers. It is **highly recommended** to install Landlab within a dedicated virtual environment to avoid dependency conflicts.

**Using Virtual Environments:**

*   **Mamba/Conda:**
    ```bash
    # Install mamba if needed: conda install mamba -c conda-forge
    mamba create -n landlab_env python=3.11 # Or desired Python version
    mamba activate landlab_env
    ```
*   **venv (built-in):**
    ```bash
    python -m venv .venv # Create environment in .venv directory
    source .venv/bin/activate # On Linux/macOS
    # .\venv\Scripts\activate # On Windows
    ```

**(Source: `docs/source/install/environments.md`)**

**Installation Methods:**

Once the environment is activated:

*   **Recommended (using Mamba/Conda):** Provides pre-compiled binaries for faster installation and better dependency management, especially for complex dependencies.
    ```bash
    # Using mamba (faster)
    mamba install landlab -c nodefaults -c conda-forge --override-channels

    # Using conda
    conda install landlab -c nodefaults -c conda-forge --override-channels
    ```

*   **Using pip:** Installs from the Python Package Index (PyPI).
    ```bash
    pip install landlab
    ```

**(Source: `README.md`, `docs/source/installation.md`)**

**Updating and Uninstalling:**

*   **Update:**
    ```bash
    # Conda/Mamba
    conda update landlab # or mamba update landlab

    # Pip
    pip install --upgrade landlab
    ```
*   **Uninstall:**
    ```bash
    # Conda/Mamba
    conda remove landlab # or mamba remove landlab

    # Pip
    pip uninstall landlab
    ```

**(Source: `docs/source/install/update_uninstall.md`)**

### 2.2. Developer Installation

If you plan to modify Landlab's code or contribute new features, install from the source code:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/landlab/landlab.git
    cd landlab
    ```
2.  **Create and Activate Environment:** Use Mamba/Conda or venv as described above. Use the provided environment files for convenience:
    ```bash
    # For Conda/Mamba (includes dev tools)
    mamba env create -f environment-dev.yml # Creates 'landlab_dev' env
    mamba activate landlab_dev

    # Or install dependencies manually if needed
    # mamba install --file=requirements.in --file=requirements-testing.in --file=requirements/dev.txt -c conda-forge
    ```
3.  **Install Dependencies (if not using environment file):**
    ```bash
    # using pip
    pip install -r requirements.in -r requirements-testing.in -r requirements/dev.txt

    # using mamba/conda (preferred for compiling extensions)
    mamba install --file=requirements.in --file=requirements-testing.in --file=requirements/dev.txt -c conda-forge
    ```
4.  **Build and Install Landlab (Editable Mode):** This requires a C++ compiler (install via `conda install compilers` or system tools like XCode/MSVC).
    ```bash
    pip install -e .
    ```
    The `-e` flag installs the package in "editable" mode, meaning changes you make to the source code are immediately reflected when you import Landlab in Python.

**(Source: `README.md`, `docs/source/install/developer_install.md`, `environment-dev.yml`, `requirements*.txt`)**

### 2.3. First Steps and Core Concepts

The documentation introduces key Landlab concepts:

*   **Model Grid:** The representation of the spatial domain. Grids contain elements like nodes, links, cells, faces, etc., with defined connectivity and geometry. Different grid types (Raster, Hex, Voronoi, Network, etc.) are available. *(See `docs/source/user_guide/grid.md`, `docs/source/user_guide/grid_summary.md`)*
*   **Fields:** Data arrays associated with specific grid elements (e.g., `topographic__elevation` at nodes). They are the primary way data is stored and shared. *(See `docs/source/user_guide/fields.md`, `docs/source/user_guide/field_definitions.md`)*
*   **Components:** Reusable modules representing specific physical processes (e.g., `FlowAccumulator`, `LinearDiffuser`). They interact with the grid and its fields. *(See `docs/source/user_guide/components.md`, `docs/source/user_guide/component_list.md`)*

**Building a Model:** A typical Landlab model involves writing a Python script (the "driver") that:
1.  Imports necessary libraries and Landlab classes (Grid, Components).
2.  Instantiates the grid.
3.  Instantiates required components, linking them to the grid.
4.  Initializes grid fields (e.g., topography).
5.  Sets boundary conditions on the grid.
6.  Runs the model, typically in a time loop, calling component `run_one_step()` methods.
7.  Processes or visualizes results.

**(Source: `docs/source/user_guide/build_a_model.md`)**

**Conceptual Driver Structure:**

```python
import numpy as np
from landlab import RasterModelGrid
from landlab.components import FlowAccumulator, FastscapeEroder # Example components

# 1. Import (already done)

# 2. Instantiate Grid
grid = RasterModelGrid((50, 50), xy_spacing=10.0)

# 3. Initialize Fields
z = grid.add_zeros("topographic__elevation", at="node")
z += np.random.rand(grid.number_of_nodes) * 0.1 # Example initial noise

# 4. Set Boundary Conditions
grid.set_closed_boundaries_at_grid_edges(True, True, True, False) # Example: open bottom

# 5. Instantiate Components
fa = FlowAccumulator(grid)
sp = FastscapeEroder(grid, K_sp=1e-5) # Example parameters

# 6. Run Model
dt = 1000.0 # years
run_duration = 50000.0 # years
uplift_rate = 0.001 # m/yr

current_time = 0.0
while current_time < run_duration:
    # Apply uplift
    z[grid.core_nodes] += uplift_rate * dt

    # Run components
    fa.run_one_step()
    sp.run_one_step(dt)

    current_time += dt

# 7. Finalize (e.g., plot)
from landlab.plot import imshow_grid
imshow_grid(grid, "topographic__elevation")
```

**(Source: Conceptual structure from `docs/source/user_guide/build_a_model.md`)**

## 3. Using Tutorials and Examples

Landlab provides extensive tutorials as Jupyter notebooks, typically found in the `landlab/notebooks` directory of the repository.

### 3.1. Accessing Notebooks

*   **`welcome.ipynb`:** The main entry point and index for tutorials (`landlab/notebooks/welcome.ipynb`).
*   **`tutorials/`:** Contains notebooks covering core Landlab concepts and component usage examples.
*   **`teaching/`:** Contains notebooks designed for classroom use (`landlab/notebooks/teaching/`).

**(Source: `README.md`, `docs/source/index.md`, `docs/source/tutorials/index.md`, `docs/source/teaching/index.md`, `notebooks/welcome.ipynb` content description)**

### 3.2. Running Notebooks

You can run the notebooks interactively:

*   **Binder:** Click the "launch binder" links in the main `README.md` or documentation for a cloud-based environment (no local installation needed).
*   **EarthscapeHub:** Use the provided links if you have access (requires login). Ensure you select the `CSDMS` kernel.
*   **Locally:**
    1.  Install Landlab (preferably developer install) and notebook dependencies:
        ```bash
        # If using conda/mamba from environment-dev.yml, dependencies are included.
        # Or install manually:
        pip install -r notebooks/requirements.in # Or use conda/mamba
        pip install jupyterlab # Or conda/mamba install jupyterlab
        ```
    2.  Navigate to the `landlab/notebooks` directory in your terminal.
    3.  Launch Jupyter Lab:
        ```bash
        jupyter lab
        ```
    4.  Open `welcome.ipynb` or other notebooks in your browser.

**(Source: `README.md`, `notebooks/requirements.in`, `environment-dev.yml`)**

### 3.3. Key Tutorial Topics (Examples)

The documentation highlights several key tutorial areas (specific notebook code is not in this digest, but their existence and topics are documented):

*   Introduction to Python/NumPy basics (`tutorials/python_intro/`)
*   Fault-scarp degradation model (`tutorials/fault_scarp/`)
*   Grid objects (`tutorials/grids/grid_object_demo.ipynb`)
*   Data fields (`tutorials/fields/`)
*   Plotting (`tutorials/plotting/`)
*   Using components (`tutorials/component_tutorial/`)
*   Gradient/Divergence functions (`tutorials/gradient_and_divergence/`)
*   Mapping between grid elements (`tutorials/mappers/`)
*   Setting boundary conditions (`tutorials/boundary_conditions/`)
*   Reading DEMs (`tutorials/reading_dem_into_landlab/`)
*   Making components (`tutorials/making_components/`)
*   Specific component examples (e.g., Flexure, OverlandFlow, Lithology, NetworkSedimentTransporter, etc.)

**(Source: `docs/source/tutorials/index.md`, `notebooks/welcome.ipynb` description)**

## 4. Navigating the User Guide and Reference

The online documentation ([https://landlab.csdms.io](https://landlab.csdms.io)) is generated from the files in `docs/source/`.

*   **User Guide:** Provides topic-based explanations (e.g., Grids, Components, Fields, Units, FAQ, Building a Model).
*   **API Reference:** Details the public functions, classes, and methods. It is largely auto-generated from code docstrings.
*   **Listings:** The documentation uses an `index.toml` file (`docs/index.toml`) to generate comprehensive lists of:
    *   Components (`docs/source/user_guide/component_list.md`)
    *   Standard Field Names and Definitions (`docs/source/user_guide/field_definitions.md`)
    *   Grid Methods Summarized by Category (`docs/source/user_guide/grid_summary.md` and `grid_methods/`)

**Example: Finding Component Information**
A user wanting to know about fluvial erosion components could navigate to the User Guide -> Component List, find relevant components like `FastscapeEroder` or `ErosionDeposition`, and then follow the links to the API Reference for detailed parameters and methods. They could also check the `field_definitions.md` page (powered by `index.toml`) to see which components *provide* or *use* specific fields like `topographic__elevation` or `sediment__flux`.

**(Source: `docs/source/user_guide/index.md`, `docs/source/index.md`, `docs/index.toml`, `docs/source/user_guide/*.md`, `docs/source/user_guide/grid_methods/*.md`)**

## 5. Contributing to Landlab

Landlab welcomes community contributions. The process is managed through GitHub.

### 5.1. Reporting Bugs

*   Check existing [GitHub Issues](https://github.com/landlab/landlab/issues) first.
*   If the bug is new, create a new issue.
*   Provide a clear title and description.
*   Include exact steps to reproduce the problem.
*   Provide a **Minimal, Reproducible Example** (MRE). This is crucial for efficient debugging.
*   Describe observed vs. expected behavior.
*   Include environment details (Landlab version, OS, Python version).

**(Source: `CONTRIBUTING.md`)**

### 5.2. Submitting Changes (Pull Requests)

1.  **Create an Issue:** Describe the proposed change or feature.
2.  **Fork the Repository:** Create your own copy of Landlab on GitHub.
3.  **Create a Branch:** Make changes on a dedicated feature branch (e.g., `git checkout -b fix-diffusion-bug`), *not* on your `master` branch.
4.  **Make Changes:** Implement your code edits, additions, tests, and documentation.
5.  **Commit Changes:** Use clear, imperative, present-tense commit messages (e.g., "Fix calculation in `run_one_step`"). Reference relevant issue numbers (e.g., "Fix #123: Correct boundary handling"). *(See `CONTRIBUTING.md` for suggested emoji prefixes)*.
6.  **Add a News Fragment:** For non-trivial changes, create a file in the `news/` directory named `ISSUE_NUMBER.TYPE.rst` (e.g., `1234.bugfix.rst`). Types include `component`, `notebook`, `feature`, `bugfix`, `docs`, `misc`. *(Source: `docs/source/development/contribution/index.md`)*.
7.  **Push Branch:** Push your feature branch to *your* fork on GitHub (`git push origin fix-diffusion-bug`).
8.  **Open a Pull Request (PR):** Go to the main [Landlab repository](https://github.com/landlab/landlab) and open a PR comparing the main repo's `master` branch with your feature branch.
9.  **Describe PR:** Clearly explain the problem and solution, linking the relevant issue.
10. **Pass Checks:** Automated checks (tests, linting) will run via Continuous Integration (CI). Address any failures by pushing further commits to your branch.

**(Source: `CONTRIBUTING.md`, `docs/source/development/practices/develop_with_git.md`, `docs/source/development/contribution/index.md`)**

### 5.3. Developing New Components

The documentation provides specific guidance for developing components:

*   **Structure:** Create a folder in `landlab/components/` containing your component's Python file (`my_component.py`) and an `__init__.py`.
*   **Inheritance:** Your component class must inherit from `landlab.Component`.
*   **Standard Interface:** Include the standard header info (`_name`, `_unit_agnostic`, `_info`), `__init__`, and `run_one_step` methods as described earlier.
*   **Testing:** Provide comprehensive unit tests (in `tests/components/my_component/`) and instructive doctests.
*   **Documentation:**
    *   Write clear docstrings following numpydoc conventions.
    *   Add an `.rst` file for your component in `docs/source/reference/components/`.
    *   Update `docs/source/reference/components/index.rst` to include your new component file.
*   **Conventions:** Follow recommended practices regarding parameters, units, and handling of inputs/outputs. *(See `docs/source/development/contribution/develop_a_component.md`, `docs/source/development/contribution/recommendations.md`)*.

**Conceptual Component File Structure (as described in docs):**

```
landlab/
└── components/
    └── my_component/
        ├── __init__.py
        └── my_component.py
tests/
└── components/
    └── my_component/
        └── test_my_component.py
docs/
└── source/
    └── reference/
        └── components/
            ├── my_component.rst
            └── index.rst  # Needs modification
```

**(Source: `docs/source/development/contribution/develop_a_component.md`)**

### 5.4. JOSS Publication Workflow

For contributors publishing Landlab components via the Journal of Open Source Software (JOSS), a specific workflow involving separate branches for the `paper.md` file is documented to avoid conflicts. *(Source: `docs/source/development/contribution/joss_workflow.md`)*.

## 6. Development Practices (as documented)

The documentation outlines key practices for Landlab development:

*   **Git Workflow:** Use feature branches, keep forks updated, use clear commit messages, and submit changes via Pull Requests. *(Source: `docs/source/development/practices/develop_with_git.md`)*.
*   **Continuous Integration (CI):** Automated testing runs on GitHub Actions (previously Travis/AppVeyor) for Linux, macOS, and Windows across supported Python versions. PRs must pass CI checks. *(Source: `docs/source/development/practices/continuous_integration.md`, `.github/workflows/*.yml` descriptions in `README.md`)*.
*   **Coding Style:** Follow PEP8 and numpydoc conventions. Use `flake8` for checking and tools like `black` and `isort` (run via `nox -s lint` or `make pretty`) for auto-formatting. *(Source: `docs/source/development/practices/style_conventions.md`, `setup.cfg`, `pyproject.toml`)*.
*   **Testing:** Write comprehensive doctests (for examples) and unit tests (using `pytest`) covering different scenarios and edge cases. Aim for high test coverage. *(Source: `docs/source/development/practices/writing_tests.md`)*.
*   **Dependencies:** Core dependencies are in `requirements.in` (derived from `pyproject.toml`). Development, testing, notebook, and docs dependencies are in separate files (`requirements-*.in`, `requirements/*.txt`). `environment*.yml` files provide convenient Conda environment setups. *(Source: `docs/source/development/practices/dependencies.md`, `requirements/`, `environment*.yml`, `pyproject.toml`)*.
*   **Releases:** Follow a specific workflow involving merging `master` to `release`, tagging, CI checks, PyPI/conda-forge uploads, and creating `-dev` tags. *(Source: `docs/source/development/practices/dev_guide_releases.md`)*.
*   **Package Organization:** The documentation (`docs/source/development/package_organization.md`) describes the standard directory structure.

## 7. About Landlab

*   **Citing Landlab:** Provides specific papers (Hobley et al., 2017; Barnhart et al., 2020) and a software DOI to cite. Also recommends citing individual component papers where relevant. Includes instructions for using the Landlab Citation Registry tool via the command line (`landlab citations`). *(Source: `docs/source/about/citing.md`, `CITATION.cff`)*.
*   **Contact:** Recommends using GitHub Issues for bugs and questions. Mentions Twitter and Slack (for workshops). *(Source: `docs/source/about/contact_us.md`, `README.md`)*.
*   **Funding:** Lists funding sources (primarily NSF). *(Source: `docs/source/about/funding.md`)*.
*   **Authors/Contributors:** Lists contributors. *(Source: `docs/source/about/authors.md`)*.
*   **License:** Uses the MIT License. *(Source: `docs/source/about/license.md`, `LICENSE.md`)*.
*   **Used By:** Provides a list of papers and presentations using Landlab. *(Source: `docs/source/about/usedby.md`)*.

## 8. Documentation Build System

The documentation is built using [Sphinx](https://www.sphinx-doc.org/) with extensions like `MyST-Parser` (for Markdown), `nbsphinx` (for Jupyter notebooks), `autodoc` (for API generation), `napoleon` (for NumPy/Google style docstrings), and `towncrier` (for changelogs). Configuration is primarily in `docs/source/conf.py`. The `Furo` theme is used for HTML output.

**(Source: `docs/source/conf.py`, `docs/requirements.in`, `Makefile`, `make.bat`)*
```


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