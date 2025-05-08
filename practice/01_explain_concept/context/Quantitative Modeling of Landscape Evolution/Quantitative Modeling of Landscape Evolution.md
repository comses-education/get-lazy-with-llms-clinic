# Quantitative Modeling of Landscape Evolution
Source: https://ris.utwente.nl/ws/portalfiles/portal/276880233/3_s2.0_B9780128182345001401_main.pdf

Arnaud JAM Temmea, Jeroen M Schoorlb, Lieven Claessensb,c, and Antonie VeIdkampd,

aDepartment of Geography and Geospatial Sciences, Kansas State University, Manhattan, KS, United States; bSoil Geography and Landscape, Wageningen University, Wageningen, The Netherlands; cInternational Institute of Tropical Agriculture (IITA), Nairobi, Kenya; dUniversity of Twente, Enschede, The Netherlands

© 2021 Elsevier Inc. All rights reserved.

# 1 Introduction

This chapter reviews the quantitative modeling of landscape evolution. Therefore, it does not only focus on landscape evolution models per se, but also on some of the concepts that underlie such models.

Quantitative modeling of landscape evolution is considered here as the dynamic and spatially explicit calculation of landscapes and landscape changes through time by means of computer software. In that sense, it differs from two alternative categories of landscape evolution modeling: the conceptual modeling of landscape evolution and the physical modeling of landscape evolution.

Conceptual, or qualitative, models of landscape evolution are aptly described by Tucker and Hancock (2010) as “word-picture(s) describing the sequential evolution of a landscape over geologic time.” Before the advent of modern computing techniques, such conceptual models provided the visual illustration of—sometimes intense—debates about the nature of landscape change. William Morris Davis’ geological cycle (Davis, 1899) has become the best-known of these models, although its validity has been contested (Orme, 2007). For more information, the reader is referred to Pazzaglia (2003), who included a discussion of conceptual models of landscape evolution in his review of landscape evolution models.

The other alternative; physical modeling of landscape evolution, is the act of mimicking the processes that operate in landscapes on a typically smaller spatial and temporal scale. Downscaling landscapes and landscape activity is a difficult task because it requires the reproduction of correct ratios between material properties and forces on a smaller scale (Pazzaglia, 2003). Nevertheless, significant progress has been made with physical models of landscape evolution. An important case in point is the seminal physical modeling work by Schumm (1973) that resulted, among others, in the conclusions that “some geomorphic anomalies are, in fact, an inherent part of the erosional development of landforms and that the components of a geomorphic system need not be in phase” (1973, p. 300). With these words and in his work, Schumm introduced the now-famous concepts of geomorphic threshold and complex response.

Our subject in this chapter, the quantitative modeling of landscape evolution, currently receives more attention from researchers than its two alternatives and offers possibilities that neither conceptual nor physical models do. For this chapter, we divide these possibilities into four broad categories.

As a start, modern models of landscape evolution allow an unprecedented easy and detailed visualization of the spatially and temporally explicit results of wide ranges of assumptions about process behavior and process interactions. In that sense, quantitative models have replaced conceptual models of landscape evolution as the main method for the description of ideas and hypotheses about landscape evolution (Coulthard, 2001; Tucker and Hancock, 2010; Glade et al., 2017). They have become the geomorphic laboratories of choice (Temme et al., 2017).

Second, when observations on the evolution of a particular landscape are available—for instance in the long term through the presence of river terraces in an incising valley (Tucker, 2009) and the normalized shape of hillslopes (Hurst et al., 2012) or in the shorter term through measurements of radionuclide redistribution (Schoorl et al., 2004), conclusions can be drawn about the validity of underlying model equations (Beven, 2009) or model parameters can be obtained through inversion (Barnhart et al., 2020). Model outputs used for such tests are postdictions, i.e. predictions of something occurring in the past (and typically ending in the present).

Treatise on Geomorphology https://doi.org/10.1016/B978-0-12-818234-5.00140-1
---
# 2 Quantitative Modeling of Landscape Evolution

Third, quantitative models of landscape evolution can be used for the detailed prediction of future landscape change. This requires confidence in model equations and parameters and is typically preceded by model calibration in postdictive studies. Predictions are an important goal of numerical landscape evolution models (Istanbulluoglu, 2009b), but they are rarely made because of limited confidence in predictive ability. As we will discuss below, recent research even suggests that at least some types of landscape change may be inherently unpredictable, due to their self-organized criticality (Coulthard and Van De Wiel, 2007).

A fourth category of numerical landscape evolution modeling studies of interest in this review is best called procedural studies; studies that are focused on learning about model choices rather than learning about landscapes. Studies that present new model algorithms (e.g. Coulthard and Van de Wiel, 2006; Temme et al., 2006) or that focus on the effects of model resolution (Claessens et al., 2005; Schoorl et al., 2000) belong to this category. Procedural studies are of interest because they expose to scientific inquiry the non-trivial computer programming decisions that can otherwise remain hidden or even unknown behind model interfaces (e.g. Nicholas, 2005).

These four categories of numerical landscape evolution studies (procedural, descriptive, postdictive and predictive) will serve as the highest-level structure of this contribution. However, it must be noted that many quantitative landscape evolution modeling studies contain elements of two or more categories. In particular, studies often combine descriptive and postdictive elements, for instance when an existing landscape is used as a template landscape for descriptive studies (e.g. Ellis et al., 1999). Also, many descriptive or postdictive studies have procedural elements when a model is first introduced or tested and then used (e.g., Claessens et al., 2007).

To assess the prevalence of these different categories in the body of literature on quantitative modeling of landscape evolution, we selected 322 studies that present landscape evolution modeling results using the search term “landscape evolution model” in Scopus. Search results that did not (partially) discuss computer models were not considered.

We then assigned all studies to one of our four categories, splitting between papers from before and after 2011 (Table 1)—realizing that this occasionally did not do justice to the width of individual contributions. We found that before 2011, 17 studies are mainly procedural, 63 are mostly descriptive, 35 have a strong postdictive focus, and only two are clearly predictive. After 2011, 40 studies were procedural, 113 studies were descriptive, 51 were postdictive and 1 was predictive in nature. In our further discussion, we will merge the postdictive and predictive categories for practical purposes.

Focusing on the years after 2011, there is a gradual increase in the number of landscape evolution modeling studies published annually (Fig. 1), and overall, landscape evolution models seem to have become a tool used by more researchers, often as one of multiple methods employed to answer questions.

In the remainder of this chapter, we will first give an overview of existing reviews of landscape evolution models. Then, we will cover general properties of modern landscape evolution models and discuss shared concepts and definitions. Third, the body of landscape evolution model studies will be reviewed and discussed. Finally, we venture a look into the future of landscape evolution modeling and explore research opportunities.

**Table 1 Categories of landscape evolution modeling studies and their prevalence in literature before and after 2011.**
|Category|Focus|Before 2011|After 2011|
|---|---|---|---|
|Procedural|Learning about models, presenting new algorithms|17|40|
|Descriptive|Possible mechanisms of landscape change, what-if analysis|63|113|
|Postdictive|Model calibration or validation using landscape change information|35|51|
|Predictive|Prediction of future change|2|1|

LEM papers per year

|Year|Number of Papers|
|---|---|
|2012|35|
|2014|30|
|2016|25|
|2018|20|
|2020|15|

Fig. 1 Number of landscape evolution papers per year, since 2012.
---
# Quantitative Modeling of Landscape Evolution

This chapter is distinct from previous chapters in this volume mostly through the larger spatial and temporal extents that are associated with landscape evolution, as opposed to soil erosion or hillslope evolution. At the very least, landscapes are larger than hillslopes, and typically include more than one of the following elements: drainage divides, hillslopes, river channels, and plains. These landscape elements may be arranged regularly or irregularly, with implications for the connectivity between them (Baartman et al., 2013; Fryirs, 2013). The inclusion of these different landscape elements requires that landscape evolution models at least combine erosion and deposition, in contrast to soil erosion models, which typically simulate on erosion only (e.g. USLE, Wishmeier and Smith, 1978).

