Title: Labs Landscape Evolution Modeling With Child Part 1 • CSDMS: Community Surface Dynamics Modeling System. Explore Earth's surface with community software

URL Source: https://csdms.colorado.edu/wiki/Labs_Landscape_Evolution_Modeling_With_Child_Part_1

Published Time: 2025-05-06T21:57:36Z

Markdown Content:
From CSDMS

Jump to:[navigation](https://csdms.colorado.edu/wiki/Labs_Landscape_Evolution_Modeling_With_Child_Part_1#mw-navigation), [search](https://csdms.colorado.edu/wiki/Labs_Landscape_Evolution_Modeling_With_Child_Part_1#p-search)

Landscape Evolution Modeling with CHILD
---------------------------------------

If you have never used the Web Modeling Tool, learn how to use it [here](https://csdms.colorado.edu/wiki/WMT_tutorial "WMT tutorial"). You will need an account on the CSDMS supercomputer to submit your jobs. More information on getting an account can be found here [Beach HPCC Access](https://csdms.colorado.edu/wiki/HPCC_Access "HPCC Access")

Before beginning these exercises, please download the CHILD visualization tools here: [File:CHILDVisTools.tar.gz](https://csdms.colorado.edu/wiki/File:CHILDVisTools.tar.gz "File:CHILDVisTools.tar.gz").

Overview
--------

The learning goals of these exercises are:

*   To appreciate that working with landscape Evolution Models, LEMs, involves choosing a level of simplification in the governing physics that is appropriate to the problem at hand.
*   To get a sense for how and why soil creep produces convex hillslopes.
*   To appreciate the concepts of transient versus steady topography.
*   To acquire a feel for the similarity and difference between detachment-limited and transport-limited modes of fluvial erosion.
*   To understand the connection between fluvial physics and slope-area plots.
*   To appreciate that LEMs (1) are able to reproduce (and therefore, at least potentially, explain) common forms in fluvially carved landscapes, (2) can enhance our insight into dynamics via visualization and experimentation, but (3) leave open many important questions regarding long-term process physics.
*   To develop a sense of “best practices” in using landscape evolution models.

[![Image 1](https://csdms.colorado.edu/csdms_wiki/images/thumb/Mesh_schematic.jpg/400px-Mesh_schematic.jpg)](https://csdms.colorado.edu/wiki/File:Mesh_schematic.jpg)

_Fig. 1: Schematic diagram of CHILD model's representation of the landscape: hexagonal Voronoi cells, nodes (at centers of cells) connected by the edges of the Delaunay triangulation, vegetated cell surfaces, channelized cells, and soil and sediment layers above bedrock._

Introduction to LEMs
--------------------

### Brief History

G.K. Gilbert, a member of the Powell Expedition, produced “word pictures” of landscape evolution that still provide insight. For example, consider his “Law of Divides” (Gilbert 1877):

We have seen that the declivity over which water flows bears an inverse relation to the quantity of water. If we follow a stream from its mouth upward and pass successively the mouths of its tributaries, we find its volume gradually less and less and its grade steeper and steeper, until finally at its head we reach the steepest grade of all. If we draw the profile of the river on paper, we produce a curve concave upward and with the greatest curvature at the upper end. The same law applies to every tributary and even to the slopes over which the freshly fallen rain flows in a sheet before it is gathered into rills. The nearer the water-shed or divide the steeper the slope; the farther away the less the slope.

It is in accordance with this law that mountains are steepest at their crests. The profile of a mountain if taken along drainage lines is concave outward...; and this is purely a matter of sculpture, the uplifts from which mountains are carved rarely if ever assuming this form.

Flash forward to the 1960’s, and we find the emergence of the first one-dimensional profile models. Culling (1963), for example, used the diffusion equation to describe the relaxation of escarpments over time. Models became more sophisticated in the early 1970’s. Frank Ahnert and Mike Kirkby, among others, began to develop computer models of slope profile development and included not only diffusive soil creep but also fluvial downcutting as well as weathering (Ahnert 1971; Kirkby 1971). Meanwhile, Alan Howard developed a simulation model of channel network evolution (Howard 1971).  
The mid-1970’s saw the first emergence of fully two-dimensional (and even quasi-three-dimensional) landscape evolution models, perhaps most noteworthy that of Ahnert (1976). Geomorphologists would have to wait nearly 15 years for models to surpass the level of sophistication found in this early model.  
During that time, computers would become much more powerful and able to model full landscapes. The late 1980’s through the mid-1990’s saw the beginning of the “modern era” of landscape evolution models, and today there are many model codes with as many applications, scales, and objectives, ranging from soil erosion to continental collision (Table 1).

Brief Overview of Models and their Uses
---------------------------------------

Some examples of landscape evolution models (LEMs) are shown in Table 1. LEMs have been developed to represent, for example, coupled erosion-deposition systems, meandering, Mars cratering, forecasting of mine-spoil degradation, and estimation of erosion risk to buried hazardous waste. These models provide powerful tools, but their process ingredients are generally provisional and subject to testing. For this reason, it is important to have continuing cross-talk between modeling and observations—after all, that’s how science works.  
In this exercise, we provide an overview of how a LEM works, including how terrain and water flow are represented numerically, and how various processes are computed.

| Model | Example reference | Notes |
| --- | --- | --- |
| SIBERIA | Willgoose, Bras, and Rodriguez-Iturbe (1991) | Transport-limited; |
|  |  | Channel activator function |
| DRAINAL | Beaumont, Fullsack, and Hamilton (1992) | “Undercapacity” concept |
| GILBERT | Chase (1992) | Precipiton |
| DELIM/MARSSIM | Howard (1994) | Detachment-limited; |
|  |  | Nonlinear diffusion |
| GOLEM | Tucker and Slingerland (1994) | Regolith generation; |
|  |  | Threshold landsliding |
| CASCADE | Braun and Sambridge (1997) | Irregular discretization |
| CAESAR | Coulthard, Kirkby, and Macklin (1996) | Cellular automaton algorithm |
|  |  | for 2D flow field |
| ZSCAPE | Densmore, Ellis, and Anderson (1998) | Stochastic bedrock |
|  |  | landsliding algorithm |
| CHILD | Tucker and Bras (2000) | Stochastic rainfall |
| EROS | Crave and Davy (2001) | Modified precipiton |
| TISC | Garcia-Castellanos (2002) | Thrust stacking |
| LAPSUS | Schoorl, Veldkamp, and Bouma (2002) | Multiple flow directions |
| APERO/CIDRE | Carretier and Lucazeau (2005) | Single or multiple |
|  |  | flow directions |

_Table 1: Partial list of numerical landscape models published between 1991 and 2005._

Continuity of Mass and Discretization
-------------------------------------

A typical mass continuity equation for a column of soil or rock is:

<math\>\\frac{\\partial n}{\\partial t} = B - \\nabla \\vec{q}\_s</math\>     (1)

where _η_ is the elevation of the land surface \[L\]; _t_ is time; _B_ \[L/T\] represents the vertical motion of the rocks and soil relative to baselevel (due, for example, to tectonic uplift or subsidence, sea-level change, or erosion along the boundary of the system); and _q⃗__s_ is sediment flux per unit width \[L2/T\]. (The letters in square brackets indicate the dimensions of each variable; L stands for length, T for time, and M for mass.) This is one of several variations; for discussion of others, see Tucker and Hancock (2010). Some models, for example, distinguish between a regolith layer and the bedrock underneath (Fig. 1). Note that this type of mass continuity equation applies only to terrain that has one and only one surface point for each coordinate; it would not apply to a vertical cliff or an overhang.

A LEM computes _η_(_x_, _y_, _t_) given (1) a set of process rules, (2) initial conditions, and (3) boundary conditions. One thing all LEMs have in common is that they divide the terrain into discrete elements. Often these are square elements, but sometimes they are irregular polygons (as in the case of CASCADE and CHILD; Fig. 1). For a discrete parcel (or “cell”) of land, continuity of mass enforced by the following equation (in words):

_Time rate of change of mass in element = mass rate in at boundaries - mass rate out at boundaries + inputs or outputs from above or below (tectonics, dust deposition, etc.)_

This statement can be expressed mathematically, for cell _i_, as follows:

<math\>\\frac{d\\eta\_i}{dt} = B + \\frac{1}{\\Lambda\_i} \\sum\_{j=1}^N q\_{sj} \\lambda\_j</math\>     (2)

where Λ _i_ is the horizontal surface area of cell _i_; _N_ is the number of faces surrounding cell _i_; _q__s__j_ is the unit flux across face _j_; and _λ__j_ is the length of face _j_ (Fig. 2). (Note that, for the sake of simplicity, we are using volume rather than mass flux; this is ok as long as the mass density of the material is unchanging). Equation (2) expresses what is known as a _finite-volume_ method because it is based on computing fluxes in and out along the boundaries of a finite volume of space.

_Some terminology: a **cell** is a patch of ground with boundaries called **faces**. A **node** is the point inside a cell at which we track elevation (and other properties). On a raster grid, each cell is square and each node lies at the center of a cell. On the irregular mesh used by CASCADE and CHILD, the **cell** is the area of land that is closer to that particular node than to any other node in the mesh. (It is a mathematical entity known as a **Voronoi cell** or **Thiessen polygon**; for more, see Braun and Sambridge (1997), Gregory E Tucker, Lancaster, Gasparini, Bras, et al. (2001).)_

Equation (2) gives us the time derivatives for the elevation of every node on the grid. How do we solve for the new elevations at time _t_? There are many ways to do this, including matrix-based implicit solvers (see for example Fagherazzi, Howard, and Wiberg (2002); Perron (2011)). We won’t get into the details of numerical solutions (at least not yet), but for now note that the simplest solution is the forward-difference approximation:

<math\>\\frac{d\\eta\_i}{dt} \\approx \\frac{\\eta\_i(t+\\Delta t) - \\eta\_i(t)}{\\Delta t}</math\>     (3)

<math\>\\eta\_i(t+\\Delta t) = \\eta\_i(t) + U\\Delta t + \\Delta t \\frac{1}{\\Lambda\_i} \\sum\_{j=1}^N q\_{sj} \\lambda\_j </math\>     (4)

The main disadvantage of this approach is that very small time steps are typically needed in order to ensure numerical stability. (CHILD uses a variant of this that seeks the largest possible stable value of Δ _t_ at each iteration). A good discussion of numerical stability, accuracy, and alternative methods for diffusion-like problems can be found in Press et al. (2007).

[![Image 2](https://csdms.colorado.edu/csdms_wiki/images/thumb/Child_mesh_schem.jpg/300px-Child_mesh_schem.jpg)](https://csdms.colorado.edu/wiki/File:Child_mesh_schem.jpg)

_Fig. 2: Schematic diagram of CHILD mesh with illustration of calculation of volumetric fluxes between cells. Dashed lines indicate cells and their faces, solid circles are nodes, and solid lines show the edges between nodes._

Gravitational Hillslope Transport
---------------------------------

Geomorphologists often distinguish between hillslope and channel processes. It’s a useful distinction, although one has to bear in mind that the transition is not always abrupt, and even where it is abrupt, it is commonly either discontinuous or highly dynamic or both.  
Alternatively, one can also distinguish between processes that are driven nearly exclusively by gravitational processes, and those that involve a fluid phase (normally water or ice). This distinction too has a gray zone: landslides are gravitational phenomena but often triggered by fluid pore pressure, while debris flows are surges of mixed fluid and solid. Nonetheless, we will start with a consideration of one form of gravitational transport on hillslopes: soil creep.

Linear Diffusion
----------------

For relatively gentle, soil-mantled slopes, there is reasonably strong support for a transport law of the form:

_q⃗__s_ =  − _D_∇_η_     (5)

where _D_ is a transport coefficient with dimensions of L2T − 1. Using the finite-volume method outlined in Equation (2), we want to calculate $\\vec{q\_s}$ at each of the cell faces. Suppose node _i_ and node _k_ are neighboring nodes that share a common face (we’ll call this face _j_). We approximate the gradient between nodes _i_ and _k_ as:

<math\>S\_{ik} = \\frac{\\eta\_k - \\eta\_i}{L\_{ik}}</math\>     (6)

where _L__i__k_ is the distance between nodes. On a raster grid, _L__i__k_ = Δ _x_ is simply the grid spacing. The sediment flux per unit width is then

<math\>q\_{sik} \\simeq D \\frac{\\eta\_k - \\eta\_i}{L\_{ik}}</math\>     (7)

where _q__s__i__k_ is the volume flux per unit width from node _k_ to node _i_ (if negative, sediment flows from _i_ to _k_), and _L__i__k_ is the distance between nodes. To compute the total sediment flux through face _j_, we simply multiply the unit flux by the width of face _j_, which we denote _λ__i__j_ (read as “the _j_\-th face of cell _i_”):

_Q__s__i__k_ = _q__s__i__k__λ__i__j_     (8)

**_Exercise 1: Getting Set Up with CHILD_**
-------------------------------------------

Our first exercise is simply to ensure that everything is in place for CHILD to be run and visualized. Note that Matlab is required to run the visualization scripts. You should already have an account on WMT and an account on beach. Note that your login credentials may not be the same for WMT as for beach.

\>\> If you do not have an account on beach, request one [here](https://csdms.colorado.edu/wiki/HPCC_account_requirements).

\>\> If you do not have an account on WMT, create one [here](https://csdms.colorado.edu/wmt/WMT.html).

\>\> If you have not downloaded the visualization tools, download them here: [File:CHILDVisTools.tar.gz](https://csdms.colorado.edu/wiki/File:CHILDVisTools.tar.gz "File:CHILDVisTools.tar.gz").

\>\>On a PC you can use 7zip (a free download in case it does not come installed with your system). You will have to run the unpacking two times, once to get rid of the gz, once to untar.

\>\> Move the visualization tools from the download folder to an easy-to-find location such as the Desktop and extract the files by opening a terminal, navigating to the folder location, and typing:

tar -zxvf CHILDVisTools.tar.gz

\>\> Note that your browser might partially extract the files for you. In that case, you may only need to type:

tar -xvf CHILDVisTools.tar

Let’s get ready to visualize the output. Start Matlab. The first thing we will do is tell Matlab where to look for the plotting programs that we will use.

\>\>At the Matlab command prompt type: **path( path, ’_childFolderLocation_∖ChildExercises∖MatlabScripts’ )** For _childFolderLocation_, use the path name of the folder that contains the unzipped visualization scripts. You can also add a folder to your path by selecting _File-Set Path..._ from the menu.

Note that the “package” also includes some documentation that you may find useful: the ChildExercises folder contains an earlier version of this document, and the Doc folder contains the Users’ Guide (child\_users\_guide.pdf). The guide covers the nuts and bolts of the model in much greater detail than these exercises and includes a full list of input parameters. Finally, there is an "Output" folder with several empty subfolders; we will use these folders later to hold the outputs of our model runs.

**_Exercise 2: Hillslope Diffusion and Parabolic Slopes with CHILD_**
---------------------------------------------------------------------

\>\> In a web browser, go to [https://csdms.colorado.edu/wmt/](https://csdms.colorado.edu/wmt/WMT.html).

\>\> Log in with your email address and password.

\>\> Click the "open folder" icon.

\>\> Click the button marked "Labels."

\>\> Check the box labeled "public"

\>\> From the drop-down menu, select "hillslope1" and click "open."

[![Image 3](https://csdms.colorado.edu/csdms_wiki/images/thumb/Howtoopen_hillslope1.png/600px-Howtoopen_hillslope1.png)](https://csdms.colorado.edu/wiki/File:Howtoopen_hillslope1.png)

\>\> You will have to save the model first to your own personal copy. Click the "save as" button under "more" tab

\>\> Enter your beach username and password to submit the model. Note that your beach username and password are the same as your IdentiKey username and password, which may not be the same as your WMT information.

[![Image 4](https://csdms.colorado.edu/csdms_wiki/images/NcedPlay.png)](https://csdms.colorado.edu/wiki/File:NcedPlay.png)

\>\> Click "view run status" to be taken to the results download page. This will open a new tab.

[![Image 5](https://csdms.colorado.edu/csdms_wiki/images/thumb/Screen_Shot_2014-09-03_at_3.56.43_PM.png/400px-Screen_Shot_2014-09-03_at_3.56.43_PM.png)](https://csdms.colorado.edu/wiki/File:Screen_Shot_2014-09-03_at_3.56.43_PM.png)

\>\> This run should take about 30 seconds on WMT. After 30 seconds, refresh the page and download the results by clicking the download button.

[![Image 6](https://csdms.colorado.edu/csdms_wiki/images/thumb/NcedDownload.png/1000px-NcedDownload.png)](https://csdms.colorado.edu/wiki/File:NcedDownload.png)

\>\> Navigate to your browser's download folder and untar the model results. Move all of the output files to the folder _childFolderLocation_∖ChildExercises∖hillslope1 . For _childFolderLocation_, use the path to the Child visualization tools package that you downloaded.

\>\> Return to Matlab and type:

cd('childFolderLocation/hillslope1')

For _childFolderLocation_, use the path name of the folder that contains the unzipped visualization scripts.

 m = cmovie( 'hillslope1', 21, 200, 200, 100, 50 );

This command says \`\`generate a 21-frame movie from the run \`hillslope1' with the x-, y- and z- axes set to 200, 200 and 100 m, respectively, and with the color range representing 0 to 50 m elevation.

To replay the movie, type:

movie

(Windows note: we found that under Vista and Windows 7, the movie figure gets erased after display; slightly re-sizing the figure window seems to fix this).

The analytical solution to elevation as a function of cross-ridge distance _y_ is:

<math\>z(y) = \\frac{U}{2D} \\left( L^2 - (y-y\_0)^2 \\right)</math\>     (9)

where _L_ is the half-width of the ridge (100 m in this case) and _y0_ is the position of the ridge crest (also 100 m). The effective uplift rate _U_, represented in the input file by the parameter UPRATE, is _10\-4_ m/yr. The diffusivity coefficient _D_, represented in the input file by parameter KD, is 0.01 m_2_/yr. You can view these parameters in the input file generated by WMT by navigating to _childFolderLocation_∖ChildExercises∖hillslope1 and using a text editor to open the file _child.in_.

Next, we'll make a plot that compares the computed and analytical solutions.

\>\> Enter the following in Matlab:

*   cd('childFolderLocation∖ChildExercises∖hillslope1') \\% For childFolderLocation, use the location of the child visualization packet that you downloaded
*   ya = 0:200; \\% This is our x-coordinate
*   U = 0.0001; D = 0.01; y0 = 100; L = 100;
*   za = ((U/(2\*D))\*((L^2)-((ya-y0)).^2));
*   figure(2), plot( ya, za ), hold on
*   xyz = creadxyz( 'hillslope1', 21 ); \\% Reads node coords, time 21
*   plot( xyz(:,2), xyz(:,3), 'r.' ), hold off
*   legend( 'Analytical solution', 'CHILD Nodes'

Diffusion theory predicts that equilibrium height varies linearly with _U_, inversely with _D_, and as the square of _L_.

\>\> In WMT, change one of these three parameters. To change _U_, edit the number in the box labeled "duration of uplift (yr)". Similarly, to change _D_, edit the value of the diffusivity coefficient, parameter _KD_. If you want to try a different ridge width _L_, change "Length of grid in x-direction," "Length of grid in y-direction," and "Grid spacing" by the same proportion (changing the grid spacing} will ensure that you keep the same number of model nodes).

[![Image 7](https://csdms.colorado.edu/csdms_wiki/images/thumb/NcedChangeValue.png/800px-NcedChangeValue.png)](https://csdms.colorado.edu/wiki/File:NcedChangeValue.png)

\>\> Re-run CHILD with your modified input file and see what happens. Create a second folder to hold the new model output if you would like to compare the two simulations side-by-side.

Nonlinear Diffusion
-------------------

As we found in our study of hillslope transport processes, the simple slope-linear transport law works poorly for slopes that are not \`\`small" relative to the angle of repose for sediment and rock. The next example explores what happens to our ridge when we (1) increase the relative uplift rate, and (2) use the nonlinear diffusion transport law:

<math\>\\vec{q}\_s = \\frac{-D \\nabla z}{1-|\\nabla z/S\_c|^2}</math\>     (10)

_Exercise 3: Nonlinear Diffusion and Planar Slopes_
---------------------------------------------------

\>\> Open the "hillslope2" model in WMT. Save and submit the job.

\>\> When the 70,000-year run finishes, download the results and move them to the folder _childFolderLocation_∖ChildExercises∖hillslope2. For _childFolderLocation_, use the path to the Child visualization tools package that you downloaded.

\>\> In Matlab, navigate to the hillslope2 folder:

cd('childFolderLocation∖ChildExercises∖hillslope2')

\>\> Type in Matlab:

m = cmovie( 'hillslope2', 21, 200, 200, 100, 70 );

If we had used linear diffusion, the equilibrium slope gradient along the edges of the ridge would be _\= UL/D = (0.001)(100)/(0.01) = 10_ m/m, or about 84<math\>^\\circ</math\>! Instead, the actual computed gradient is close to the threshold limit of 0.7. Notice too how the model solution speed slowed down. This reflects the need for especially small time steps when the slopes are close to the threshold angle.

There is a lot more to mass movement than what is encoded in these simple diffusion-like transport laws. Some models include stochastic landsliding algorithms (e.g., CASCADE, ZSCAPE). Some impose threshold slopes (e.g., GOLEM). One spinoff version of CHILD even includes debris-flow generation and routing (Lancaster, Hayes, and Grant 2003).