At this larger spatial extent, landscape evolution is typically studied over longer timescales than soil erosion or hillslope evolution. In addition, the temporal extent of individual landscape evolution modeling studies is strongly linked to the type of study: procedural, descriptive, postdictive or predictive. Over timescales of millions of years, studies are almost exclusively descriptive—illustrating what landscape evolution could look like under a range of assumptions and almost in the absence of observations (Ellis et al., 1999). Only at smaller timescales, e.g. smaller than several ten thousands of years, when more detailed information about palaeo landscapes and other model inputs is available, do studies become typically postdictive (Tucker, 2009). Finally, studies predicting future evolution of a particular landscape have temporal extents that are typically smaller than the postdictive studies that are used to calibrate the models for prediction (Temme et al., 2009; Willgoose and Riley, 1998). In keeping with their nature, procedural studies do not entail a typical temporal extent.

We do not consider analytical solutions to landscape evolution problems in this chapter because their application has hitherto been—and conceivably remains—limited to idealized cases (e.g. Tucker, 2004) or cases with simple boundary conditions. Readers interested in analytical solutions are best referred to a recent volume that includes an excellent overview of analytical solutions to landscape evolution equations (Pelletier, 2008).

# Recent reviews of quantitative landscape evolution modeling

Two early reviews of models that focus on landscape evolution are by Kirkby (1988, 1993). These reviews partly reflected the descent of such models from the hillslope and erosion models that are not the subject of this chapter.

The years since 2000 have seen more reviews of landscape evolution modeling, summarized in Table 2. Pazzaglia (2003) took the widest view and discusses quantitative, conceptual and physical models of landscape evolution.

The most practically and procedurally oriented reviews are Coulthard (2001) and Tucker and Hancock (2010). Coulthard (2001) reviewed four landscape evolution models from the user-point of view, comparing model characteristics such as runtime and type of inputs and outputs. Tucker and Hancock (2010) reviewed the entire chain of assumptions, choices and solutions used in contemporary landscape evolution models. These two reviews are useful starting points when planning a quantitative landscape evolution study—along with more general modeling works like Beven (2009).

Bras et al. (2003) wrote an elegant and personal defence of landscape evolution modeling against possible criticisms, arguing why such models have value even when they do not pass the most stringent mathematical and physical tests. Martin and Church (2004) focused on the appropriate level of detail in process descriptions in landscape evolution models as a function of spatial scale—ranging from mechanistic (Newtonian) modeling at small scales up to generalized, cellular automata at larger scales. At the same wide range of spatial scales is Willgoose (2005), which covers both geomorphic and computer issues.

|Authors|Year|Title|
|---|---|---|
|Coulthard|2001|Landscape evolution models: a software review|
|Bras et al.|2003|Six myths about mathematical modeling in geomorphology|
|Pazzaglia|2003|Landscape evolution models|
|Martin and Church|2004|Numerical modelling of landscape evolution: geomorphological perspectives|
|Whipple|2004|Bedrock rivers and the geomorphology of active orogens|
|Willgoose|2005|Mathematical modeling of whole landscape evolution|
|Codilean et al.|2006|Surface process models and the links between tectonics and topography|
|Bishop|2007|Long-term landscape evolution: linking tectonics and surface processes|
|Tucker and Hancock|2010|Modelling landscape evolution|
|Minasny et al.|2015|Resolving the integral connection between pedogenesis and landscape evolution|
|Chen et al.|2014|Landscape evolution models: A review of their fundamental equations|
|Williams et al.|2016|Numerical modelling of braided river morphodynamics: Review and future challenges|
|Temme et al.|2017|Developing, choosing and using landscape evolution models to inform field-based landscape reconstruction studies|
|Braun|2018|A review of numerical modeling studies of passive margin escarpments leading to a new analytical expression for the rate of escarpment migration velocity|

---
# 4 Quantitative Modeling of Landscape Evolution

Both Codilean et al. (2006) and Bishop (2007) reviewed landscape evolution models at the largest spatial and temporal extents, where tectonics and topographic processes interact. Whipple (2004) took a somewhat smaller focus and discussed the modeling of bedrock rivers in different tectonic settings. At even smaller extent, Williams et al. (2016) focus on the modeling of morphodynamics of braided river reaches.

Minasny et al. (2015) reviewed the extent to which soil development has been included in LEMs, Braun (2018) reviewed landscape evolution modeling of passive margins and Temme et al. (2017) focused specifically on strategies for postdictive LEM studies.

# 3 Quantitative models of landscape evolution: Concepts and definitions

# 3.1 Landscape evolution

Of the first sentences of this chapter gives a broad definition: landscape evolution is the change of landscapes over time. The word evolution suggests both slow and (very) long-term change—but by no means rates of change that are constant over time. The notion of constant rates—uniformitarianism—is out-dated (Gould, 1965). In fact, relatively sudden events such as extreme floods, volcanic eruptions, major debris flows and lahars or large rock falls can have huge impacts on landscapes that may persist over millennia (e.g., Lamb and Fonstad, 2010; van Gorp et al., 2016). Nonetheless, in some cases, and after averaging over appropriate timescales, an equilibrium may exist between uplift on the one hand and erosion and deposition through various processes on the other hand. Such an equilibrium would result in stable (“steady-state”) landscape morphology. The prevalence of such conditions in the real world has been questioned (Phillips, 2010), but equilibrium conditions are often imposed during model studies of theoretical landscapes to gain an understanding of first-order controls on key landscape metrics (e.g. Langston et al., 2015; Simón et al., 2000; Willett et al., 2001).

# 3.2 Landscape evolution models

At their core, modern landscape evolution models calculate the effects of geomorphic and tectonic processes on the landscape, driven by climate and conditioned by lithological and topographic boundary conditions. In mathematical terms, they are sets of equations operating on a digital representation of a landscape. The model setup scheme in Fig. 2 (adapted from Beven, 2001) helps to structure a short introduction to such models and related concepts and definitions.

In the scheme, the setup of landscape evolution model studies proceeds from choosing the objectives through making perceptual, conceptual and procedural models to model calibration and model evaluation. For now, we focus on the first four steps—where the model is built—rather than on the last two steps—where the model is used.

The choice of objectives determines the spatial and temporal extents of a quantitative landscape evolution modeling study. It also determines the type of output that is required: a digital representation of a landscape or alternatively a landscape metric, such as mean elevation or drainage network configuration (e.g. Rinaldo et al., 1993). Models that simulate landscape metrics are

|Objectives|Define spatiotemporal extent|
|---|---|
|Reconsider|The perceptual model|
|Revise equations|Conceptual model|
|Decide on equations|Debug code|
|Procedural model|Write and test computer code|
|Revise values|Model calibration|
|Get parameter values, optimize fit|Model evaluation|
|Assess accuracy and error|No|
|Success?|Yes|

Fig. 2 (Beven, 2001)’s model setup scheme. Adapted from Beven K (2001) Rainfall-Runoff Modelling: The Primer, 361 pp. Chichester: John Wiley & Sons.
---
# Quantitative Modeling of Landscape Evolution

sometimes called surrogate models (Pazzaglia, 2003) to distinguish them from more traditional landscape evolution models. The objectives of a study also determine whether it is procedural, descriptive, postdictive or predictive.

In the perceptual model phase, choices are made about the processes included in the model. For our purposes here, two choices are particularly important because they strongly impact model structure.

First, whether to use multiple processes or one process only. When it is decided that multiple processes are relevant for a study, decisions regarding their interaction must be made during the next steps in model setup that are otherwise not necessary. Such decisions include the use of homogenous or heterogeneous spatial and temporal resolution for the processes (Temme et al., 2011). The most commonly included processes are fluvial erosion and deposition and hillslope diffusion—a contained concept that encompasses processes such as soil creep, frost heave, and sometimes landsliding (Roering et al., 2001a,b).

Second, and more specifically, whether to include tectonics. At timescales shorter than hundreds of thousands of years, tectonics are not usually included in landscape evolution models. Therefore, these models are sometimes called surface process models (e.g., Codilean et al., 2006).

In the conceptual model phase, decisions are made about the equations that describe each process in the model. Typically, choices are placed along an imaginary axis ranging from fully mechanistic (Newtonian) approaches to fully descriptive (regression-based) approaches (like the USLE-type hillslope erosion models (Renard et al., 1997; Wishmeier and Smith, 1978). Mechanistic models need limited calibration at the expense of strong computing and data demands. As a result, (nearly) mechanistic models are used only at short timescales and for small study areas—for instance to study evolution of reaches of large-boulder rivers (Hodge et al., 2007; Williams et al., 2016). Because of their lack of use in whole-landscape studies, we will disregard them in this review.

More descriptive equations offer ease of use at larger temporal and spatial extents at the expense of larger calibration needs and a weaker connection of model parameters to measurable physical quantities. All landscape evolution models are descriptive to some extent, most of them strongly so (Brasington and Richards, 2007). Common simplifications of the mechanistic St. Venant equations that describe waterflow are first the assumptions that flow has steady speed within a timestep (quasi-steady state, the gradually varied flow approximation), then that inertia of water is negligible (the diffusion-wave approximation), and finally that water pressure effects on water flow are negligible (the popular kinematic-wave approximation, where flow is determined by topography only (Tucker and Hancock, 2010).

In the procedural model phase, decisions are made about the translation of equations into computer code. This is no trivial step, especially because decisions include a choice for the discretization of the landscape. The two most popular discretizations are the Digital Elevation Model (DEM) and the Triangulated Irregular Network (TIN). In DEMs, the landscape is represented as a regular grid of square cells with uniform altitude. In TINs, the landscape is built up of Delaunay triangles. This choice is usually followed by the choice for an algorithm for the flow of water over the surface, based on the kinematic-wave approximation—if the geomorphic processes under consideration are dependent on the amount of water. Many water flow algorithms are available, most of them reviewed and tested in Freeman (1991) and Murray and Paola (1997). In the resulting calculation framework, equations are translated into computer code (Pelletier, 2008). Recent improvements have focused on parallelizing (Barnes, 2019) and linear scaling (Anand et al., 2020) of the computationally intensive flow routing calculations.

From the setup scheme, it can be argued that every new landscape evolution modeling study (with new objectives) should lead to a new model formulation. However, existing models (and their set of underlying perceptual, conceptual and procedural choices) are often re-used in later research with minor or no changes, especially within research teams.

Models or model frameworks that allow individual users to choose among a range of perceptual, conceptual and procedural choices, minimize this problem. Some model setup choices have been included in the interfaces of modern landscape evolution models (e.g. Lorica, Fig. 3 and CAESAR-Lisflood, Ramirez et al., 2020). Landlab (e.g. Shobe et al., 2017) is a modeling framework specifically designed to be modular, i.e. to allow the construction of a wide range of models based on user perceptual, conceptual and procedural choices. The availability of such models in advanced facilities such as those of the Community Surface Dynamics Modeling System (CSDMS, Voinov et al., 2010) are instrumental in opening up the range of model setup options to modelers while minimizing time spent on writing computer code (e.g. Pan et al., 2021; Shen et al., 2021).

# 3.3 Geomorphic processes

As shown above, a central concept in geomorphology and geomorphic modeling is the geomorphic process. This concept has not been critically discussed in the reviews mentioned before, although it has been the topic of philosophical work (e.g., Rhoads, 2006).

Geomorphic processes have been recognized since the birth of the discipline as the activities leading to the formation and maintenance of different landforms (e.g. Press and Siever, 1994). For instance, wind erosion and deposition lead to dune formation, glacial activity leads to characteristic moraine and sub-glacial landforms, and solifluction leads to lobate forms on hillslopes. Born in the conceptual landscape evolution modeling age, these form-process relationships (or, if one is more critical, narratives, e.g., Rhoads, 2006) have been at the base of geomorphic thinking ever since. At that point, landforms were thought of as the result of single processes and were described in mono-genetic terms. This categorical way of thinking is fundamentally at odds with modern numerical multi-process models where a landscape changes and landforms develop because of the activity and interaction of multiple processes.

It can be argued that what are seen as processes, are sets (or categories) of landscape activity defined in a multi-dimensional space of material properties (including resistance) and affecting forces. It is not ensured that our traditional definition of these sets of activity—by means of the landforms that they supposedly create—is objective or correct.
---
# 6 Quantitative Modeling of Landscape Evolution

# LORICA Landscape Evolution Model

# RunFile Map

# About

|Geomorphic processes|Soil forming processes|Hydrological parameters|Inputs|Run|Output|
|---|---|---|---|---|---|
|Water erosion and deposition|Tillage|Creep|Landsliding|Solifluction|Rock weathering|
|Tectonics|Tree fall|Activate this process|Only calculate water flow, no erosion and deposition|Daily water flow|(multiple flow factor)|
|1.67|m (exponent of overland flow)|1.3|(exponent of slope)|1.0003|K (erodibility)|
|0.01|erosion threshold|rock protection constant|bio protection constant|0|selectivity change constant|

Start
Quit
view tabs?

info

time

processes

sed export

Tillage volume

# FLOW

|River|Mudflow|Earthflow|Landslide|Solifluction|
|---|---|---|---|---|
|dry|Seasonal|SLIDE|Rockslide|Talus creep|
|soil creep|HEAVE| | | |

Fig. 4 is a concrete example of the ideas in Fig. 3 for hillslope processes. However, processes are not occupying an area in process space, but are merely points. Assigning processes to points instead of areas does not solve but rather avoids the overlap and underlap issues raised above. It leaves unanswered questions such as: when does landsliding change into earthflow? Which geomorphic activity happens between solifluction and mudflows—have we considered that activity in our studies?

As mentioned above, multi-process numerical landscape evolution models that combine processes that suffer from overlap and underlap would ab initio calculate some geomorphic activity twice and some activity not at all. Since overlap and underlap cannot be avoided with our current set of process-definitions, this is not merely a problem of academic importance.

It may seem that (in postdictive studies) these problems can be solved in the model calibration step (Fig. 1). Indeed, it is not unthinkable that calibrating—tuning—parameters in the equations for the different processes can cause the model to calculate an output that is in agreement with a set of observations. However, this would be unsatisfactory because the correct output would have been calculated with the wrong model—causing problems in validation (Fig. 1) and prediction.
---
# Quantitative Modeling of Landscape Evolution

# 7

hydrology geomorphology biology geology engineering (geochemistry human biogeochemistry EARTH SURFACE DYNAMICS atmospherics

Fig. 5 A visualization of the interdependence and interactions between fields related to landscape evolution (Murray et al., 2009).

The multi-process problem is all the more alarming because our common focus seems to be shifting toward the study of the interaction between processes. Recent reviews and white papers (Murray et al., 2009; Paola et al., 2006; Reinhardt et al., 2010) call for a more holistic view of landscape change, accounting for the many interactions between and among geomorphic processes, hydrology, vegetation (ecology) and perhaps human activity (Fig. 5).

If our models with individual, over- or underlapping geomorphic processes have been calibrated to calculate the correct output for the wrong reasons, then individual process activities or volumes are wrong. Therefore, interactions between them will also be calculated wrongly.

This means that, although process overlap and underlap are not currently seen as major problems in landscape evolution modeling, their effects may become more important as we continue to integrate our models with more geomorphic processes and with models from other environmental or socio-economical sciences (Claessens et al., 2009)—resulting in new feedbacks and interactions that are at risk. Solutions to these problems must come from a clear definition of individual processes, which may differ between studies.

# 4 Landscape evolution model studies

Below, we discuss the landscape evolution modeling literature; categorized on the type of study as procedural, descriptive, postdictive or predictive.

# 4.1 Procedural studies

A decade ago, a large portion of procedural studies focused on exploring the impact the digital representation of the landscape. As mentioned above, there are essentially two options in landscape evolution modeling: regular grids (we use the better-known term DEMs as stand-in for the more specific term Digital Terrain Models) and triangulated irregular networks (TINs). Taking DEMs as a starting point, three issues are focused on in LEM literature: (i) the effect of production or gridding method, (ii) the effect of DEM resolution and (iii) the effect and role of sinks and depressions.

Hancock (2006), for instance, showed that DEM-derived topographical or hydrological properties may show (subtle) differences between different gridding methods. However, over large temporal extents, SIBERIA landscape evolution model outputs are not significantly different between these gridding methods—suggesting that the choice of gridding method is not of particular importance for their landscape evolution model study.

Resolution does matter of course. There have been only few tests of the effect of resolution on landscape evolution model results. According to Schoorl et al. (2000), DEM resolution has a strong effect on soil redistribution and especially redeposition rates: the coarser the spatial modeling resolution, the smoother the slope, and the less re-deposition their LAPSUS-model predicts. Claessens et al. (2005) found a similarly strong effect of DEM resolution on shallow landslide hazard and soil redistribution modeling (Fig. 6), also using the LAPSUS model (Claessens et al., 2007). These results can serve as illustrations of the fact that there is a danger involved in changing the resolution of the digital landscape: process descriptions or their parameters may be invalid for resolutions that they were not designed for.

Both Temme et al. (2006) and Hancock (2008) have studied depression removal in landscape evolution models. Depressions (or sinks) in DEMs may be either spurious (due to errors in DEM production, or due to too coarse resolution) or natural (e.g. karst depressions, lakes, post-glacial kars). Hancock (2008) found that initial sediment export rates of a catchment differed considerably between DEMs with and without depressions, but that the difference was negligible at timescales longer than a thousand years.

Arguing the other way around (landscape evolution models should be able to deal with natural depressions to study the interaction and incorporation of sink-causing processes), Temme et al. (2006) designed an algorithm that allows LEMs to deal with large and small depressions as natural landscape elements that can be filled in, enlarged or fragmented (Fig. 7). Using this algorithm for a research area in South Africa, they also found a decreasing importance of sinks in input DEMs as runs progressed.

The use of TINs in landscape evolution modeling was pioneered by Braun and Sambridge (1997), who listed some advantages and disadvantages of working with TINs and DEMs. Tucker et al. (2001) uses a set of routing and transport equations designed for use in a TIN environment. Using the CHILD model, Clevis et al. (2006) proposed an algorithm for dealing with the problem of linking TINs and raster discretization schemes and illustrated its applicability in river meander and subsurface fluvial architecture modeling (Fig. 8). The Landlab model framework (Shen et al., 2021) can deal with both DEM and TIN discretizations.
---
# 8 Quantitative Modeling of Landscape Evolution

| | |10 m|25 m|50 m|100 m|
|---|---|---|---|---|---|
|2|2₅|1.5|1|0.5|0|
| | |0.77|0.2|0.1|A) 0.05|

Fig. 6 Total amounts of landslide erosion for different critical rainfall thresholds and DEM resolutions (Claessens et al., 2005).

Legend

- New shore
- Delta (0.2 m altilines)
- Original DEM (3 m altilines)
- Original shore

Fig. 7 The building of a delta in a hypothetical depression with sediment from upstream erosion (not shown) using the algorithm of Temme et al. (2006).

flow lines

Voronoi cell

Fig. 8 Landscape evolution modeling with TINs: example of steepest descent flow routing (Tucker et al., 2001).

More recently, procedural studies often focus on improving LEM computational speed (Braun and Willett, 2013). The use of larger DEMs and more involved process formulations, along with the need for many model runs for inversion (Chandra et al., 2020), calibration or sensitivity analysis, has placed a premium on the acceleration of model runtimes. Croissant and Braun (2014) presented a scheme to very rapidly solve flow routing using steepest descent in the Fastscape model, and Anand et al. (2020) provided a fast method to route flow using multiple flow directions. Models are increasingly able to use parallelization (Barnes, 2019), enabling model runs on high-performance computers with many Graphic Processing Units.

There is also more attention for the creation of realistic manifold artificial landscapes that avoid idiosyncrasies of real landscapes (Hillier et al., 2015), yet at the same time avoid the radical simplification that would preclude their use as realistic input (Bunel et al., 2021).
---
# Quantitative Modeling of Landscape Evolution

# 4.2 Descriptive studies

Most descriptive studies that we reviewed, can be subdivided into three broad categories. The first category contains work that focuses on experimentation with the interactions between tectonic and surface processes. The second category contains a set of studies that apply sensitivity analysis to explore landscape reaction to a range of variables and processes. A third category of landscape evolution model studies focuses on the use of models to define field-observations that can help decide between competing equations for geomorphic processes.

In the first category, Kooi and Beaumont (1996) investigated the response of a landscape evolution model to tectonic forcing at spatial scales ranging from slopes to series of basins. Densmore et al. (1998) used a numerical landscape evolution model combining a detailed tectonic displacement field with a set of physically based geomorphic rules including bedrock landsliding, to generate synthetic landscapes that closely resemble mountainous topography observed in the western US Basin and Range. Similarly, in Western Nepal, Champel et al. (2002) use a landscape evolution model combining uplift, hillslope diffusion and landsliding to demonstrate the dynamics of fault-related fold propagation. In south-eastern Australia, Van Der Beek and Braun (1999) use a similar model to assess controls on landscape evolution and denudation history.

Studying extensional relay zones with a similar model, Densmore et al. (2003) conclude that the geomorphic evolution of such zones is an interplay between the timescale over which the fault array develops, and the timescale over which the footwall catchment fan-systems are established. Miller and Slingerland (2006) and Miller et al. (2007) use landscape evolution modeling to suggest an explanation for the fact that drainage basins along opposite flanks of mountain ranges are aligned and commonly similar in planform. Their model, with tectonics, detachment-limited stream incision and linear hillslope diffusion, shows such advection of topography when valleys are incised and bedrock moves laterally. In a simpler tectonic setting—uniform vertical uplift—Pelletier (2004) shows that drainage migration (as opposed to stable drainage networks) occurs only when steepest-descent water routing is abandoned in favor of bifurcation routing (or presumably other more complicated routing schemes). Duvall and Tucker (2015) explored the impact of strike-slip movements on ridges and valleys.

Recent studies have focused on the potential of model inversion, i.e. estimation of model input parameters from topography. He et al. (2021) used a model to estimate topographic advection and uplift gradient history from the location of mountain drainage divides. Similar approaches to relief inversion have featured models that combine tectonics, surface processes and increasing rainfall processes (Zavala et al., 2020; Gallen and Fernández-Blanco, 2021; Pan et al., 2021; Shen et al., 2021).

In the second category (sensitivity analysis to explore landscape reaction to a range of variables and processes), Flores-Cervantes et al. (2006) developed a model of headcut retreat of gullies resulting from plunge-pool erosion and did a sensitivity analysis for flow discharge, upstream slope, surface roughness and headcut height. Using similar sensitivity analyses, Strudley and Murray (2007) and Strudley et al. (2006) studied pediment formation and properties as a function of rock type, base level history, style of sediment transport and rainfall rate. They found that uniformity of thin regolith mantles in pediments is governed by a negative feedback between weathering rate and regolith thickness (cf. Minasny and McBratney, 2006). Evaluating different types of transport equations (linear vs. nonlinear), Jimenez-Hornero et al. (2005) show that different conditions might result in the same hillslope morphology. This is an illustration of the concept of polygenesis, which we will discuss more in depth for postdictive studies.

Focusing on signatures of climate in landscapes, Rinaldo et al. (1995) illustrated that both landscapes in equilibrium with current climate and landscapes with relict signatures of past climates are possible. Heimsath et al. (1999) further explore the issue of equilibrium landscapes through a model that predicts the spatial variation in thickness of soil as a consequence of the local balance between soil production and erosion. Using two independent methods, they confirm that soil production varies inversely with the thickness of soil and apply this assumption in the model, comparing modeled soil thickness with measured field data and finding good agreement. Using a deterministic model, Fowler et al. (2007) present a channel equation for the formation of river channels that admits a global steady state. Hancock and Willgoose (2001) showed that the SIBERIA landscape evolution model can correctly simulate experimental model landscapes in declining equilibrium. Their simulations are sensitive to the (non-uniform) spatial distribution of rainfall and DTM errors.

In steeper soil-mantled landscapes in Oregon and California, Roering et al. (2001a, 2007) compared the effect of non-linear and linear transport processes, finding that the timescale of hillslope adjustment is shorter with non-linear transport. In later work, O’Hara et al. (2019) find that sub-orogen-scale uplift perturbation can cause large and long-lived landscape responses away from a steady-state condition.

The difference between timescales of damming events and erosion are the most important controls on river incision and landscape evolution, according to Ouimet et al. (2007), who used an area in the eastern margin of the Tibetan plateau as a template. At larger spatial scales, Roe et al. (2003) find a strong effect of orographic patterns of precipitation and temperature on 1D river profiles. In 2D, Huang (2006) studied the role of groundwater movement in long-term drainage basin evolution for a catchment in Pennsylvania. For dune landscapes, Baas and Nield (2007), Nield and Baas (2008a,b), Baas (2007) used the DECAL model to focus on the interactions between dune formation and vegetation. They found a strong effect of vegetation type (with corresponding geomorphic effect) on the type of predicted equilibrium landscape—something they called an attractor state.

Similarly focusing on the effect of vegetation on geomorphic processes, Istanbulluoglu and Bras (2005) find that a runoff erosion-dominated landscape, under none or poor vegetation cover, may become landslide dominated under a denser vegetation cover. They also substantiate the effects of vegetation disturbances by geomorphic events and wildfires on the landscape structure.
---
# 10 Quantitative Modeling of Landscape Evolution

|Channel|Isolated pediment| | | | | | |
|---|---|---|---|---|---|---|---|
|Tors| | |2000|surfaces|2000| | |
|20| |Regolith|thickness|40| | | |
| | |(m)|1 m|(m)|20| | |
|400| | |0.9 m|400| | | |
| | | | |(m)|0.8 m|(m)|1.8 m|
| | | |0.7 m| |144 m| | |
| | | |0.6 m| |1.2 m| | |
| |10|20|30|40| | | |
|Scale: no. of cells (1 cell = 3x3 m)|0.4 m|10|20|30|40| | |
| |0.3 m| |0.2 m| |0.1 m| | |

|Channel|Isolated pediment| | | | | |
|---|---|---|---|---|---|---|
| | |2000|surfaces|2000| | |
|20|Regolith|thickness|60| | | |
| |(m)|3 m|(m)| | | |
|400| |2.7 m|20| | | |
| |(m)|1 m| |0.9 m| | |
| | |0.8 m|(m)|0.7 m| | |
| | |0.6 m| |0.5 m| | |
| |1.2 m|10|20|30|40| |
| |Scale: no. of cells (1 cell = 3x3 m)|0.9 m| |0.4 m| | |
| | | | |0.6 m| |0.3 m|
| | | | |0.2 m| |0.1 m|
| | |0 m| |0 m| | |

Fig. 9 Different landforms resulting after 5 Ma simulations of high intensity storms in humid environments with 0.1 mm per year incision, initial slope of 5 degrees and rainfall increasing from 20 cm per year (M) to 152 cm per year (P). From Strudley MW and Murray AB (2007) Sensitivity analysis of pediment development through numerical simulation and selected geospatial query. Geomorphology 88(3–4): 329–351.

Fig. 10 Parabolic dune development in the DECAL model. The green gradation indicates grass “density” (vegetation effectiveness), the spacing and size of red sticks indicates woody shrubbery “density.” Started from a flat fully vegetated surface with a few bare circular patches. Transport direction from lower-left to upper-right (unidirectional). From Baas ACW (2007) Complex systems in aeolian geomorphology. Geomorphology 91(3–4): 311–331.
---
# Quantitative Modeling of Landscape Evolution

D’Alpaos et al. (2007) proposed ecomorphodynamic modeling of the interplay between vegetation, erosion and deposition in tidal landscapes to investigate different scenarios of sediment supply, colonization by halophytes, and changing sea level. At global level, Yetemen et al. (2015) simulated the vegetation response to insolation and the attendant erosional dynamics to study hillslope asymmetry across large latitudinal gradients.

Coulthard et al. (2000) and Coulthard and Macklin (2001) apply their CAESAR model to an upland catchment in the United Kingdom to separate the effects of land use and climate change on channel formation. Looking at tectonic and climatic forcing, Tucker (2004) developed analytical solutions for average rates of stream incision and sediment transport in the presence of an erosion threshold for flood flows. Results imply that non-linearity resulting from (not always realistic) threshold effects can have a first-order impact on topography and patterns of dynamic response to tectonic and climate forcing.

In glacial environments, Dadson and Church (2005) studied the evolution of an idealized glaciated valley during the period following retreat of ice using a numerical model including landsliding and fluvial sediment transport. Model results are compared with those from a deterministic linear-diffusion model and predict a rapid rate of fluvial sediment transport following deglaciation with a subsequent gradual decline. Tomkin (2009) presents a numerical model incorporating glacial slide-based erosion that simulates the evolution of glaciated mountain landscapes and shows an application with generic parameters and another one with parameters from the Southern Alps of New Zealand (Fig. 11).

For combined glacial and periglacial settings, Egholm et al. (2012) explain how frost cracking and frost creep may produce summit flats that have persisted since perhaps before the Quaternary.

# Ice Thickness

|Glacial Maximum|Topographic change|Glacial "Buzz Saw"|220 mm/yr|+20|Valley Excavation|
|---|---|---|---|---|---|
|Topographic change|Peak recovery|220 mm/yr|+20|Valley Infilling| |
|Interglacial|Topographic height| | | | |

Fig. 11 Perspective plots of ice thickness at glacial maximum (A), topography and net topographic change at a glacial maximum (B), and topography and net topographic change during an interglacial (C) produced by the Southern Alp simulation model. The area displayed measures 150 km by 20 km, with a vertical exaggeration ratio of 15:1. A and B represent 4.40 Ma of evolution; C represents 4.43 Ma of evolution. Net rates of topographic change are averaged over 10 ka. D is a 150 km by 20 km transect of the central Southern Alps. From Tomkin JH (2009) Numerically simulating alpine landscapes: The geomorphologic consequences of incorporating glacial erosion in surface process models. Geomorphology 103(2): 180–188.
---
# 12 Quantitative Modeling of Landscape Evolution

The model predicts that current rates of sedimentation are higher than the long-term average, and that several tens of thousands of years are required for the landscape to adjust to a change in the dominant erosional forcing. He concludes that therefore, glaciated orogens are unlikely to achieve topographic steady state over Milankovitch timescales. At larger temporal extent, MacGregor et al. (2000, 2009) use a numerical model of glacial erosion and headwall retreat driven by the past 400 thousand years of variable climate to explore the development of the longitudinal profiles of glaciated valleys.

In a tropical setting, Fleurant et al. (2008) simulate the formation of cockpit karst landscapes. Varying the spatial pattern of subsurface dissolution, they conclude that an anisotropic dissolution pattern results in simulated landscapes that better resemble a reference karst landscape in Jamaica than an isotropic dissolution pattern. Kaufmann (2009), using the KARST model, focused on the subsurface evolution of a karst aquifer, although a surface landscape was used as well.

Focusing on hillslopes and river channels, Willgoose et al. (1990, 1991a,b) proposed and applied an early influential drainage network and hillslope evolution model that combined hillslope surface processes with drainage network development. Using sensitivity analysis, they found that the (imposed) amount of flow where hillslope conditions and equations change into channel conditions and equations strongly affects drainage density. The form of a channel network is very sensitive to initial topographic conditions, but physical statistics such as drainage density are only slightly affected by these conditions (cf. Rinaldo et al., 1993).

Willgoose et al. (1991c) describe the results of this model in more detail. They find that the model performs well (“desirable behaviour,” p. 237), both during transient periods and during dynamic equilibrium. Willgoose et al. (1992) use the same model to study how the hillslope and drainage network scale interact in river catchments.

Schneider et al. (2008) use landscape evolution models and morphometric data to illustrate how the ratio between sediment transport on hillslopes and in channels influences landscape and channel network morphologies. Headwaters of fluvial- and debris-flow-dominated systems are characterized by rough, high-relief, highly incised surfaces with a closely spaced channel network whereas where landsliding is important they are characterized by a low channel density and by rather straight and unstable channels and smooth topography. Willgoose and Hancock (1998) use the SIBERIA catchment evolution model to explore the role of hypsometry as an indicator of geomorphic form and process. They show that hypsometry can reflect runoff and erosion processes, and is also strongly dependent on channel network and catchment geometry.

Hancock and Anderson (2002) used a one-dimensional channel-evolution model, including sediment transport, vertical bedrock erosion limited by alluvial cover, and lateral valley-wall erosion, to explore whether and how temporal variations in sediment and water discharge can generate terrace sequences. Sobel et al. (2003) developed models of channel defeat to examine the threshold conditions required to fragment the channel network of large, internally drained areas and concluded that channels persist indefinitely when uplift overwhelms the fluvial systems and defeats the pre-existing channel network.

Studying network morphology, Rinaldo et al. (1993) used a landscape metric model to simulate Optimal Channel Networks (OCNs, Rodriguez-Iturbe et al., 1992) from a range of random topographies, and compared fractal statistics of the results (Tarboton et al., 1988, 1989) to those of real river networks. They concluded that both sets of statistics are indistinguishable—meaning that river networks conform to their assumptions of minimum energy expenditure. Finally, they suggest that OCNs are spatial models of self-organized criticality (Rigon et al., 1994; Rinaldo et al., 1993).

Wainwright (2008) explored an agent-based approach to simulate the dynamic interactions of people and animals with their landscapes and demonstrated the value of this approach in simulating the vulnerability of landform evolution to anthropic pressures (Fig. 12). More traditionally, Schoorl and Veldkamp (2001) and Schoorl et al. (2002) applied the LAPSUS model to explore the impacts of land use and vegetation changes on both on- and off-site landscape and soil properties. Two scenarios of fast and gradual land use change were simulated for a study area in south Spain and different erosion rates and patterns as well as contrasting on- and off-site effects were found (Fig. 13).

Looking at soil more in detail, Rosenbloom et al. (2001, 2006) applied a LEM that focuses on the redistribution of soil texture and soil carbon along a hillslope in response to geomorphic transport processes. The model results suggest that sandy soils are more likely to differentiate downslope with respect to soil texture than clayey soils and that this redistribution will lead to disproportionately broad areas of predominantly coarse-grained particles on upper slopes. The soil-landscape evolution field has since benefitted from pioneering work into 1D simulation of soil development (Finke and Hutson, 2008; Finke et al., 2013; Opolot et al., 2015), resulting in a.o. the MILESD (Vanwalleghem et al., 2013) and LORICA (Temme and Vanwalleghem, 2016) soil-landscape evolution models that are used to explore interactions between soil formation, surface processes under natural and managed conditions (van der Meij et al., 2018, 2020).

The conclusions of work in this second category have resulted in strong attention for the complex-systems properties of landscapes, caused by non-linear cause-effect relationships. Self-organization patterns result from models of fluvial (De Boer, 2001) and eolian landscapes (Baas, 2002) and chaotic behavior is simulated in eolian landscapes (Baas and Nield, 2007). Moreover, as for instance Nicholas and Quine (2007) conclude, dramatic and persistent landscape change (in their case: fan entrenchment) may occur in the absence of external forcing like tectonics and climate (Schoorl et al., 2014) find similar autogenic sediment waves. Using CAESAR, Coulthard and Van De Wiel (2007) take this concept further: in their study, similar amounts of rainfall or runoff produce strongly different amounts of erosion and deposition—they argue that this indicates self-organized criticality in fluvial environments. Supported by similar results by others (Pelletier, 2007a), they point out (Van De Wiel and Coulthard, 2010) that such results are at odds with traditional thinking that interprets the sedimentary record as a function of tectonic or climatic forcing. The conclusion that seemingly minor differences in floodplain morphology can cause widely differing reactions to controls is a message of strong interest to the geomorphological community. Sheehan and Ward (2021) highlight how landscapes with near-horizontal layers that differ in hardness can produce sediment pulses and drainage reorganization that are unrelated to climate changes.
---
# Quantitative Modeling of Landscape Evolution

Animal agents are distributed through the landscape have energy requirements to be met by eating vegetation can move through the landscape to find food but incur energy costs in so doing.

Cells define local characteristics:

- vegetation type and amount
- soil texture and nutrients
- soil-moisture content
- runoff generation
- diffuse erosion
- weathering

Human agents are distributed through the landscape and use the same basic energetics model as the animal agents but can move to hunt, gather or clear vegetation from the landscape.

Local neighbourhoods of cells define:

- flow routing
- concentrated erosion
- sediment routing

Fig. 12 An overview of Wainwright’s (2008) agent-based model combining human, animal and geomorphic effects.

(A) (B)

(C) +1.5 +0.6 0.6 -.5 15 300

Fig. 13 Erosion and deposition outputs (10 years) of the LAPSUS model for three scenarios of land-use change (Schoorl and Veldkamp, 2001). Scenario A corresponds to no land-use change, scenario B and C correspond to different speeds of olive orchard abandonment.

The third category of landscape evolution model studies is about the use of models to define field-observations that can help decide between competing equations for geomorphic processes. Tucker and Slingerland (1994) present a nonlinear, two-dimensional landscape evolution model that is used to assess the necessary conditions for long-term retreat of erosional escarpments of rifted continents. Of all the conditions, high continental elevation is common to most rift margin escarpments and may ultimately be the most important factor. Tucker and Whipple (2002) examine the topographic implications of two leading classes of river erosion models, detachment-limited and transport-limited, in order to identify diagnostic and testable differences.
---
# 14 Quantitative Modeling of Landscape Evolution

between them. Their findings indicate that given proper constraints, it is indeed possible to test fluvial erosion theories on the basis of observed topography. Whipple and Tucker (2002) analyze the implications of various sediment-flux-dependent river incision models for large-scale topography to identify quantifiable and diagnostic differences between models that could be detected from topographic data and to explain the apparent ubiquity of mixed bedrock-alluvial channels in active orogens. Herman and Braun (2006) show that for soil-mantled hillslopes, linear and depth-dependent creep constants can be constrained by simple geomorphometric measurements, such as the distribution of soil thickness on the landform and its relationship to surface curvature. Using a similar approach, Wu et al. (2006) conclude that using drainage area as a surrogate for channel discharge in the stream power erosion law has important shortcomings and suggest using it together with the geomorphoclimatic instantaneous unit hydrograph.

# 4.3 Postdictive and predictive studies

Although some of the studies in the descriptive category use existing landscapes as a template or comparison for their experiments, they were not classified as postdictive because their objective was experimentation rather than the accurate simulation of landscape development. In this section, studies are discussed that do have accurate simulation as an objective.

Almost all postdictive and, by definition, all predictive landscape evolution model studies calculate forward in time, from a more or less well-known palaeo-landscape to another landscape (often the present). The conceptual and mathematical problems of backward modeling are well known. Equifinality, the notion that different palaeo-landscapes may result in one present landscape, and polygenesis, the notion that different processes may be responsible for the formation of a landscape, are at the root of these difficulties (Beven, 2009). However, if processes are well known, and if the landscape does not structurally change within the temporal framework under consideration, then these problems may be small. This was illustrated by Peeters et al. (2006) for a catchment in Belgium. They found that differences between forward and backward modeling with their WaTEM LT model are minor, both in terms of total amount of erosion and in terms of spatial distribution of erosion.

Nevertheless, forward modeling remains the method of choice for postdictive studies. Many of those studies focus on the redistribution (erosion and deposition) of soil over hillslopes and small catchments, at decadal to millennial timescales. First, we discuss several such studies that validate the postdictions of calibrated models.

Desmet and Govers (1995) innovatively used information from soil maps to assess the validity of the outputs of their hillslope erosion model for an agricultural catchment in Belgium. Hancock et al. (2000) used the SIBERIA model in Australia to postdict known 50-year erosion from a man-made mine waste rock dump. The model correctly simulated the geomorphic development of gullies on the dump. Later, Hancock and Willgoose (2002) and Hancock et al. (2002) compared model predictions with physical landscape evolution model results and with a natural catchment on the basis of landscape metrics such as hypsometric curve, width function, cumulative area distribution and area-slope relationship. Van Rompaey et al. (2001) calibrated and validated the sediment delivery model SEDEM using datasets for several dozens of small catchments in Belgium, achieving an average accuracy of 41%. In New Zealand, Roering (2002) used the thickness of (bioturbated, creeping) soil over a 22.6 thousand years old tephra layer as a data source to calibrate a transport model. Peeters et al. (2008) used short-term erosion data to calibrate the WaTEM LT erosion model in Belgium and then successfully postdicted millennial-scale soil erosion known through profile truncation (Fig. 14). They achieved a Model Efficiency Factor (Nash and Sutcliff, 1970) of 0.92 (the maximum MEF value is 1).

|1|0.6|Measured|
|---|---|---|
|3|0.4|Simulated|
|L|0.2| |
|3|0.0| |
|2|-0.2| |
|1|-0.4| |
|1|-0.6|MEF = 0.92|

Scenario 2

Class 1
Class 2
Class 3
Class 4
Class 5

Fig. 14 Peeters et al.’s (2008) comparison of measured and simulated (postdicted) long-term soil redistribution (in mm) for a landscape divided in five classes—using a landscape evolution model that was calibrated with short-term erosion data.
---
# Quantitative Modeling of Landscape Evolution

Van Oost et al. (2004) similarly evaluated a soil redistribution model that uses multiple texture classes. Braun et al. (2001) used observations of soil thickness to evaluate a hillslope transport model. When assuming that hillslope profiles are in equilibrium, steady-state landscape evolution model postdictions can be tested by comparing them directly with existing profiles. Roering et al. (1999) made this assumption for a number of catchments in Oregon and tested postdictions of a hillslope transport law using measured high-resolution profiles. It must be noted that the equilibrium assumption has attracted criticism on theoretical grounds (Phillips, 2010), and that in many settings, hillslope-profiles and catchments are clearly in disequilibrium (e.g. Densmore et al., 2003; Tomkin, 2009). At the very least, use of the equilibrium assumption must be clearly defended.

Radionuclides are a quantitative source of erosion and deposition data. In particular, a cesium isotope—Cs137—has been popular. This anthropogenic radionuclide was deposited worldwide after nuclear tests in the 1960s and has a half-life of about 30 years. When making assumptions about initial spatial distribution (usually uniform) it is therefore well suited to characterize decadal-scale soil redistribution. Govers et al. (1996) used the technique to measure soil redistribution rates in two catchments in Great-Britain and compared these to model postdictions. The modeling of diffusive processes gave the best postdiction: r2 = 0.43 and 0.41 for the two catchments. Later, Quine et al. (1997) used the same technique to study the relative influence of tillage and water erosion at sites in Belgium and China. Schoorl et al. (2004) successfully used the technique with LAPSUS in a more challenging steep and rocky natural area in Spain. Heuvelink et al. (2006) also used the technique with LAPSUS to postdict tillage redistribution for an area in Canada (r2 = 0.39).

In other studies, validation datasets were not available. Calibrating a landslide model, Claessens et al. (2006) used a sediment record at the outlet of a catchment in New Zealand—to assess the postdicted volumes of landslide deposits delivered to rivers. Roering et al. (2001b) calibrated a non-linear hillslope soil transport model with results of a laboratory study of a hillslope of granular material. Roering and Gerber (2005) later used field-measurements of post-fire and long-term critical slope gradient (above which flux increased rapidly) to calibrate a soil redistribution model in Oregon. On a much longer timescale, Gilchrist et al. (1994) used landscape evolution models to study Post-Gondwana geomorphic evolution (denudation) of south-western Africa, resulting in several postdictions that are consistent with large-scale field observations.

In fluvial environments, postdictive studies use network morphology or incision histories (mainly in bedrock reaches) or streambed morphology (mainly in alluvial reaches) to calibrate and validate models. Tomkin et al. (2003) invoked the equilibrium assumption—using terrace sequences to argue for stable incision—to evaluate six competing bedrock incision models in Washington state. None of the models successfully accounted for the observations. Brocard and Van Der Beek (2006) use field observations from several dozens of combined detachment- and transport-limited rivers in the French Alps to calibrate a model for the development of valley flats (in transport-limited reaches). In the Austrian Alps, Anders et al. (2009) used a combined vector-based longitudinal profile incision model and a grid-based surface process model with a 1-m spatial resolution DEM to realistically simulate development of a catchment from the late glacial to present. Langston et al. (2015) explored the various mechanisms by which climate change over glacial-interglacial timescales can affect terrace development along the Colorado Front Range of the Rocky Mountains.

Working in alluvial reaches, Coulthard et al.’s (1998) CAESAR model concentrates on the simulation of floodplain morphology. Working at 1 m resolution in a catchment in Great Britain, CAESAR realistically postdicted formation of bars, braids, terraces and alluvial fans (Coulthard et al., 1998). In another catchment, where rainfall input data for the last 9200 years were prepared, CAESAR was used to postdict landscape development of a reach with an alluvial fan. Fluvial postdictions reacted to climatic and land use changes as expected, but fan postdictions indicated no clear link with climate or land use history (Coulthard et al., 2002). Recent use of the latest version of CAESAR (Coulthard et al., 2013) simulated a Swiss river’s response to historical human engineering works (Gioia and Lazzari, 2019; Gioia and Schiattarella, 2020).

Lancaster and Bras (2002) designed a model of river meandering, which compared well with meanders observed in nature. At larger spatial scale, van Balen et al. (2010) modeled the response of the Rhine-Meuse fluvial system to known climate fluctuations at post-glacial timescales, confirming among others that terraces are diachronic features: they were formed earlier—and are older—upstream than downstream. Results of this 2D study extended the conclusions of an earlier 1D profile study (Tebbens et al., 2000).

Combining tectonics and surface processes, Van Der Beek et al. (1999) postdicted the landscape evolution of the south-eastern Australian highlands—providing a new hypothesis for their formation. Similarly, van der Beek et al. (2002) postdicted denudation history of the South-African Drakensberg and compared model results with apatite fission track data. In tectonically active western Nepal, Champel et al. (2002) used a similar model to postdict a drainage pattern that compared well with observations. Pelletier (2007b) modeled the Cenozoic geomorphic history of the Sierra Nevada, comparing postdictions with known uplift history. Conversely, and as an example of the current use of LEMs in inversion schemes, Racano et al. (2020) used marine terrace ages as calibration targets to infer Quaternary uplift rates along the southern margin of Anatolia.

A general note is in order about the value of goodness-of-fit indicators in postdictive studies. In studies from about a decade ago, goodness-of-fit was most often indicated qualitatively (e.g. “correctly,” Hancock and Willgoose, 2001 and “good,” Heimsath et al., 1999). More recently, a quantitative expression of model performance is preferred. Cell-by-cell comparisons, comparisons of moving-window averages or of landscape-class averages can for instance be expressed as coefficients of determination (r2, Govers et al., 1996), Root Mean Square Errors (RMSE) or Model Efficiency Factors (MEF, Peeters et al., 2006). Results are typically better where overall landscape forms do not change much and form-process feedbacks are limited (for instance, soil redistribution studies) than where landscape form is very dynamic. This means that it is difficult to compare even quantitative goodness-of-fit indicators between study sites.
---
# 16 Quantitative Modeling of Landscape Evolution

Fig. 15 Simulated morphology of Ranger Uranium Mine dump after 0 (A), 500 (B) and 1000 (C) years. From Willgoose G and Riley S (1998) The long-term stability of engineered landforms of the ranger uranium mine, Northern Territory, Australia: Applications of a catchment evolution model. Earth Surface Processes and Landforms 23(3): 237–259.

Only two predictive landscape evolution modeling studies were found. Willgoose and Riley (1998) predicted the 1000-year evolution of the Ranger Uranium Mine in Australia, to assess whether government-imposed requirements for containment were met (Fig. 15). Temme et al. (2009) also extrapolated their earlier 50-thousand-year postdictive modeling efforts (Temme and Veldkamp, 2009) in a small catchment in South Africa for 1000 years into the future. Uncertainty was considered by varying LAPSUS model parameter values in a Monte Carlo-setup. They found that—accounting for this uncertainty—in most sub-zones of their catchment, landscape evolution under predicted changing climate differed significantly and substantially from landscape evolution under stable climate.

# 5 The future of landscape evolution modeling

Below, we venture a look into the future of landscape evolution modeling and point out a few directions for future research that we deem particularly important.

# 5.1 Self-organized criticality

As discussed above, recent modeling work has resulted in the suggestion that some geomorphic activity [sediment export from rivers, Coulthard and Van De Wiel (2007), or fluvial network density, Rinaldo et al. (1993)] displays self-organized criticality: the variable (e.g. sediment export) is independent from the external forcing (e.g. rainfall, discharge). This idea is a major threat to conventional interpretations of sedimentary records being caused by driving factors such as climate and land use change. Building on contributions from conceptual modeling (cause-effect narratives) and physical modeling (complex response), this major theoretical contribution can be uniquely attributed to quantitative modeling studies.

It is important to find out to which degree the simulation of self-organized criticality is a model artifact. If not, we must find out in how many geomorphic environments and variables it exists, and how significant its effect is over larger temporal and spatial timescales (Van De Wiel and Coulthard, 2010). Landscape evolution modeling is poised to play a large role in answering these crucial questions through its ability to simulate wide ranges of processes, environments and timescales.
---
# 5.2 Predictive studies, inversion and uncertainty analysis

The increasing availability of decadal, centennial and millennial scale datasets for landscape evolution model calibration makes it possible that our models of landscape evolution at shorter timescales are used less descriptively and more predictively. Therefore, their results may become more useful for policy makers (Korup, 2002). This requires clarity about the value of predictions.

For this purpose, sensitivity analysis and uncertainty analysis are becoming more important. (Beven, 2009) argued that uncertainty analysis is one of the directions in which most is to be gained for environmental models in general—perhaps more than from model improvement. We agree with that assertion, and moreover we argue that the procedural level of models should be included in such sensitivity and uncertainty analyses (Temme et al., 2011). Formerly, procedural decisions are hidden behind interfaces, making them inaccessible to users, but this is strongly improving through model frameworks like Landlab (Barnhart et al., 2020). The inclusion of procedural options in interface-based models is now allowing a wider appraisal of the sensitivity of model outputs. Procedural options in sensitivity analyses could include the type of digital landscape (DEM/TIN), the type of flow routing, the choice of transport law and the method of dealing with sinks and flats. The development and sharing of models that offer these advanced sensitivity analysis opportunities, through efforts such as CSDMS (Voinov et al., 2010) should continue.

Varying parameter values to assess their effect on model outputs or goodness-of-fit indicators is often easily done through Monte-Carlo analysis. In Monte-Carlo analysis, many (sets of) parameter values are randomly drawn from their (joint) probability distributions—and the model is run repeatedly with these (sets of) parameters. If no information about distributions is available, a uniform distribution is often used. Monte-Carlo analysis is computationally intensive due to repeating model runs, but has great potential in inversion, quantifying model uncertainty (when uncertainty of parameters is known) or model sensitivity (when uncertainty is not known).

Another possible contribution towards clarity about the validity of predictions is a more thorough exploration of the validity of boundary conditions and process descriptions when using models in environments or at spatial and temporal scales other than what they were designed for. End-user knowledge of such validity domains is an important objective and could be realized through model meta-information.

# 5.3 Feedbacks to and from other fields

Feedbacks from traditional geomorphology to vegetation currently receive much attention (e.g. Baas and Nield, 2007; Buis et al., 2010; Istanbulluoglu, 2009a; Istanbulluoglu and Bras, 2005; Tucker and Hancock, 2010). These feedbacks form a crucial field of investigation that will likely grow in future years. It is likely that non-linear interactions of vegetation with geomorphic processes will increase our understanding of the complex-systems properties of landscapes, and perhaps of the predictability of landscape evolution.

Feedbacks can be found elsewhere, too (Murray et al., 2009; Paola et al., 2006). Wainwright (2008) offers an interesting road to quantifying the role of humans as land-users and constructors at the large spatial extents where inevitable small-scale probabilistic effects of his approach can be lumped together. Land use change models may offer an additional way of accounting for human activity on the landscape and on vegetation (e.g. Verburg and Overmars, 2009). Interactions between large-scale land use and landscape have already been explored (Claessens et al., 2009) and have strong potential. Further inclusions of soil development processes into soil-landscape evolution models can increase the range of land use impacts on landscape evolution that can be simulated.

# 5.4 Validation with whole-landscape datasets

Finally, it remains crucial to focus on calibration and validation of landscape evolution models. Calibration and validation datasets that combine different types of data (for instance total altitude change at a number of sites, sediment export from a catchment as a whole through time and the current rate of erosion of the water-divides) offer exciting opportunities for validation. This has long been recognized as an important issue, and calibration and validation datasets at the millennia and shorter timescales are—although rare—coming available for model tests, also through smarter selection of case studies in landscapes that offer validation opportunities (Tucker, 2009). Millennia-scale postdictive studies are currently rare, but as more datasets become available, such studies will increase in number—conceivably leading to better models (Temme et al., 2017).

At the shorter timescale, a crucial role will likely be played by the Critical Zone Observatories in the United States and some comparable observatories in Europe. The role that such observatories can play in our understanding of landscape evolution at the larger timescale, is still unknown and may be limited where and when evolution is slow or rare events play large roles. Still, the wealth of landscape process, vegetation, meteorological and other data that will be available from such observatories should also lead to an increase in model calibration and validation studies—especially because the Observatories are situated in a wide range of environments.
---