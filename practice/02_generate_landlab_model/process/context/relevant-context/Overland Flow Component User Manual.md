Title: Overland Flow Component User Manual

URL Source: https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html

Markdown Content:
Overland Flow Component User Manual - landlab
=============== 

   

Hide navigation sidebar

Hide table of contents sidebar

_Landlab 2.9 released!_

Toggle site navigation sidebar

[landlab](https://landlab.readthedocs.io/en/v2.9.2/index.html)

Toggle Light / Dark / Auto color theme

Toggle table of contents sidebar

[![Image 6: Logo](https://landlab.readthedocs.io/en/v2.9.2/_static/landlab_logo.png)](https://landlab.readthedocs.io/en/v2.9.2/index.html)

  

Getting Started

*   [Install](https://landlab.readthedocs.io/en/v2.9.2/installation.html)
*   [Getting started](https://landlab.readthedocs.io/en/v2.9.2/getting_started/index.html)
*   [User Guide](https://landlab.readthedocs.io/en/v2.9.2/user_guide/index.html)[ ] 
    
    Toggle navigation of User Guide
    
    *   [Grid & Component reference](https://landlab.readthedocs.io/en/v2.9.2/user_guide/reference/index.html)[ ] 
        
        Toggle navigation of Grid & Component reference
        
        *   [Landlab Grids](https://landlab.readthedocs.io/en/v2.9.2/user_guide/reference/grid.html)[ ] 
            
            Toggle navigation of Landlab Grids
            
            *   [landlab.grid.base](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.base.html)
            *   [landlab.grid.create](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.create.html)
            *   [landlab.grid.decorators](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.decorators.html)
            *   [landlab.grid.diagonals](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.diagonals.html)
            *   [landlab.grid.divergence](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.divergence.html)
            *   [landlab.grid.gradients](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.gradients.html)
            *   [landlab.grid.grid\_funcs](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.grid_funcs.html)
            *   [landlab.grid.linkstatus](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.linkstatus.html)
            *   [landlab.grid.mappers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.mappers.html)
            *   [landlab.grid.nodestatus](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.nodestatus.html)
            *   [landlab.grid.raster\_aspect](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster_aspect.html)
            *   [landlab.grid.raster\_funcs](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster_funcs.html)
            *   [landlab.grid.raster\_gradients](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster_gradients.html)
            *   [landlab.grid.raster\_mappers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster_mappers.html)
            *   [landlab.grid.raster\_set\_status](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster_set_status.html)
            *   [landlab.grid.warnings](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.warnings.html)
            *   [landlab.grid.base](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.base.html)
            *   [landlab.grid.raster](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster.html)
            *   [landlab.grid.voronoi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.voronoi.html)
            *   [landlab.grid.framed\_voronoi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.framed_voronoi.html)
            *   [landlab.grid.hex](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.hex.html)
            *   [landlab.grid.radial](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.radial.html)
            *   [landlab.grid.network](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.network.html)
            *   [landlab.grid.icosphere](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.icosphere.html)
            *   [landlab.grid.unstructured](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.unstructured.html)[ ] 
                
                Toggle navigation of landlab.grid.unstructured
                
                *   [base](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.unstructured.base.html)
                *   [cells](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.unstructured.cells.html)
                *   [links](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.unstructured.links.html)
                *   [nodes](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.unstructured.nodes.html)
                *   [status](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.unstructured.status.html)
        *   [Layers](https://landlab.readthedocs.io/en/v2.9.2/user_guide/reference/layers.html)[ ] 
            
            Toggle navigation of Layers
            
            *   [landlab.layers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.layers.html)[ ] 
                
                Toggle navigation of landlab.layers
                
                *   [ext](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.layers.ext.html)
                *   [eventlayers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.layers.eventlayers.html)
                *   [materiallayers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.layers.materiallayers.html)
        *   [landlab.components.lithology.lithology](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.lithology.lithology.html)
        *   [landlab.components.lithology.litholayers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.lithology.litholayers.html)
        *   [Values](https://landlab.readthedocs.io/en/v2.9.2/user_guide/reference/values.html)[ ] 
            
            Toggle navigation of Values
            
            *   [landlab.values](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.values.html)[ ] 
                
                Toggle navigation of landlab.values
                
                *   [synthetic](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.values.synthetic.html)
        *   [Components](https://landlab.readthedocs.io/en/v2.9.2/user_guide/reference/components.html)[ ] 
            
            Toggle navigation of Components
            
            *   [landlab.components.diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.diffusion.html)[ ] 
                
                Toggle navigation of landlab.components.diffusion
                
                *   [diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.diffusion.diffusion.html)
            *   [landlab.components.nonlinear\_diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.nonlinear_diffusion.html)[ ] 
                
                Toggle navigation of landlab.components.nonlinear\_diffusion
                
                *   [Perron\_nl\_diffuse](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.nonlinear_diffusion.Perron_nl_diffuse.html)
            *   [landlab.components.depth\_dependent\_diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depth_dependent_diffusion.html)[ ] 
                
                Toggle navigation of landlab.components.depth\_dependent\_diffusion
                
                *   [hillslope\_depth\_dependent\_linear\_flux](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depth_dependent_diffusion.hillslope_depth_dependent_linear_flux.html)
            *   [landlab.components.transport\_length\_diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.transport_length_diffusion.html)[ ] 
                
                Toggle navigation of landlab.components.transport\_length\_diffusion
                
                *   [transport\_length\_hillslope\_diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.transport_length_diffusion.transport_length_hillslope_diffusion.html)
            *   [landlab.components.taylor\_nonlinear\_hillslope\_flux](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.taylor_nonlinear_hillslope_flux.html)[ ] 
                
                Toggle navigation of landlab.components.taylor\_nonlinear\_hillslope\_flux
                
                *   [taylor\_nonlinear\_hillslope\_flux](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.taylor_nonlinear_hillslope_flux.taylor_nonlinear_hillslope_flux.html)
            *   [landlab.components.depth\_dependent\_taylor\_soil\_creep](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depth_dependent_taylor_soil_creep.html)[ ] 
                
                Toggle navigation of landlab.components.depth\_dependent\_taylor\_soil\_creep
                
                *   [hillslope\_depth\_dependent\_taylor\_flux](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depth_dependent_taylor_soil_creep.hillslope_depth_dependent_taylor_flux.html)
            *   [landlab.components.threshold\_eroder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.threshold_eroder.html)[ ] 
                
                Toggle navigation of landlab.components.threshold\_eroder
                
                *   [threshold\_eroder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.threshold_eroder.threshold_eroder.html)
            *   [landlab.components.concentration\_tracker](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.concentration_tracker.html)[ ] 
                
                Toggle navigation of landlab.components.concentration\_tracker
                
                *   [concentration\_tracker\_for\_diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.concentration_tracker.concentration_tracker_for_diffusion.html)
            *   [landlab.components.stream\_power](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.stream_power.html)[ ] 
                
                Toggle navigation of landlab.components.stream\_power
                
                *   [fastscape\_stream\_power](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.stream_power.fastscape_stream_power.html)
                *   [sed\_flux\_dep\_incision](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.stream_power.sed_flux_dep_incision.html)
                *   [stream\_power](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.stream_power.stream_power.html)
                *   [stream\_power\_smooth\_threshold](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.stream_power.stream_power_smooth_threshold.html)
            *   [landlab.components.detachment\_ltd\_erosion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.detachment_ltd_erosion.html)[ ] 
                
                Toggle navigation of landlab.components.detachment\_ltd\_erosion
                
                *   [generate\_detachment\_ltd\_erosion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.detachment_ltd_erosion.generate_detachment_ltd_erosion.html)
                *   [generate\_erosion\_by\_depth\_slope](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.detachment_ltd_erosion.generate_erosion_by_depth_slope.html)
            *   [landlab.components.erosion\_deposition](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.erosion_deposition.html)[ ] 
                
                Toggle navigation of landlab.components.erosion\_deposition
                
                *   [erosion\_deposition](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.erosion_deposition.erosion_deposition.html)
                *   [generalized\_erosion\_deposition](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.erosion_deposition.generalized_erosion_deposition.html)
                *   [shared\_stream\_power](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.erosion_deposition.shared_stream_power.html)
            *   [landlab.components.space](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.space.html)[ ] 
                
                Toggle navigation of landlab.components.space
                
                *   [space](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.space.space.html)
                *   [space\_large\_scale\_eroder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.space.space_large_scale_eroder.html)
            *   [landlab.components.network\_sediment\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.network_sediment_transporter.html)[ ] 
                
                Toggle navigation of landlab.components.network\_sediment\_transporter
                
                *   [bed\_parcel\_initializers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.network_sediment_transporter.bed_parcel_initializers.html)
                *   [network\_sediment\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.network_sediment_transporter.network_sediment_transporter.html)
                *   [sediment\_pulser\_at\_links](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.network_sediment_transporter.sediment_pulser_at_links.html)
                *   [sediment\_pulser\_base](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.network_sediment_transporter.sediment_pulser_base.html)
                *   [sediment\_pulser\_each\_parcel](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.network_sediment_transporter.sediment_pulser_each_parcel.html)
            *   [landlab.components.gravel\_river\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.gravel_river_transporter.html)[ ] 
                
                Toggle navigation of landlab.components.gravel\_river\_transporter
                
                *   [gravel\_river\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.gravel_river_transporter.gravel_river_transporter.html)
            *   [landlab.components.area\_slope\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.area_slope_transporter.html)[ ] 
                
                Toggle navigation of landlab.components.area\_slope\_transporter
                
                *   [area\_slope\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.area_slope_transporter.area_slope_transporter.html)
            *   [landlab.components.gravel\_bedrock\_eroder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.gravel_bedrock_eroder.html)[ ] 
                
                Toggle navigation of landlab.components.gravel\_bedrock\_eroder
                
                *   [gravel\_bedrock\_eroder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.gravel_bedrock_eroder.gravel_bedrock_eroder.html)
            *   [landlab.components.flow\_director](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.html)[ ] 
                
                Toggle navigation of landlab.components.flow\_director
                
                *   [flow\_direction\_DN](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_direction_DN.html)
                *   [flow\_direction\_dinf](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_direction_dinf.html)
                *   [flow\_direction\_mfd](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_direction_mfd.html)
                *   [flow\_director](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director.html)
                *   [flow\_director\_d8](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director_d8.html)
                *   [flow\_director\_dinf](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director_dinf.html)
                *   [flow\_director\_mfd](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director_mfd.html)
                *   [flow\_director\_steepest](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director_steepest.html)
                *   [flow\_director\_to\_many](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director_to_many.html)
                *   [flow\_director\_to\_one](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director_to_one.html)
            *   [landlab.components.flow\_accum](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_accum.html)[ ] 
                
                Toggle navigation of landlab.components.flow\_accum
                
                *   [flow\_accum\_bw](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_accum.flow_accum_bw.html)
                *   [flow\_accum\_to\_n](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_accum.flow_accum_to_n.html)
                *   [flow\_accumulator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_accum.flow_accumulator.html)
                *   [lossy\_flow\_accumulator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_accum.lossy_flow_accumulator.html)
            *   [landlab.components.depression\_finder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depression_finder.html)[ ] 
                
                Toggle navigation of landlab.components.depression\_finder
                
                *   [floodstatus](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depression_finder.floodstatus.html)
                *   [lake\_mapper](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depression_finder.lake_mapper.html)
            *   [landlab.components.lake\_fill](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.lake_fill.html)[ ] 
                
                Toggle navigation of landlab.components.lake\_fill
                
                *   [lake\_fill\_barnes](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.lake_fill.lake_fill_barnes.html)
            *   [landlab.components.priority\_flood\_flow\_router](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.priority_flood_flow_router.html)[ ] 
                
                Toggle navigation of landlab.components.priority\_flood\_flow\_router
                
                *   [priority\_flood\_flow\_router](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.priority_flood_flow_router.priority_flood_flow_router.html)
            *   [landlab.components.sink\_fill](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.sink_fill.html)[ ] 
                
                Toggle navigation of landlab.components.sink\_fill
                
                *   [fill\_sinks](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.sink_fill.fill_sinks.html)
                *   [sink\_fill\_barnes](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.sink_fill.sink_fill_barnes.html)
            *   [landlab.components.overland\_flow](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.html)[ ] 
                
                Toggle navigation of landlab.components.overland\_flow
                
                *   [generate\_overland\_flow\_Bates](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.generate_overland_flow_Bates.html)
                *   [generate\_overland\_flow\_deAlmeida](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.generate_overland_flow_deAlmeida.html)
                *   [generate\_overland\_flow\_implicit\_kinwave](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.generate_overland_flow_implicit_kinwave.html)
                *   [generate\_overland\_flow\_kinwave](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.generate_overland_flow_kinwave.html)
                *   [kinematic\_wave\_rengers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.kinematic_wave_rengers.html)
                *   [linear\_diffusion\_overland\_flow\_router](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.linear_diffusion_overland_flow_router.html)
            *   [landlab.components.tidal\_flow](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.tidal_flow.html)[ ] 
                
                Toggle navigation of landlab.components.tidal\_flow
                
                *   [tidal\_flow\_calculator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.tidal_flow.tidal_flow_calculator.html)
            *   [landlab.components.radiation](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.radiation.html)[ ] 
                
                Toggle navigation of landlab.components.radiation
                
                *   [radiation](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.radiation.radiation.html)
            *   [landlab.components.pet](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.pet.html)[ ] 
                
                Toggle navigation of landlab.components.pet
                
                *   [potential\_evapotranspiration\_field](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.pet.potential_evapotranspiration_field.html)
            *   [landlab.components.soil\_moisture](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.soil_moisture.html)[ ] 
                
                Toggle navigation of landlab.components.soil\_moisture
                
                *   [infiltrate\_soil\_green\_ampt](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.soil_moisture.infiltrate_soil_green_ampt.html)
                *   [soil\_moisture\_dynamics](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.soil_moisture.soil_moisture_dynamics.html)
            *   [landlab.components.groundwater](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.groundwater.html)[ ] 
                
                Toggle navigation of landlab.components.groundwater
                
                *   [dupuit\_percolator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.groundwater.dupuit_percolator.html)
            *   [landlab.components.bedrock\_landslider](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.bedrock_landslider.html)[ ] 
                
                Toggle navigation of landlab.components.bedrock\_landslider
                
                *   [bedrock\_landslider](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.bedrock_landslider.bedrock_landslider.html)
            *   [landlab.components.landslides](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.landslides.html)[ ] 
                
                Toggle navigation of landlab.components.landslides
                
                *   [landslide\_probability](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.landslides.landslide_probability.html)
            *   [landlab.components.dimensionless\_discharge](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.dimensionless_discharge.html)[ ] 
                
                Toggle navigation of landlab.components.dimensionless\_discharge
                
                *   [dimensionless\_discharge](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.dimensionless_discharge.dimensionless_discharge.html)
            *   [landlab.components.vegetation\_dynamics](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.vegetation_dynamics.html)[ ] 
                
                Toggle navigation of landlab.components.vegetation\_dynamics
                
                *   [vegetation\_dynamics](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.vegetation_dynamics.vegetation_dynamics.html)
            *   [landlab.components.plant\_competition\_ca](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.plant_competition_ca.html)[ ] 
                
                Toggle navigation of landlab.components.plant\_competition\_ca
                
                *   [plant\_competition\_ca](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.plant_competition_ca.plant_competition_ca.html)
            *   [landlab.components.species\_evolution](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.html)[ ] 
                
                Toggle navigation of landlab.components.species\_evolution
                
                *   [base\_taxon](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.base_taxon.html)
                *   [record](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.record.html)
                *   [species\_evolver](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.species_evolver.html)
                *   [zone](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.zone.html)
                *   [zone\_controller](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.zone_controller.html)
                *   [zone\_taxon](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.zone_taxon.html)
            *   [landlab.components.uniform\_precip](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.uniform_precip.html)[ ] 
                
                Toggle navigation of landlab.components.uniform\_precip
                
                *   [generate\_uniform\_precip](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.uniform_precip.generate_uniform_precip.html)
            *   [landlab.components.spatial\_precip](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.spatial_precip.html)[ ] 
                
                Toggle navigation of landlab.components.spatial\_precip
                
                *   [generate\_spatial\_precip](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.spatial_precip.generate_spatial_precip.html)
            *   [landlab.components.weathering](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.weathering.html)[ ] 
                
                Toggle navigation of landlab.components.weathering
                
                *   [exponential\_weathering](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.weathering.exponential_weathering.html)
                *   [exponential\_weathering\_integrated](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.weathering.exponential_weathering_integrated.html)
            *   [landlab.components.carbonate](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.carbonate.html)[ ] 
                
                Toggle navigation of landlab.components.carbonate
                
                *   [carbonate\_producer](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.carbonate.carbonate_producer.html)
            *   [landlab.components.marine\_sediment\_transport](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.marine_sediment_transport.html)[ ] 
                
                Toggle navigation of landlab.components.marine\_sediment\_transport
                
                *   [simple\_submarine\_diffuser](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.marine_sediment_transport.simple_submarine_diffuser.html)
            *   [landlab.components.advection](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.advection.html)[ ] 
                
                Toggle navigation of landlab.components.advection
                
                *   [advection\_solver\_tvd](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.advection.advection_solver_tvd.html)
                *   [flux\_limiters](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.advection.flux_limiters.html)
            *   [landlab.components.steepness\_index](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.steepness_index.html)[ ] 
                
                Toggle navigation of landlab.components.steepness\_index
                
                *   [channel\_steepness](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.steepness_index.channel_steepness.html)
            *   [landlab.components.chi\_index](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.chi_index.html)[ ] 
                
                Toggle navigation of landlab.components.chi\_index
                
                *   [channel\_chi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.chi_index.channel_chi.html)
            *   [landlab.components.drainage\_density](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.drainage_density.html)[ ] 
                
                Toggle navigation of landlab.components.drainage\_density
                
                *   [drainage\_density](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.drainage_density.drainage_density.html)
            *   [landlab.components.profiler.channel\_profiler](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.profiler.channel_profiler.html)
            *   [landlab.components.profiler.trickle\_down\_profiler](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.profiler.trickle_down_profiler.html)
            *   [landlab.components.hack\_calculator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.hack_calculator.html)[ ] 
                
                Toggle navigation of landlab.components.hack\_calculator
                
                *   [hack\_calculator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.hack_calculator.hack_calculator.html)
            *   [landlab.components.hand\_calculator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.hand_calculator.html)[ ] 
                
                Toggle navigation of landlab.components.hand\_calculator
                
                *   [hand\_calculator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.hand_calculator.hand_calculator.html)
            *   [landlab.components.flexure](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flexure.html)[ ] 
                
                Toggle navigation of landlab.components.flexure
                
                *   [flexure](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flexure.flexure.html)
                *   [flexure\_1d](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flexure.flexure_1d.html)
                *   [funcs](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flexure.funcs.html)
            *   [landlab.components.gflex](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.gflex.html)[ ] 
                
                Toggle navigation of landlab.components.gflex
                
                *   [flexure](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.gflex.flexure.html)
            *   [landlab.components.normal\_fault](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.normal_fault.html)[ ] 
                
                Toggle navigation of landlab.components.normal\_fault
                
                *   [normal\_fault](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.normal_fault.normal_fault.html)
            *   [landlab.components.tectonics](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.tectonics.html)[ ] 
                
                Toggle navigation of landlab.components.tectonics
                
                *   [listric\_kinematic\_extender](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.tectonics.listric_kinematic_extender.html)
            *   [landlab.components.fire\_generator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.fire_generator.html)[ ] 
                
                Toggle navigation of landlab.components.fire\_generator
                
                *   [generate\_fire](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.fire_generator.generate_fire.html)
            *   [landlab.components.fracture\_grid](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.fracture_grid.html)[ ] 
                
                Toggle navigation of landlab.components.fracture\_grid
                
                *   [fracture\_grid](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.fracture_grid.fracture_grid.html)
    *   [List of Components](https://landlab.readthedocs.io/en/v2.9.2/user_guide/component_list.html)
    *   [List of Landlab Fields](https://landlab.readthedocs.io/en/v2.9.2/user_guide/field_definitions.html)
    *   [List of Grid Methods](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid_summary.html)[ ] 
        
        Toggle navigation of List of Grid Methods
        
        *   [Nodes, Links, and Patches](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid_methods/01_nodes_links_patches.html)
        *   [Corners, Faces, and Cells](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid_methods/02_corners_faces_cells.html)
        *   [Boundary conditions](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid_methods/03_boundary_conditions.html)
        *   [Subsets of elements](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid_methods/04_element_subsets.html)
        *   [Mapping between elements](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid_methods/05_element_mapping.html)
        *   [Gradients, fluxes, and divergences](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid_methods/06_gradients.html)
        *   [Surface analysis](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid_methods/07_surface_analysis.html)
        *   [Fields](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid_methods/08_fields.html)
        *   [Uncategorized or Deprecated](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid_methods/99_uncategorized.html)
    *   [Introduction to Landlab’s Gridding Library](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid.html)
    *   [The Component Library](https://landlab.readthedocs.io/en/v2.9.2/user_guide/components.html)
    *   [What goes into a Landlab model?](https://landlab.readthedocs.io/en/v2.9.2/user_guide/build_a_model.html)
    *   [How Landlab Is/Is Not Unit Agnostic](https://landlab.readthedocs.io/en/v2.9.2/user_guide/units.html)
    *   [Time steps](https://landlab.readthedocs.io/en/v2.9.2/user_guide/time_steps.html)
    *   [Frequently Asked Questions](https://landlab.readthedocs.io/en/v2.9.2/user_guide/faq.html)
    *   [Overland Flow Component User Manual](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#)
    *   [CellLab-CTS User Guide](https://landlab.readthedocs.io/en/v2.9.2/user_guide/cell_lab_user_guide.html)
*   [Tutorials](https://landlab.readthedocs.io/en/v2.9.2/tutorials/index.html)[ ] 
    
    Toggle navigation of Tutorials
    
    *   [Gallery](https://landlab.readthedocs.io/en/v2.9.2/generated/tutorials/index.html)[ ] 
        
        Toggle navigation of Gallery
        
        *   [TVD advection solver and related functions](https://landlab.readthedocs.io/en/v2.9.2/tutorials/advection/overview_of_advection_solver.html)
        *   [Agent-based modeling with Landlab and Mesa](https://landlab.readthedocs.io/en/v2.9.2/tutorials/agent_based_modeling/README.html)
        *   [Coupling a Landlab groundwater with a Mesa agent-based model](https://landlab.readthedocs.io/en/v2.9.2/tutorials/agent_based_modeling/groundwater/landlab_mesa_groundwater_pumping.html)
        *   [Wolf-Sheep-Grass Model with Soil Creep](https://landlab.readthedocs.io/en/v2.9.2/tutorials/agent_based_modeling/wolf_sheep/wolf_sheep_with_soil_creep.html)
        *   [Setting Boundary Conditions: interior rectangle](https://landlab.readthedocs.io/en/v2.9.2/tutorials/boundary_conditions/set_BCs_from_xy.html)
        *   [Setting Boundary Conditions on the Perimeter of a Raster.](https://landlab.readthedocs.io/en/v2.9.2/tutorials/boundary_conditions/set_BCs_on_raster_perimeter.html)
        *   [Setting Boundary Conditions on a Voronoi.](https://landlab.readthedocs.io/en/v2.9.2/tutorials/boundary_conditions/set_BCs_on_voronoi.html)
        *   [Setting watershed boundary conditions on a raster grid](https://landlab.readthedocs.io/en/v2.9.2/tutorials/boundary_conditions/set_watershed_BCs_raster.html)
        *   [The Carbonate Producer component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/carbonates/carbonate_producer.html)
        *   [Getting to know the Landlab component library](https://landlab.readthedocs.io/en/v2.9.2/tutorials/component_tutorial/component_tutorial.html)
        *   [DataRecord Tutorial](https://landlab.readthedocs.io/en/v2.9.2/tutorials/data_record/DataRecord_tutorial.html)
        *   [Tutorial For Cellular Automaton Vegetation Model Coupled With Ecohydrologic Model](https://landlab.readthedocs.io/en/v2.9.2/tutorials/ecohydrology/cellular_automaton_vegetation_DEM/cellular_automaton_vegetation_DEM.html)
        *   [Tutorial For Cellular Automaton Vegetation Model Coupled With Ecohydrologic Model](https://landlab.readthedocs.io/en/v2.9.2/tutorials/ecohydrology/cellular_automaton_vegetation_flat_surface/cellular_automaton_vegetation_flat_domain.html)
        *   [Introduction to Landlab: Creating a simple 2D scarp diffusion model](https://landlab.readthedocs.io/en/v2.9.2/tutorials/fault_scarp/landlab-fault-scarp.html)
        *   [Understanding and working with Landlab data fields](https://landlab.readthedocs.io/en/v2.9.2/tutorials/fields/working_with_fields.html)
        *   [Using the Landlab 1D flexure component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/flexure/flexure_1d.html)
        *   [Using the Landlab flexure component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/flexure/lots_of_loads.html)
        *   [Landscape evolution model with Priority flood and Space\_v2](https://landlab.readthedocs.io/en/v2.9.2/tutorials/flow_direction_and_accumulation/PriorityFlood_LandscapeEvolutionModel.html)
        *   [Introduction to priority flood component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/flow_direction_and_accumulation/PriorityFlood_realDEMs.html)
        *   [Comparison of FlowDirectors](https://landlab.readthedocs.io/en/v2.9.2/tutorials/flow_direction_and_accumulation/compare_FlowDirectors.html)
        *   [Introduction to the FlowAccumulator](https://landlab.readthedocs.io/en/v2.9.2/tutorials/flow_direction_and_accumulation/the_FlowAccumulator.html)
        *   [Introduction to FlowDirectors](https://landlab.readthedocs.io/en/v2.9.2/tutorials/flow_direction_and_accumulation/the_FlowDirectors.html)
        *   [Introduction to PriorityFloodFlowRouter (priorityFlood filler, director and accumulator)](https://landlab.readthedocs.io/en/v2.9.2/tutorials/flow_direction_and_accumulation/the_Flow_Director_Accumulator_PriorityFlood.html)
        *   [Using the Landlab `FractureGridGenerator` component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/fracture_grid/using_fracture_grid.html)
        *   [Using Landlab’s gradient and flux divergence functions](https://landlab.readthedocs.io/en/v2.9.2/tutorials/gradient_and_divergence/gradient_and_divergence.html)
        *   [Diverse grid classes](https://landlab.readthedocs.io/en/v2.9.2/tutorials/grids/diverse_grid_classes.html)
        *   [What happens when you create a grid object?](https://landlab.readthedocs.io/en/v2.9.2/tutorials/grids/grid_object_demo.html)
        *   [How to create and visualize a Landlab Icosphere Grid](https://landlab.readthedocs.io/en/v2.9.2/tutorials/grids/how_to_create_and_viz_icosphere_grid.html)
        *   [Icosphere example models](https://landlab.readthedocs.io/en/v2.9.2/tutorials/grids/icosphere_example_models.html)
        *   [Modeling groundwater flow in a conceptual catchment](https://landlab.readthedocs.io/en/v2.9.2/tutorials/groundwater/groundwater_flow.html)
        *   [Component Overview: `DepthDependentTaylorDiffuser`](https://landlab.readthedocs.io/en/v2.9.2/tutorials/hillslope_geomorphology/depth_dependent_taylor_diffuser/depth_dependent_taylor_diffuser.html)
        *   [Component Overview: `TaylorNonLinearDiffuser`](https://landlab.readthedocs.io/en/v2.9.2/tutorials/hillslope_geomorphology/taylor_diffuser/taylor_diffuser.html)
        *   [The transport-length hillslope diffuser](https://landlab.readthedocs.io/en/v2.9.2/tutorials/hillslope_geomorphology/transport-length_hillslope_diffuser/TLHDiff_tutorial.html)
        *   [The Basics](https://landlab.readthedocs.io/en/v2.9.2/tutorials/hillslope_geomorphology/transport-length_hillslope_diffuser/TLHDiff_tutorial.html#The-Basics)
        *   [Example 1:](https://landlab.readthedocs.io/en/v2.9.2/tutorials/hillslope_geomorphology/transport-length_hillslope_diffuser/TLHDiff_tutorial.html#Example-1:)
        *   [Example 2:](https://landlab.readthedocs.io/en/v2.9.2/tutorials/hillslope_geomorphology/transport-length_hillslope_diffuser/TLHDiff_tutorial.html#Example-2:)
        *   [Unit tests and parameterization for `AreaSlopeTransporter`](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/area_slope_transporter/einstein-brown.html)
        *   [Example of a transport-limited LEM using `AreaSlopeTransporter`](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/area_slope_transporter/transport-limited-LEM-example.html)
        *   [Introduction to the `ErosionDeposition` component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/erosion_deposition/erosion_deposition_component.html)
        *   [Using the Landlab Shared Stream Power Model](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/erosion_deposition/shared_stream_power.html)
        *   [Run with Transient Uplift](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/erosion_deposition/shared_stream_power.html#Run-with-Transient-Uplift)
        *   [Unit Tests for the Landlab GravelBedrockEroder Component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/gravel_bedrock_eroder/gravel_bedrock_transporter_unit_tests.html)
        *   [The Landlab GravelRiverTransporter Component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/gravel_river_transporter/gravel_river_transporter.html)
        *   [HyLands: modelling the evolution of landscapes and mass movements](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/hylands/HyLandsTutorial.html)
        *   [Adding a discharge point source to a LEM](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/river_input_lem/adding_discharge_point_source_to_a_lem.html)
        *   [The `StreamPowerSmoothThresholdEroder` component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/smooth_threshold_eroder/stream_power_smooth_threshold_eroder.html)
        *   [User guide and example for the Landlab SPACE\_large\_Scale\_eroder component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/space/SPACE_large_scale_eroder_user_guide_and_examples.html)
        *   [User guide and example for the Landlab SPACE component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/space/SPACE_user_guide_and_examples.html)
        *   [User guide and example for the Landlab threshold\_eroder component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/landscape_evolution/threshold_eroder/threshold_eroder.html)
        *   [Introduction to the Lithology and LithoLayers objects](https://landlab.readthedocs.io/en/v2.9.2/tutorials/lithology/lithology_and_litholayers.html)
        *   [Tips on Writing Landlab Components](https://landlab.readthedocs.io/en/v2.9.2/tutorials/making_components/component_design_tips.html)
        *   [How to write a Landlab component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/making_components/making_components.html)
        *   [Mapping values between grid elements](https://landlab.readthedocs.io/en/v2.9.2/tutorials/mappers/mappers.html)
        *   [Using the Landlab SimpleSubmarineDiffuser component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/marine_sediment_transport/simple_submarine_diffuser_tutorial.html)
        *   [Landslide Runout Animation](https://landlab.readthedocs.io/en/v2.9.2/tutorials/mass_wasting_runout/landslide_runout_animation.html)
        *   [Synthetic landscape animation](https://landlab.readthedocs.io/en/v2.9.2/tutorials/mass_wasting_runout/synthetic_landscape_animation.html)
        *   [Building a matrix for numerical methods using a Landlab grid](https://landlab.readthedocs.io/en/v2.9.2/tutorials/matrix_creation/numerical_matrix_building_tools.html)
        *   [Using the Landlab BedParcelInitializer components to initialize river bed sediment parcels for the NetworkSedimentTransporter component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/network_sediment_transporter/bed_parcel_initializer.html)
        *   [Create A Network Grid from Raster Grid](https://landlab.readthedocs.io/en/v2.9.2/tutorials/network_sediment_transporter/create_networkgrid_from_rastergrid.html)
        *   [Using plotting tools associated with the Landlab NetworkSedimentTransporter component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/network_sediment_transporter/network_plotting_examples.html)
        *   [Using the Landlab NetworkSedimentTransporter component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/network_sediment_transporter/network_sediment_transporter.html)
        *   [Using USGS NHDPlus HR Datasets With the Landlab NetworkSedimentTransporter Component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/network_sediment_transporter/network_sediment_transporter_NHDPlus_HR_network.html)
        *   [Using the Landlab NetworkSedimentTransporter component starting with a shapefile river network](https://landlab.readthedocs.io/en/v2.9.2/tutorials/network_sediment_transporter/network_sediment_transporter_shapefile_network.html)
        *   [Profiling and Scaling Analysis of the NetworkSedimentTransporter](https://landlab.readthedocs.io/en/v2.9.2/tutorials/network_sediment_transporter/nst_scaling_profiling.html)
        *   [Generate a Network Model Grid on an OpenTopography DEM](https://landlab.readthedocs.io/en/v2.9.2/tutorials/network_sediment_transporter/run_network_generator_OpenTopoDEM.html)
        *   [Using SedimentPulserAtLinks to add sediment parcels to a channel network](https://landlab.readthedocs.io/en/v2.9.2/tutorials/network_sediment_transporter/sediment_pulser_at_links.html)
        *   [Using SedimentPulserEachParcel to add sediment parcels to a channel network](https://landlab.readthedocs.io/en/v2.9.2/tutorials/network_sediment_transporter/sediment_pulser_each_parcel.html)
        *   [Introduction to the NormalFault component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/normal_fault/normal_fault_component_tutorial.html)
        *   [Writing with legacy vtk files](https://landlab.readthedocs.io/en/v2.9.2/tutorials/output/writing_legacy_vtk_files.html)
        *   [A coupled rainfall-runoff model in Landlab](https://landlab.readthedocs.io/en/v2.9.2/tutorials/overland_flow/coupled_rainfall_runoff.html)
        *   [How to do “D4” pit-filling on a digital elevation model (DEM)](https://landlab.readthedocs.io/en/v2.9.2/tutorials/overland_flow/how_to_d4_pitfill_a_dem.html)
        *   [The deAlmeida Overland Flow Component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/overland_flow/overland_flow_driver.html)
        *   [The Implicit Kinematic Wave Overland Flow Component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/overland_flow/kinwave_implicit/kinwave_implicit_overland_flow.html)
        *   [The Linear Diffusion Overland Flow Router](https://landlab.readthedocs.io/en/v2.9.2/tutorials/overland_flow/linear_diffusion_overland_flow/linear_diffusion_overland_flow_router.html)
        *   [Components for modeling overland flow erosion](https://landlab.readthedocs.io/en/v2.9.2/tutorials/overland_flow/overland_flow_erosion/ol_flow_erosion_components.html)
        *   [Green-Ampt infiltration and kinematic wave overland flow](https://landlab.readthedocs.io/en/v2.9.2/tutorials/overland_flow/soil_infiltration_green_ampt/infilt_green_ampt_with_overland_flow.html)
        *   [Animate Landlab output](https://landlab.readthedocs.io/en/v2.9.2/tutorials/plotting/animate-landlab-output.html)
        *   [Plotting grid data with Landlab](https://landlab.readthedocs.io/en/v2.9.2/tutorials/plotting/landlab-plotting.html)
        *   [A super-brief intro to Python and NumPy](https://landlab.readthedocs.io/en/v2.9.2/tutorials/python_intro/python_intro.html)
        *   [How to read a DEM as a Landlab grid](https://landlab.readthedocs.io/en/v2.9.2/tutorials/reading_dem_into_landlab/reading_dem_into_landlab.html)
        *   [Introduction to the SpeciesEvolver component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/species_evolution/Introduction_to_SpeciesEvolver.html)
        *   [Using the Landlab ListricKinematicExtender component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/tectonics/listric_kinematic_extender.html)
        *   [Using the ChiFinder Component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/terrain_analysis/chi_finder/chi_finder.html)
        *   [Using the DrainageDensity Component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/terrain_analysis/drainage_density/drainage_density.html)
        *   [Application of the flow\_\_distance utility on a Sicilian basin](https://landlab.readthedocs.io/en/v2.9.2/tutorials/terrain_analysis/flow__distance_utility/application_of_flow__distance_utility.html)
        *   [Using the HackCalculator Component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/terrain_analysis/hack_calculator/hack_calculator.html)
        *   [Using the SteepnessFinder Component](https://landlab.readthedocs.io/en/v2.9.2/tutorials/terrain_analysis/steepness_finder/steepness_finder.html)
        *   [Tidal Flow Calculator](https://landlab.readthedocs.io/en/v2.9.2/tutorials/tidal_flow/tidal_flow_calculator.html)
        *   [Importing Landlab .obj format output into Blender](https://landlab.readthedocs.io/en/v2.9.2/tutorials/visualization/blender/landlab_to_blender.html)
        *   [Viewing Landlab output in ParaView](https://landlab.readthedocs.io/en/v2.9.2/tutorials/visualization/paraview/importing_landlab_netcdf_to_paraview.html)
*   [Teaching with Landlab](https://landlab.readthedocs.io/en/v2.9.2/teaching/index.html)[ ] 
    
    Toggle navigation of Teaching with Landlab
    
    *   [Getting started](https://landlab.readthedocs.io/en/v2.9.2/teaching/welcome_teaching.html)
    *   [Gallery](https://landlab.readthedocs.io/en/v2.9.2/generated/teaching/index.html)[ ] 
        
        Toggle navigation of Gallery
        
        *   [Quantifying river channel evolution with Landlab](https://landlab.readthedocs.io/en/v2.9.2/teaching/geomorphology_exercises/channels_streampower_notebooks/stream_power_channels_class_notebook.html)
        *   [Modeling Hillslopes and Channels with Landlab](https://landlab.readthedocs.io/en/v2.9.2/teaching/geomorphology_exercises/drainage_density_notebooks/drainage_density_class_notebook.html)
        *   [Linear diffusion exercise with Landlab](https://landlab.readthedocs.io/en/v2.9.2/teaching/geomorphology_exercises/hillslope_notebooks/hillslope_diffusion_class_notebook.html)
        *   [Using Landlab to explore a diffusive hillslope in the piedmont of North Carolina](https://landlab.readthedocs.io/en/v2.9.2/teaching/geomorphology_exercises/hillslope_notebooks/north_carolina_piedmont_hillslope_class_notebook.html)
        *   [Exploring rainfall driven hydrographs with Landlab](https://landlab.readthedocs.io/en/v2.9.2/teaching/surface_water_hydrology_exercises/overland_flow_notebooks/hydrograph_class_notebook.html)

Contributing

*   [Developer Install](https://landlab.readthedocs.io/en/v2.9.2/install/index.html)[ ] 
    
    Toggle navigation of Developer Install
    
    *   [Virtual Environments](https://landlab.readthedocs.io/en/v2.9.2/install/environments.html)
    *   [Updating and uninstalling](https://landlab.readthedocs.io/en/v2.9.2/install/update_uninstall.html)
*   [Developer Guide](https://landlab.readthedocs.io/en/v2.9.2/development/index.html)[ ] 
    
    Toggle navigation of Developer Guide
    
    *   [Guidelines for Contributing Code to Landlab](https://landlab.readthedocs.io/en/v2.9.2/development/contribution/index.html)[ ] 
        
        Toggle navigation of Guidelines for Contributing Code to Landlab
        
        *   [Develop your own component or utility](https://landlab.readthedocs.io/en/v2.9.2/development/contribution/develop_a_component.html)[ ] 
            
            Toggle navigation of Develop your own component or utility
            
            *   [Software Development Practices](https://landlab.readthedocs.io/en/v2.9.2/development/practices/index.html)[ ] 
                
                Toggle navigation of Software Development Practices
                
                *   [Develop with Git](https://landlab.readthedocs.io/en/v2.9.2/development/practices/develop_with_git.html)
                *   [Continuous Integration Practices](https://landlab.readthedocs.io/en/v2.9.2/development/practices/continuous_integration.html)
                *   [Style Guidelines and Enforcement](https://landlab.readthedocs.io/en/v2.9.2/development/practices/style_conventions.html)
                *   [Writing docstring and unit tests for your component (or utility)](https://landlab.readthedocs.io/en/v2.9.2/development/practices/writing_tests.html)
                *   [How to create a Landlab release](https://landlab.readthedocs.io/en/v2.9.2/development/practices/dev_guide_releases.html)
                *   [How Landlab Specifies Dependencies](https://landlab.readthedocs.io/en/v2.9.2/development/practices/dependencies.html)
        *   [Recommendations and Rules for User-Contributed Components](https://landlab.readthedocs.io/en/v2.9.2/development/contribution/recommendations.html)
        *   [Ongoing Development in Landlab](https://landlab.readthedocs.io/en/v2.9.2/development/contribution/ongoing_development.html)
        *   [Desired Contributions to Landlab](https://landlab.readthedocs.io/en/v2.9.2/development/contribution/desired_contributions.html)
        *   [Workflow to submit your Landlab contribution to Journal of Open Source Software](https://landlab.readthedocs.io/en/v2.9.2/development/contribution/joss_workflow.html)
    *   [Software Development Practices](https://landlab.readthedocs.io/en/v2.9.2/development/practices/index.html)[ ] 
        
        Toggle navigation of Software Development Practices
        
        *   [Develop with Git](https://landlab.readthedocs.io/en/v2.9.2/development/practices/develop_with_git.html)
        *   [Continuous Integration Practices](https://landlab.readthedocs.io/en/v2.9.2/development/practices/continuous_integration.html)
        *   [Style Guidelines and Enforcement](https://landlab.readthedocs.io/en/v2.9.2/development/practices/style_conventions.html)
        *   [Writing docstring and unit tests for your component (or utility)](https://landlab.readthedocs.io/en/v2.9.2/development/practices/writing_tests.html)
        *   [How to create a Landlab release](https://landlab.readthedocs.io/en/v2.9.2/development/practices/dev_guide_releases.html)
        *   [How Landlab Specifies Dependencies](https://landlab.readthedocs.io/en/v2.9.2/development/practices/dependencies.html)
    *   [Package Organization](https://landlab.readthedocs.io/en/v2.9.2/development/package_organization.html)
*   [API Reference](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.html)[ ] 
    
    Toggle navigation of API Reference
    
    *   [bmi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.bmi.html)[ ] 
        
        Toggle navigation of bmi
        
        *   [bmi\_bridge](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.bmi.bmi_bridge.html)
        *   [components](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.bmi.components.html)
        *   [standard\_names](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.bmi.standard_names.html)
    *   [ca](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.ca.html)[ ] 
        
        Toggle navigation of ca
        
        *   [boundaries](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.ca.boundaries.html)[ ] 
            
            Toggle navigation of boundaries
            
            *   [hex\_lattice\_tectonicizer](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.ca.boundaries.hex_lattice_tectonicizer.html)
        *   [celllab\_cts](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.ca.celllab_cts.html)
        *   [hex\_cts](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.ca.hex_cts.html)
        *   [oriented\_hex\_cts](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.ca.oriented_hex_cts.html)
        *   [oriented\_raster\_cts](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.ca.oriented_raster_cts.html)
        *   [raster\_cts](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.ca.raster_cts.html)
    *   [cmd](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.cmd.html)[ ] 
        
        Toggle navigation of cmd
        
        *   [authors](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.cmd.authors.html)
        *   [landlab](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.cmd.landlab.html)
    *   [components](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.html)[ ] 
        
        Toggle navigation of components
        
        *   [advection](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.advection.html)[ ] 
            
            Toggle navigation of advection
            
            *   [advection\_solver\_tvd](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.advection.advection_solver_tvd.html)
            *   [flux\_limiters](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.advection.flux_limiters.html)
        *   [area\_slope\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.area_slope_transporter.html)[ ] 
            
            Toggle navigation of area\_slope\_transporter
            
            *   [area\_slope\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.area_slope_transporter.area_slope_transporter.html)
        *   [bedrock\_landslider](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.bedrock_landslider.html)[ ] 
            
            Toggle navigation of bedrock\_landslider
            
            *   [bedrock\_landslider](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.bedrock_landslider.bedrock_landslider.html)
        *   [carbonate](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.carbonate.html)[ ] 
            
            Toggle navigation of carbonate
            
            *   [carbonate\_producer](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.carbonate.carbonate_producer.html)
        *   [chi\_index](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.chi_index.html)[ ] 
            
            Toggle navigation of chi\_index
            
            *   [channel\_chi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.chi_index.channel_chi.html)
        *   [concentration\_tracker](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.concentration_tracker.html)[ ] 
            
            Toggle navigation of concentration\_tracker
            
            *   [concentration\_tracker\_for\_diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.concentration_tracker.concentration_tracker_for_diffusion.html)
        *   [depression\_finder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depression_finder.html)[ ] 
            
            Toggle navigation of depression\_finder
            
            *   [floodstatus](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depression_finder.floodstatus.html)
            *   [lake\_mapper](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depression_finder.lake_mapper.html)
        *   [depth\_dependent\_diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depth_dependent_diffusion.html)[ ] 
            
            Toggle navigation of depth\_dependent\_diffusion
            
            *   [hillslope\_depth\_dependent\_linear\_flux](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depth_dependent_diffusion.hillslope_depth_dependent_linear_flux.html)
        *   [depth\_dependent\_taylor\_soil\_creep](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depth_dependent_taylor_soil_creep.html)[ ] 
            
            Toggle navigation of depth\_dependent\_taylor\_soil\_creep
            
            *   [hillslope\_depth\_dependent\_taylor\_flux](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.depth_dependent_taylor_soil_creep.hillslope_depth_dependent_taylor_flux.html)
        *   [detachment\_ltd\_erosion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.detachment_ltd_erosion.html)[ ] 
            
            Toggle navigation of detachment\_ltd\_erosion
            
            *   [generate\_detachment\_ltd\_erosion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.detachment_ltd_erosion.generate_detachment_ltd_erosion.html)
            *   [generate\_erosion\_by\_depth\_slope](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.detachment_ltd_erosion.generate_erosion_by_depth_slope.html)
        *   [diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.diffusion.html)[ ] 
            
            Toggle navigation of diffusion
            
            *   [diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.diffusion.diffusion.html)
        *   [dimensionless\_discharge](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.dimensionless_discharge.html)[ ] 
            
            Toggle navigation of dimensionless\_discharge
            
            *   [dimensionless\_discharge](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.dimensionless_discharge.dimensionless_discharge.html)
        *   [discharge\_diffuser](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.discharge_diffuser.html)[ ] 
            
            Toggle navigation of discharge\_diffuser
            
            *   [diffuse\_by\_discharge](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.discharge_diffuser.diffuse_by_discharge.html)
        *   [drainage\_density](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.drainage_density.html)[ ] 
            
            Toggle navigation of drainage\_density
            
            *   [drainage\_density](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.drainage_density.drainage_density.html)
        *   [erosion\_deposition](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.erosion_deposition.html)[ ] 
            
            Toggle navigation of erosion\_deposition
            
            *   [erosion\_deposition](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.erosion_deposition.erosion_deposition.html)
            *   [generalized\_erosion\_deposition](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.erosion_deposition.generalized_erosion_deposition.html)
            *   [shared\_stream\_power](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.erosion_deposition.shared_stream_power.html)
        *   [fire\_generator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.fire_generator.html)[ ] 
            
            Toggle navigation of fire\_generator
            
            *   [generate\_fire](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.fire_generator.generate_fire.html)
        *   [flexure](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flexure.html)[ ] 
            
            Toggle navigation of flexure
            
            *   [flexure](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flexure.flexure.html)
            *   [flexure\_1d](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flexure.flexure_1d.html)
            *   [funcs](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flexure.funcs.html)
        *   [flow\_accum](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_accum.html)[ ] 
            
            Toggle navigation of flow\_accum
            
            *   [flow\_accum\_bw](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_accum.flow_accum_bw.html)
            *   [flow\_accum\_to\_n](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_accum.flow_accum_to_n.html)
            *   [flow\_accumulator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_accum.flow_accumulator.html)
            *   [lossy\_flow\_accumulator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_accum.lossy_flow_accumulator.html)
        *   [flow\_director](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.html)[ ] 
            
            Toggle navigation of flow\_director
            
            *   [flow\_direction\_DN](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_direction_DN.html)
            *   [flow\_direction\_dinf](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_direction_dinf.html)
            *   [flow\_direction\_mfd](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_direction_mfd.html)
            *   [flow\_director](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director.html)
            *   [flow\_director\_d8](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director_d8.html)
            *   [flow\_director\_dinf](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director_dinf.html)
            *   [flow\_director\_mfd](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director_mfd.html)
            *   [flow\_director\_steepest](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director_steepest.html)
            *   [flow\_director\_to\_many](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director_to_many.html)
            *   [flow\_director\_to\_one](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_director.flow_director_to_one.html)
        *   [flow\_router](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_router.html)[ ] 
            
            Toggle navigation of flow\_router
            
            *   [ext](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_router.ext.html)[ ] 
                
                Toggle navigation of ext
                
                *   [single\_flow](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_router.ext.single_flow.html)[ ] 
                    
                    Toggle navigation of single\_flow
                    
                    *   [priority\_routing](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.flow_router.ext.single_flow.priority_routing.html)
        *   [fracture\_grid](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.fracture_grid.html)[ ] 
            
            Toggle navigation of fracture\_grid
            
            *   [fracture\_grid](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.fracture_grid.fracture_grid.html)
        *   [gflex](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.gflex.html)[ ] 
            
            Toggle navigation of gflex
            
            *   [flexure](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.gflex.flexure.html)
        *   [gravel\_bedrock\_eroder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.gravel_bedrock_eroder.html)[ ] 
            
            Toggle navigation of gravel\_bedrock\_eroder
            
            *   [gravel\_bedrock\_eroder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.gravel_bedrock_eroder.gravel_bedrock_eroder.html)
        *   [gravel\_river\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.gravel_river_transporter.html)[ ] 
            
            Toggle navigation of gravel\_river\_transporter
            
            *   [gravel\_river\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.gravel_river_transporter.gravel_river_transporter.html)
        *   [groundwater](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.groundwater.html)[ ] 
            
            Toggle navigation of groundwater
            
            *   [dupuit\_percolator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.groundwater.dupuit_percolator.html)
        *   [hack\_calculator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.hack_calculator.html)[ ] 
            
            Toggle navigation of hack\_calculator
            
            *   [hack\_calculator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.hack_calculator.hack_calculator.html)
        *   [hand\_calculator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.hand_calculator.html)[ ] 
            
            Toggle navigation of hand\_calculator
            
            *   [hand\_calculator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.hand_calculator.hand_calculator.html)
        *   [lake\_fill](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.lake_fill.html)[ ] 
            
            Toggle navigation of lake\_fill
            
            *   [lake\_fill\_barnes](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.lake_fill.lake_fill_barnes.html)
        *   [landslides](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.landslides.html)[ ] 
            
            Toggle navigation of landslides
            
            *   [landslide\_probability](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.landslides.landslide_probability.html)
        *   [lateral\_erosion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.lateral_erosion.html)[ ] 
            
            Toggle navigation of lateral\_erosion
            
            *   [lateral\_erosion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.lateral_erosion.lateral_erosion.html)
            *   [node\_finder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.lateral_erosion.node_finder.html)
        *   [lithology](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.lithology.html)[ ] 
            
            Toggle navigation of lithology
            
            *   [litholayers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.lithology.litholayers.html)
            *   [lithology](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.lithology.lithology.html)
        *   [marine\_sediment\_transport](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.marine_sediment_transport.html)[ ] 
            
            Toggle navigation of marine\_sediment\_transport
            
            *   [simple\_submarine\_diffuser](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.marine_sediment_transport.simple_submarine_diffuser.html)
        *   [mass\_wasting\_runout](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.mass_wasting_runout.html)[ ] 
            
            Toggle navigation of mass\_wasting\_runout
            
            *   [mass\_wasting\_runout](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.mass_wasting_runout.mass_wasting_runout.html)
            *   [mass\_wasting\_saver](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.mass_wasting_runout.mass_wasting_saver.html)
        *   [network\_sediment\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.network_sediment_transporter.html)[ ] 
            
            Toggle navigation of network\_sediment\_transporter
            
            *   [bed\_parcel\_initializers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.network_sediment_transporter.bed_parcel_initializers.html)
            *   [network\_sediment\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.network_sediment_transporter.network_sediment_transporter.html)
            *   [sediment\_pulser\_at\_links](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.network_sediment_transporter.sediment_pulser_at_links.html)
            *   [sediment\_pulser\_base](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.network_sediment_transporter.sediment_pulser_base.html)
            *   [sediment\_pulser\_each\_parcel](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.network_sediment_transporter.sediment_pulser_each_parcel.html)
        *   [nonlinear\_diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.nonlinear_diffusion.html)[ ] 
            
            Toggle navigation of nonlinear\_diffusion
            
            *   [Perron\_nl\_diffuse](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.nonlinear_diffusion.Perron_nl_diffuse.html)
        *   [normal\_fault](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.normal_fault.html)[ ] 
            
            Toggle navigation of normal\_fault
            
            *   [normal\_fault](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.normal_fault.normal_fault.html)
        *   [overland\_flow](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.html)[ ] 
            
            Toggle navigation of overland\_flow
            
            *   [generate\_overland\_flow\_Bates](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.generate_overland_flow_Bates.html)
            *   [generate\_overland\_flow\_deAlmeida](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.generate_overland_flow_deAlmeida.html)
            *   [generate\_overland\_flow\_implicit\_kinwave](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.generate_overland_flow_implicit_kinwave.html)
            *   [generate\_overland\_flow\_kinwave](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.generate_overland_flow_kinwave.html)
            *   [kinematic\_wave\_rengers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.kinematic_wave_rengers.html)
            *   [linear\_diffusion\_overland\_flow\_router](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.linear_diffusion_overland_flow_router.html)
        *   [pet](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.pet.html)[ ] 
            
            Toggle navigation of pet
            
            *   [potential\_evapotranspiration\_field](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.pet.potential_evapotranspiration_field.html)
        *   [plant\_competition\_ca](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.plant_competition_ca.html)[ ] 
            
            Toggle navigation of plant\_competition\_ca
            
            *   [plant\_competition\_ca](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.plant_competition_ca.plant_competition_ca.html)
        *   [potentiality\_flowrouting](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.potentiality_flowrouting.html)[ ] 
            
            Toggle navigation of potentiality\_flowrouting
            
            *   [route\_flow\_by\_boundary](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.potentiality_flowrouting.route_flow_by_boundary.html)
        *   [priority\_flood\_flow\_router](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.priority_flood_flow_router.html)[ ] 
            
            Toggle navigation of priority\_flood\_flow\_router
            
            *   [priority\_flood\_flow\_router](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.priority_flood_flow_router.priority_flood_flow_router.html)
        *   [profiler](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.profiler.html)[ ] 
            
            Toggle navigation of profiler
            
            *   [base\_profiler](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.profiler.base_profiler.html)
            *   [channel\_profiler](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.profiler.channel_profiler.html)
            *   [profiler](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.profiler.profiler.html)
            *   [trickle\_down\_profiler](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.profiler.trickle_down_profiler.html)
        *   [radiation](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.radiation.html)[ ] 
            
            Toggle navigation of radiation
            
            *   [radiation](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.radiation.radiation.html)
        *   [sink\_fill](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.sink_fill.html)[ ] 
            
            Toggle navigation of sink\_fill
            
            *   [fill\_sinks](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.sink_fill.fill_sinks.html)
            *   [sink\_fill\_barnes](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.sink_fill.sink_fill_barnes.html)
        *   [soil\_moisture](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.soil_moisture.html)[ ] 
            
            Toggle navigation of soil\_moisture
            
            *   [infiltrate\_soil\_green\_ampt](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.soil_moisture.infiltrate_soil_green_ampt.html)
            *   [soil\_moisture\_dynamics](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.soil_moisture.soil_moisture_dynamics.html)
        *   [space](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.space.html)[ ] 
            
            Toggle navigation of space
            
            *   [space](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.space.space.html)
            *   [space\_large\_scale\_eroder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.space.space_large_scale_eroder.html)
        *   [spatial\_precip](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.spatial_precip.html)[ ] 
            
            Toggle navigation of spatial\_precip
            
            *   [generate\_spatial\_precip](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.spatial_precip.generate_spatial_precip.html)
        *   [species\_evolution](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.html)[ ] 
            
            Toggle navigation of species\_evolution
            
            *   [base\_taxon](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.base_taxon.html)
            *   [record](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.record.html)
            *   [species\_evolver](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.species_evolver.html)
            *   [zone](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.zone.html)
            *   [zone\_controller](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.zone_controller.html)
            *   [zone\_taxon](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.species_evolution.zone_taxon.html)
        *   [steepness\_index](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.steepness_index.html)[ ] 
            
            Toggle navigation of steepness\_index
            
            *   [channel\_steepness](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.steepness_index.channel_steepness.html)
        *   [stream\_power](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.stream_power.html)[ ] 
            
            Toggle navigation of stream\_power
            
            *   [fastscape\_stream\_power](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.stream_power.fastscape_stream_power.html)
            *   [sed\_flux\_dep\_incision](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.stream_power.sed_flux_dep_incision.html)
            *   [stream\_power](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.stream_power.stream_power.html)
            *   [stream\_power\_smooth\_threshold](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.stream_power.stream_power_smooth_threshold.html)
        *   [taylor\_nonlinear\_hillslope\_flux](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.taylor_nonlinear_hillslope_flux.html)[ ] 
            
            Toggle navigation of taylor\_nonlinear\_hillslope\_flux
            
            *   [taylor\_nonlinear\_hillslope\_flux](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.taylor_nonlinear_hillslope_flux.taylor_nonlinear_hillslope_flux.html)
        *   [tectonics](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.tectonics.html)[ ] 
            
            Toggle navigation of tectonics
            
            *   [listric\_kinematic\_extender](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.tectonics.listric_kinematic_extender.html)
        *   [threshold\_eroder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.threshold_eroder.html)[ ] 
            
            Toggle navigation of threshold\_eroder
            
            *   [threshold\_eroder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.threshold_eroder.threshold_eroder.html)
        *   [tidal\_flow](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.tidal_flow.html)[ ] 
            
            Toggle navigation of tidal\_flow
            
            *   [tidal\_flow\_calculator](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.tidal_flow.tidal_flow_calculator.html)
        *   [transport\_length\_diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.transport_length_diffusion.html)[ ] 
            
            Toggle navigation of transport\_length\_diffusion
            
            *   [transport\_length\_hillslope\_diffusion](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.transport_length_diffusion.transport_length_hillslope_diffusion.html)
        *   [uniform\_precip](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.uniform_precip.html)[ ] 
            
            Toggle navigation of uniform\_precip
            
            *   [generate\_uniform\_precip](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.uniform_precip.generate_uniform_precip.html)
        *   [vegetation\_dynamics](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.vegetation_dynamics.html)[ ] 
            
            Toggle navigation of vegetation\_dynamics
            
            *   [vegetation\_dynamics](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.vegetation_dynamics.vegetation_dynamics.html)
        *   [weathering](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.weathering.html)[ ] 
            
            Toggle navigation of weathering
            
            *   [exponential\_weathering](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.weathering.exponential_weathering.html)
            *   [exponential\_weathering\_integrated](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.weathering.exponential_weathering_integrated.html)
    *   [core](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.core.html)[ ] 
        
        Toggle navigation of core
        
        *   [errors](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.core.errors.html)
        *   [messages](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.core.messages.html)
        *   [model\_component](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.core.model_component.html)
        *   [model\_parameter\_loader](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.core.model_parameter_loader.html)
        *   [utils](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.core.utils.html)
    *   [data\_record](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.data_record.html)[ ] 
        
        Toggle navigation of data\_record
        
        *   [aggregators](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.data_record.aggregators.html)
        *   [data\_record](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.data_record.data_record.html)
    *   [field](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.field.html)[ ] 
        
        Toggle navigation of field
        
        *   [errors](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.field.errors.html)
        *   [graph\_field](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.field.graph_field.html)
    *   [framework](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.framework.html)[ ] 
        
        Toggle navigation of framework
        
        *   [component](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.framework.component.html)
        *   [decorators](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.framework.decorators.html)
        *   [interfaces](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.framework.interfaces.html)
    *   [graph](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.html)[ ] 
        
        Toggle navigation of graph
        
        *   [ext](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.ext.html)
        *   [framed\_voronoi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.framed_voronoi.html)[ ] 
            
            Toggle navigation of framed\_voronoi
            
            *   [dual\_framed\_voronoi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.framed_voronoi.dual_framed_voronoi.html)
            *   [framed\_voronoi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.framed_voronoi.framed_voronoi.html)
        *   [hex](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.hex.html)[ ] 
            
            Toggle navigation of hex
            
            *   [ext](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.hex.ext.html)
            *   [dual\_hex](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.hex.dual_hex.html)
            *   [hex](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.hex.hex.html)
        *   [matrix](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.matrix.html)[ ] 
            
            Toggle navigation of matrix
            
            *   [ext](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.matrix.ext.html)
            *   [at\_node](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.matrix.at_node.html)
            *   [at\_patch](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.matrix.at_patch.html)
        *   [object](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.object.html)[ ] 
            
            Toggle navigation of object
            
            *   [ext](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.object.ext.html)
            *   [at\_node](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.object.at_node.html)
            *   [at\_patch](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.object.at_patch.html)
        *   [quantity](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.quantity.html)[ ] 
            
            Toggle navigation of quantity
            
            *   [ext](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.quantity.ext.html)
            *   [of\_link](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.quantity.of_link.html)
            *   [of\_patch](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.quantity.of_patch.html)
        *   [quasi\_spherical](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.quasi_spherical.html)[ ] 
            
            Toggle navigation of quasi\_spherical
            
            *   [dual\_icosphere](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.quasi_spherical.dual_icosphere.html)
            *   [refinable\_icosahedron](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.quasi_spherical.refinable_icosahedron.html)
        *   [radial](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.radial.html)[ ] 
            
            Toggle navigation of radial
            
            *   [dual\_radial](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.radial.dual_radial.html)
            *   [radial](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.radial.radial.html)
        *   [sort](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.sort.html)[ ] 
            
            Toggle navigation of sort
            
            *   [ext](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.sort.ext.html)
            *   [intpair](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.sort.intpair.html)
            *   [sort](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.sort.sort.html)
        *   [structured\_quad](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.structured_quad.html)[ ] 
            
            Toggle navigation of structured\_quad
            
            *   [ext](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.structured_quad.ext.html)
            *   [dual\_structured\_quad](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.structured_quad.dual_structured_quad.html)
            *   [structured\_quad](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.structured_quad.structured_quad.html)
        *   [voronoi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.voronoi.html)[ ] 
            
            Toggle navigation of voronoi
            
            *   [ext](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.voronoi.ext.html)
            *   [dual\_voronoi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.voronoi.dual_voronoi.html)
            *   [voronoi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.voronoi.voronoi.html)
            *   [voronoi\_to\_graph](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.voronoi.voronoi_to_graph.html)
        *   [dual](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.dual.html)
        *   [graph](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.graph.html)
        *   [graph\_convention](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.graph_convention.html)
        *   [ugrid](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.graph.ugrid.html)
    *   [grid](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.html)[ ] 
        
        Toggle navigation of grid
        
        *   [unstructured](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.unstructured.html)[ ] 
            
            Toggle navigation of unstructured
            
            *   [base](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.unstructured.base.html)
            *   [cells](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.unstructured.cells.html)
            *   [links](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.unstructured.links.html)
            *   [nodes](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.unstructured.nodes.html)
            *   [status](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.unstructured.status.html)
        *   [base](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.base.html)
        *   [create](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.create.html)
        *   [create\_network](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.create_network.html)
        *   [decorators](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.decorators.html)
        *   [diagonals](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.diagonals.html)
        *   [divergence](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.divergence.html)
        *   [framed\_voronoi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.framed_voronoi.html)
        *   [gradients](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.gradients.html)
        *   [grid\_funcs](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.grid_funcs.html)
        *   [hex](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.hex.html)
        *   [hex\_mappers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.hex_mappers.html)
        *   [icosphere](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.icosphere.html)
        *   [linkorientation](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.linkorientation.html)
        *   [linkstatus](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.linkstatus.html)
        *   [mappers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.mappers.html)
        *   [network](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.network.html)
        *   [nodestatus](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.nodestatus.html)
        *   [radial](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.radial.html)
        *   [raster](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster.html)
        *   [raster\_aspect](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster_aspect.html)
        *   [raster\_divergence](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster_divergence.html)
        *   [raster\_funcs](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster_funcs.html)
        *   [raster\_gradients](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster_gradients.html)
        *   [raster\_mappers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster_mappers.html)
        *   [raster\_set\_status](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.raster_set_status.html)
        *   [voronoi](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.voronoi.html)
        *   [warnings](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.grid.warnings.html)
    *   [io](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.io.html)[ ] 
        
        Toggle navigation of io
        
        *   [netcdf](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.io.netcdf.html)[ ] 
            
            Toggle navigation of netcdf
            
            *   [dump](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.io.netcdf.dump.html)
            *   [errors](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.io.netcdf.errors.html)
            *   [load](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.io.netcdf.load.html)
            *   [read](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.io.netcdf.read.html)
            *   [write](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.io.netcdf.write.html)
        *   [esri\_ascii](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.io.esri_ascii.html)
        *   [legacy\_vtk](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.io.legacy_vtk.html)
        *   [native\_landlab](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.io.native_landlab.html)
        *   [obj](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.io.obj.html)
        *   [shapefile](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.io.shapefile.html)
    *   [layers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.layers.html)[ ] 
        
        Toggle navigation of layers
        
        *   [ext](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.layers.ext.html)
        *   [eventlayers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.layers.eventlayers.html)
        *   [materiallayers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.layers.materiallayers.html)
    *   [plot](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.plot.html)[ ] 
        
        Toggle navigation of plot
        
        *   [network\_sediment\_transporter](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.plot.network_sediment_transporter.html)[ ] 
            
            Toggle navigation of network\_sediment\_transporter
            
            *   [locate\_parcel\_xy](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.plot.network_sediment_transporter.locate_parcel_xy.html)
            *   [plot\_network\_and\_parcels](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.plot.network_sediment_transporter.plot_network_and_parcels.html)
        *   [colors](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.plot.colors.html)
        *   [drainage\_plot](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.plot.drainage_plot.html)
        *   [event\_handler](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.plot.event_handler.html)
        *   [graph](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.plot.graph.html)
        *   [imshow](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.plot.imshow.html)
        *   [imshowhs](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.plot.imshowhs.html)
        *   [layers](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.plot.layers.html)
        *   [video\_out](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.plot.video_out.html)
    *   [utils](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.html)[ ] 
        
        Toggle navigation of utils
        
        *   [ext](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.ext.html)
        *   [add\_halo](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.add_halo.html)
        *   [count\_repeats](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.count_repeats.html)
        *   [decorators](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.decorators.html)
        *   [depth\_dependent\_roughness](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.depth_dependent_roughness.html)
        *   [distance\_to\_divide](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.distance_to_divide.html)
        *   [fault\_facet\_finder](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.fault_facet_finder.html)
        *   [flow\_\_distance](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.flow__distance.html)
        *   [jaggedarray](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.jaggedarray.html)
        *   [jaggedarray\_ma](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.jaggedarray_ma.html)
        *   [matrix](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.matrix.html)
        *   [return\_array](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.return_array.html)
        *   [source\_tracking\_algorithm](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.source_tracking_algorithm.html)
        *   [stable\_priority\_queue](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.stable_priority_queue.html)
        *   [structured\_grid](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.structured_grid.html)
        *   [suppress\_output](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.suppress_output.html)
        *   [watershed](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.watershed.html)
        *   [window\_statistic](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.utils.window_statistic.html)
    *   [values](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.values.html)[ ] 
        
        Toggle navigation of values
        
        *   [synthetic](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.values.synthetic.html)

About

*   [Release Notes](https://landlab.readthedocs.io/en/v2.9.2/about/changes.html)
*   [Contact](https://landlab.readthedocs.io/en/v2.9.2/about/contact_us.html)
*   [Citing Landlab](https://landlab.readthedocs.io/en/v2.9.2/about/citing.html)
*   [Funding](https://landlab.readthedocs.io/en/v2.9.2/about/funding.html)
*   [Contributors](https://landlab.readthedocs.io/en/v2.9.2/about/authors.html)
*   [License](https://landlab.readthedocs.io/en/v2.9.2/about/license.html)
*   [Used by](https://landlab.readthedocs.io/en/v2.9.2/about/usedby.html)

Project Links

*   [GitHub](https://github.com/landlab/landlab)
*   [PyPI](https://pypi.org/project/landlab)
*   [Conda-Forge](https://github.com/conda-forge/landlab-feedstock)

[Back to top](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#)

[Edit this page](https://github.com/landlab/landlab/edit/master/docs/source/user_guide/overland_flow_user_guide.md "Edit this page")

Toggle Light / Dark / Auto color theme

Toggle table of contents sidebar

Overland Flow Component User Manual[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#overland-flow-component-user-manual "Link to this heading")
================================================================================================================================

Background on OverlandFlow component[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#background-on-overlandflow-component "Link to this heading")
--------------------------------------------------------------------------------------------------------------------------------

The Landlab OverlandFlow component implements a 2-D solution of the shallow water equations, following the algorithm of de Almeida et al., (2012). In this component, an explicit solution simulates a flood wave moving across a gridded terrain, capturing hydrodynamics throughout the system. At each point within the grid, surface water discharge is calculated based on physical properties. This component expands the hydrologic capabilities of Landlab by offering a nonsteady flow routing method as an alternative to the steady-state flow routing regimes found in many geomorphic or landscape evolution models (such as the Landlab `FlowAccumulator` component).

This User Manual describes how to instantiate, parameterize and plot data using the OverlandFlow component, using an example described in Adams et al., (in press, _Geoscientific Model Development_). For further information about the derivation of the algorithm used in this component, see: Bates et al., (2010) and de Almeida et al., (2012).

**Note**: Currently, the OverlandFlow component can only operate on a structured grid, and so all references to the grid below are specifically referring to the Landlab RasterModelGrid module.

_Prerequisites_: A working knowledge of the Python programming language (any version) and familiarity with the Python libraries NumPy and Matplotlib. A basic understanding of the Landlab modeling framework (Hobley et al., 2017) is also recommended.

Model parameters and variables[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#model-parameters-and-variables "Link to this heading")
--------------------------------------------------------------------------------------------------------------------------------

**Input parameters**

Parameters listed here are easily tuned by the model user. For a complete list, see [`here`](https://landlab.readthedocs.io/en/v2.9.2/generated/api/landlab.components.overland_flow.html#module-landlab.components.overland_flow "landlab.components.overland_flow").

*   **Alpha** : Weight on the adaptive time step, ranging between 0.2 - 0.7. For more information, see Hunter et al., (2005).
    
*   **Manning’s n** : An empirical value describing surface roughness. See Chow (1959).
    
*   **Theta** : A weighting factor in the de Almeida et al., (2012) equation, suggested value between 0.8 and 0.9
    

**Model variables**

Variables listed here are updated by the component at the grid locations listed.

*   **surface\_water\_\_discharge**, _link_, \[m^2 s^-1\] : At each link in grid, _surface\_water\_\_discharge_ is calculated using the de Almeida et al., (2012) equation. Discharge is a function of the water depth, adaptive time step, surface water slope and Manning’s roughness coefficient.
    
*   **surface\_water\_\_depth**, _node_, \[m\] : At each node in the grid, _surface\_water\_\_depth_ is updated using the _surface\_water\_\_discharge_ on links connected to a given node.
    

Basic steps of an OverlandFlow model[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#basic-steps-of-an-overlandflow-model "Link to this heading")
--------------------------------------------------------------------------------------------------------------------------------

1.  **Import the necessary libraries**: `OverlandFlow` is required. Optional libraries include the `SinkFiller` component, the Landlab plotting method `imshow__grid`. Additional packages mentioned here include `matplotlib.pyplot` and `numpy`.
    
2.  **Defining the model domain**: The computational domain of an OverlandFlow model can only work on RasterModelGrid instances as of Landlab version 1.0.0.
    
3.  **Setting the boundary conditions**: If a clipped watershed digital elevation model (DEM) from ArcGIS is imported in ASCII format, the method `set_watershed_boundary_condition()` can be used. Alternatively, `fixed_link` boundary conditions can be used for discharge inputs on links. Other boundary condition scenarios can be accommodated by setting individual nodes or edges of the grid using Landlab boundary condition handling.
    
4.  **Pre-processing the DEM**: This step is _optional_. If a watershed DEM is used, ArcGIS “D8” pit-filling will not create a continuous network for the “D4” `OverlandFlow` algorithm. The `SinkFiller` component can pit fill for a “D4” network.
    
5.  **Initializing the OverlandFlow component**: The instance of the `OverlandFlow` class is declared, and parameters are set by the user.
    
6.  **Determining precipitation inputs**: A constant precipitation rate can be passed to the `OverlandFlow` class, where precipitation persists for the entire model run. Alternatively, a single event can be set within the time loop, and then water can drain from the system when the precipitation event is over.
    
7.  **Time loop**: The main `OverlandFlow` methods are called, and grid variables are updated through time. Data can be saved for plotting or later analysis.
    

### Step 1. Import the necessary libraries[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-1-import-the-necessary-libraries "Link to this heading")

To build an OverlandFlow model, first the necessary Landlab components and utilities, as well as any necessary Python packages must be imported. Standard Python style dictates all import statements belong in the top of the driver file, after the module docstrings. In this simple example, the OverlandFlow model driver begins as follows:

"""overland\_flow\_driver.py

OverlandFlow component example, initializing a 36 km^2 square watershed with a
grid resolution of 30 m, from an ESRI ASCII file, simulating a 5 mm/hr rainfall
intensity over 2 hours, the standard storm example from Adams et al.,
in prep for Geoscientific Model Development

Written by Jordan Adams, August 2016
"""

\## Landlab components
from landlab.components import OverlandFlow, SinkFiller  \# SinkFiller is optional

\## Landlab utilities
from landlab.io import read\_esri\_ascii  \# OR from landlab import RasterModelGrid
from landlab.plot import imshow\_grid  \# plotter functions are optional

\## Additional Python packages
import numpy as np
from matplotlib import pyplot as plt  \# plotter functions are optional

To run the test case presented here, two components are needed. First is the required `OverlandFlow` component, which will be used to calculate surface water discharge and surface water depth across the model grid. Also presented here is the `SinkFiller` component, which can be used optionally to pre-process the DEM. The `SinkFiller` component is described in more detail in **Step 4** of this Users Manual.

To create a model domain, a Landlab RasterModelGrid instance must be initialized. In this example, the Landlab input/output suite of tools is used to read in a DEM that is formatted as an ESRI ASCII file `read_esri_ascii`). Alternatively, a model domain can be manually created by the user. Both of these methods are described in detail in **Step 2** of this Users Manual.

Other Landlab utilities used in this example are the plotting library `imshow_grid`, which is a utility that can plot a Landlab grid instance and data field in map view, as described in the **Plotting and visualization** section in this Users Manual.

Finally, additional Python packages are imported. In this example, both packages are dependencies of Landlab, which means they are required for Landlab installation and as such, should already be present on the user’s machine. The scientific computing library NumPy is used for mathematical operations, and the matplotlib library is used for plotting model output.

### Step 2. Defining the model domain[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-2-defining-the-model-domain "Link to this heading")

As previously stated, the algorithm used in the OverlandFlow component was derived to work on remotely-sensed data and, as such, only works on the RasterModelGrid instance in Landlab (e.g. Bates et al., 2010, de Almeida et al., 2012). Shown here is an example of a Landlab raster grid:

[![Image 7: ../_images/RasterGrid_Directions.png](https://landlab.readthedocs.io/en/v2.9.2/_images/RasterGrid_Directions.png)](https://landlab.readthedocs.io/en/v2.9.2/_images/RasterGrid_Directions.png)**Figure** 1: Example of a Landlab RasterModelGrid instance. Each RasterModelGrid is composed of 3 core elements: nodes, which are points in (x, y) space; cells, a polygon with an area around a node; and links, ordered lines which connect neighboring pairs of node that store directionality.

There are two ways to implement a RasterModelGrid that work with Landlab: reading in remotely-sensed data from a DEM with `read_esri_ascii()`, or manually setting a generic structured grid using the RasterModelGrid library. Both of these methods are described in detail below.

#### Reading in a watershed DEM[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#reading-in-a-watershed-dem "Link to this heading")

Landlab can easily interact with DEM data output by ESRI’s ArcGIS software. In this example, the DEM ‘Square\_TestBasin.asc’ represents a single watershed. Reading in the data takes two lines of code, outlined here:

watershed\_dem \= "Square\_TestBasin.asc"
(rmg, z) \= read\_esri\_ascii(watershed\_dem, name\="topographic\_\_elevation")

In this example, the watershed DEM is read in by the `read_esri_ascii()` method, and the elevation data from the DEM is automatically assigned to the Landlab data field `topographic__elevation`, for use by the components.

#### Setting up a generic RasterModelGrid[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#setting-up-a-generic-rastermodelgrid "Link to this heading")

The alternative to reading in a watershed DEM is to set the RasterModelGrid instance manually:

rmg \= RasterModelGrid((number\_of\_node\_rows, number\_of\_node\_columns), dx)
z \= user\_defined\_elevation\_data  \# length of number\_of\_nodes
rmg\["node"\]\["topographic\_\_elevation"\] \= z

This example assumes that the model users knows the following information: the number of grid rows (`number_of_grid_rows`), the number of grid columns (`number_of_grid_columns`), the grid resolution (`dx`) and some elevation data for each node. Here, the user must manually set the elevation data. When passing elevation data to the `topographic__elevation` field, the length of `user_defined_elevation_data` **must** be equal to the number of nodes in the grid (which can be found using a command such as: `rmg.number_of_nodes`.

### Step 3. Setting the boundary conditions[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-3-setting-the-boundary-conditions "Link to this heading")

Landlab contains several methods which can set and update boundary conditions at _node_ and _link_ grid elements. When modeling water flow across a grid, a user needs to predetermine locations where water can and cannot flow. If a user reads in a single watershed DEM, (as described in **Step 2**), there is a utility within Landlab that can handle the specific boundary conditions needed to control flow:

rmg.set\_watershed\_boundary\_condition(z, nodata\_values\=-9999.0)

By definition, a watershed has only one outlet, or open boundary location, and therefore all other nodes surrounding the watershed will be closed, or no flux, boundaries. The `set_watershed_boundary_condition()` method reads the gridded elevation data, (`z`), identifies the watershed outlet and sets it to an open boundary (identified by the grid attribute `grid.BC_NODE_IS_FIXED_VALUE` in Landlab). An open boundary allows flux to leave the modeling domain. Additionally, this methods also identifies all NODATA nodes (given a default value of -9999) and sets them to closed, or no flux, boundaries.

**Note**: As of Landlab version 1.0.0., this method only works on single watersheds, and so assumes that the watershed has been clipped in ArcGIS and has only one outlet point.

#### Other boundary condition options[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#other-boundary-condition-options "Link to this heading")

There are other options for boundary condition handling that are more appropriate for non-DEM modeling domains. (For a complete review of boundary condition handling in Landlab, review Hobley et al., in submission for _Earth Surface Dynamics_ or Landlab [boundary](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid_methods/03_boundary_conditions.html#api-grid-grid-summary-bc) condition documentation

Here, the `FIXED_GRADIENT` boundary condition is described. The `set_nodata_nodes_to_fixed_gradient()` method sets all NODATA nodes to `FIXED_GRADIENT`, and all boundary links (links that connect core nodes within the model domain to a fixed gradient nodes) are set to `FIXED_LINK` status. Then, boundary links can be updated with some input discharge value:

rmg.set\_nodata\_nodes\_to\_fixed\_gradient(z)
rmg.fixed\_links \= input\_discharge\_value

This boundary condition can be useful because of how the underlying algorithm in OverlandFlow (de Almeida et al., 2012) updates discharge at each time step. In this model, discharge is calculated as a function of the neighboring discharge values:

[![Image 8: ../_images/deAlmeidaGridExample.png](https://landlab.readthedocs.io/en/v2.9.2/_images/deAlmeidaGridExample.png)](https://landlab.readthedocs.io/en/v2.9.2/_images/deAlmeidaGridExample.png)**Figure 2**: The algorithm from de Almeida et al., (2012) uses discharge information on neighboring links to calculate discharge. Fixed link boundary conditions allow the user to set discharge on links along the boundary, so that the interior discharges can be updated using those manually-set fluxes.

In this example, calculating discharge on qx requires discharge values qx-1 and qx+1. If a link is along the boundary of the domain, the default value is 0. Fixed link boundary statuses allow the user to manually update the discharge value at a boundary link, to simulate some influx of water discharge into the model domain.

If the user desires, these fixed links can also be updated to contain flux value of their nearest interior neighbor. Following the earlier example, if discharge qx-1 is at on a fixed boundary link, it can be updated to contain the value of its neighboring discharge qx. This is done exclusively in the OverlandFlow component. The user simply needs to call `default_fixed_links = True` when initializing the `OverlandFlow` component, as described in **Step 5**. This method prevents flow from exiting the edge of the watershed onto NODATA nodes, and does not set an outlet node by default. If the user wants to set an outlet node to an open boundary, that must be done manually, not described here.

### Step 4. Pre-processing the DEM (_Optional_)[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-4-pre-processing-the-dem-optional "Link to this heading")

When modeling surface flow across a DEM and the user wants to ensure all water drains out of the system (that is, water is not trapped in pits or holes on the DEM surface), there must be a continuous flow path. In many applications, flow is allowed to exit a node in 8 directions (‘D8’): the cardinal directions (East, North, West, South) and the diagonal directions (Northeast, Northwest, Southwest, Southeast). However, this model restricts flow to only the cardinal directions (‘D4’). To create a continuous flow network, GIS applications often include a pit-filling regime to remove divots in the DEM surface so water can exit the pit and travel to the outlet. In ArcGIS, this pit-filling regime operates in ‘D8’:

[![Image 9: ../_images/D8_vs_D4.png](https://landlab.readthedocs.io/en/v2.9.2/_images/D8_vs_D4.png)](https://landlab.readthedocs.io/en/v2.9.2/_images/D8_vs_D4.png)**Figure 3**: Comparison of ‘D8’ and ‘D4’ flow routing methods. The key difference: in ‘D8’ methods, flow can move diagonally out of a given node.

However, in Landlab version 1.0.0., the OverlandFlow component is limited to the ‘D4’ regime. If a watershed DEM has been processed in ArcGIS, the flow network most likely follows a ‘D8’ path. When using the OverlandFlow component on a ‘D8’ network, the flow path may not be continuous.

To address this discrepancy, the SinkFiller component in Landlab has been developed to accommodate both ‘D8’ or ‘D4’ pit-filling on a DEM. Running this component can take some time, particularly on large grids, so it is _optional_ to run the OverlandFlow component. This component can be applied to our DEM in two lines of code, initializing the SinkFiller component and running the `fill_pits()` method:

sf \= SinkFiller(rmg, routing\="D4", apply\_slope\=True, fill\_slope\=1.0e-5)
sf.fill\_pits()

**Note**: For more information about the SinkFiller `component`.

### Step 5. Initializing the OverlandFlow component[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-5-initializing-the-overlandflow-component "Link to this heading")

Most Landlab components are structured as a Python class. These classes are imported (as seen in **Step 1**) and then the user must create an instance of the class:

of \= OverlandFlow(rmg, mannings\_n\=0.03, steep\_slopes\=True)

When the instance of the class is created, parameters are passed as keywords to the class. All Landlab components take a grid as their first argument. All subsequent keywords are parameters used to control model behavior. Each Landlab component has documentation which lists the parameters. The OverlandFlow documentation is linked in the **Model description** section above. The example script shown here includes parameters _Manning’s n_, which takes a numerical value, and the stability criterion `steep_slopes` flag, which is passed a Boolean (`True` or `False`) value. Details about the stability criterion are provided in the next subsection.

#### Stability criteria[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#stability-criteria "Link to this heading")

The OverlandFlow component is built off the de Almeida et al., (2012) algorithm for urban flood inundation, and is most stable in flat environments. Because of this, instabilities can arise when trying to apply the algorithm to steep landscapes. To adapt this model for use across a variety of terrains, stability criteria (following Coulthard et al., 2013) is implemented to using the `steep_slopes` flag. This method reduces flow discharge to keep flow subcritical according to the Froude number less than or equal to 1.0. For more information, see Adams et al., (in prep for _Geoscientific Model Development_).

### Step 6. Precipitation inputs[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-6-precipitation-inputs "Link to this heading")

Often, the user will want to route a precipitation event or a series of precipitation events across a watershed.There are two methods for setting precipitation parameters in the OverlandFlow component.

**Note**: At the moment, only uniform precipitation events have been tested using this component.

#### Constant precipitation input[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#constant-precipitation-input "Link to this heading")

This is the simplest method, and is used when a constant precipitation intensity is routed for the entirety of a model run (model\_run\_time). In this example, rainfall\_\_intensity (units \[m s\-1\]) is passed when the OverlandFlow component is initialized (**Step 5**):

elapsed\_time \= 0.0
model\_run\_time \= 86400.0
of \= OverlandFlow(
    rmg, steep\_slopes\=True, rainfall\_intensity\=1.38889 \* (10\*\*-6)
)  \# m/s

#### Single storm event[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#single-storm-event "Link to this heading")

Alternatively, a user may decide to route an event where rainfall stops, and water drains from the system. The simplest case is a single storm event, presented here:

elapsed\_time \= 0.0
model\_run\_time \= 86400.0

storm\_duration \= 7200.0
rainfall\_mmhr \= 5.0

In this example, storm characteristics (duration and intensity) are set separately from the OverlandFlow component initialization. These characteristics are used in a time loop within the model driver (seen in **Step 7**). While elapsed\_time in a model is less than storm duration, the precipitation intensity is input across all nodes in the model domain. When the storm event ends, the precipitation intensity is reset to 0 \[m s\-1\], allowing the water remaining in the system to drain out.

### Step 7. Iterate through time[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-7-iterate-through-time "Link to this heading")

The key part of any Landlab model driver is the time loop, where components recalculate the processes, and update their necessary data values. In the OverlandFlow component, during a time loop, at each time step, surface water discharge and surface water depth are recalculated. A simple example of an OverlandFlow time loop is presented here:

while elapsed\_time < model\_run\_time:
    of.dt \= of.calc\_time\_step()  \# Adaptive time step

    if elapsed\_time < (storm\_duration):
        of.rainfall\_intensity \= rainfall\_mmhr \* (2.777778 \* 10\*\*-7)
    else:
        of.rainfall\_intensity \= 0.0

    of.overland\_flow()

    rmg.at\_node\["surface\_water\_\_discharge"\] \= of.discharge\_mapper(
        of.q, convert\_to\_volume\=True
    )

    elapsed\_time += of.dt

This code snippet is described here:

*   This OverlandFlow example loops through time as a `while` loop. After each time loop, `elapsed_time` is increased until it exceeds `model_run_time`.
    
*   An adaptive time step is recommended, and is calculated here at the start of each time loop. (See the next subsection for more information about the adaptive time step).
    
*   Inside the time loop, there is a test to see if the `elapsed_time` is less than the `storm_duration`. If so, the rainfall intensity property of OverlandFlow is updated to the rainfall intensity (here converted from \[mm hr\-1 to \[m s\-1).
    
*   If the `elapsed_time` is greater than the `storm_duration`, the rainfall intensity parameter of the OverlandFlow component is reset to 0 \[m s\-1\].
    
*   After the rainfall intensity is set, the actual process method `overland_flow()` is called. This method calculate discharge as a function of the de Almeida et al., (2012) algorithm and updates the Landlab data fields for `surface_water__discharge` and `surface_water__depth` on links and nodes respectively.
    
*   To translate the discharge values calculated on Landlab links to nodes, values on links (`of.q`) are summed and mapped to their node neighbors using the method `of.discharge_mapper`. Using the `convert_to_volume` flag, these discharge values are converted from units of \[m2 s\-1\] to \[m3 s\-1\].
    
*   At the end of each loop, `elapsed_time` is updated with the adaptive time step.
    

**Note**: If using the adaptive time step, it may be possible that both the storm duration and model run time may be exceeded if the calculated time step is too large. It is recommended the use add additional logic tests to ensure both the storm\_duration and model\_run\_time are not exceeded. during the time loop.

#### Adaptive time step[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#adaptive-time-step "Link to this heading")

de Almeida et al., (2012) implement an adaptive time step to maintain model stability and computational efficiency. This adaptive time step follows Hunter et al., (2005). By default, the OverlandFlow component calculates this adaptive time step. It is listed explicitly the **Step 7** code for clarity. If that lines was removed from that code, the component would still call `calc_time_step()` every time the `overland_flow()` method is called.

Alternatively, an explicit time step can be passed to the `overland_flow()` method. However, this method cannot guarantee model stability. Numerical instability in the model can drive surface water depth ‘checkerboarding’ patterns. Additionally, water mass imbalances can be linked to model instability. If an explicit time step must be used, a small time step is recommended to maintain model stability.

**Note**: Model behavior can vary across different parameter space and grid resolution. Stability testing is always recommended.

Plotting and visualization[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#plotting-and-visualization "Link to this heading")
--------------------------------------------------------------------------------------------------------------------------------

### Hydrographs[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#hydrographs "Link to this heading")

#### Before time loop:[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#before-time-loop "Link to this heading")

To plot a hydrograph, the user simply needs to save the discharge value at a given link at each time step. This can be achieved using a Python list object. Before the time loop starts, the user initializes at least two loops, one to save the model time, and one to save the discharge value.

**Note**: Currently, this plotting solution assumes the user has identified a link to sample on. In this example, the active link connecting outlet node to its neighbor core node is selected. If, in other DEMs, more than one active link is identified on the outlet node, the link with the steepest topographic slope is recommended.

hydrograph\_time \= \[\]
discharge\_at\_outlet \= \[\]

#### During time loop:[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#during-time-loop "Link to this heading")

The OverlandFlow component calculates discharge in units of \[m2 s\-1\]. In this example (and in Adams et al., _in prep. for Geoscientific Model Development_), discharge is plotted as a volumetric flux. To convert the calculated discharge (_q_) to a volumetric discharge (_Q_), it can be multiplied by the fact width, or grid resolution (_dx_) of the model grid. Similarly, time is converted from units of seconds (_s_) to hours (_hr_)

hydrograph\_time.append(elapsed\_time / 3600.0)  \# convert seconds to hours
discharge\_at\_outlet.append(
    np.abs(of.q\[outlet\_link\]) \* rmg.dx
)  \# append discharge in m^3/s

#### After model run:[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#after-model-run "Link to this heading")

Once the model is done running, the hydrograph can be plotted using the matplotlib library. This is a simple example, for more customization options, we recommend the matplotlib [documentation](https://matplotlib.org//api/pyplot_api.html).

plt.plot(hydrograph\_time, discharge\_at\_outlet)
plt.ylabel("Time (hr)")
plt.xlabel("Discharge, (cms)")
plt.title("Outlet Hydrograph, Rainfall: 5 mm/hr in 2 hr")

[![Image 10: ../_images/OverlandFlow_Manual_Hydrograph.png](https://landlab.readthedocs.io/en/v2.9.2/_images/OverlandFlow_Manual_Hydrograph.png)](https://landlab.readthedocs.io/en/v2.9.2/_images/OverlandFlow_Manual_Hydrograph.png)**Figure 4**: Sample hydrograph from the test basin, after a storm with intensity of 5 mm/hr for a duration of 2 hr.

### Water depth maps[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#water-depth-maps "Link to this heading")

The Landlab plotting library includes a utility `imshow__grid` which can easily take a grid instance and plot data values from the grid in map view. This method also allows for customization of the plots. An example plotting water depth is shown here:

imshow\_grid(
    rmg,
    "surface\_water\_\_depth",
    plot\_name\="Water depth at time = 2 hr",
    var\_name\="Water Depth",
    var\_units\="m",
    grid\_units\=("m", "m"),
    cmap\="Blues",
)

[![Image 11: ../_images/OverlandFlow_Manual_WaterDepth.png](https://landlab.readthedocs.io/en/v2.9.2/_images/OverlandFlow_Manual_WaterDepth.png)](https://landlab.readthedocs.io/en/v2.9.2/_images/OverlandFlow_Manual_WaterDepth.png)**Figure 5**: Map of water depths at time = 2 hr, for the sample storm on the square basin (5 mm/hr over duration of 2 hr).

In this example, the water depths are plotted after 2 hours of model run time `model_run_time` = 7200 s in **Step 6**). The method `imshow__grid` takes a grid instance and data field by default. Optional methods displayed here include plot title, color bar title (`var__name`), color bar units (`var__units`), grid dimension units (`grid_units`), and matplotlib color map (`cmap`).

**Note**: As of right now, `imshow__grid` plots data on nodes and cells. If the user wants to plot data from link elements, a mapper from link to cell or link to node must be used first. An extensive list of Landlab [mapper](https://landlab.readthedocs.io/en/v2.9.2/user_guide/grid_methods/05_element_mapping.html#api-grid-grid-summary-mappers) methods is available in the documentation.

References[#](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#references "Link to this heading")
--------------------------------------------------------------------------------------------------------------------------------

Adams, J. M., Gasparini, N. M., Hobley, D. E. J., Tucker, G. E., Hutton, E. W. H., Nudurupati, S. S. and Istanbulluoglu, E. (2017) The Landlab OverlandFlow component: a Python library for modeling the shallow water equations across watersheds, in press.

Bates, P. D., Horritt, M. S., & Fewtrell, T. J. (2010). A simple inertial formulation of the shallow water equations for efficient two-dimensional flood inundation modelling. _Journal of Hydrology_, 387(1), 33-45.

Chow, V.T., 1959, Open-channel hydraulics: New York, McGraw-Hill, 680 p.

Coulthard, T. J., Neal, J. C., Bates, P. D., Ramirez, J., Almeida, G. A., and Hancock, G. R. (2013). Integrating the LISFLOOD-FP 2D hydrodynamic model with the CAESAR model: implications for modelling landscape evolution. _Earth Surface Processes and Landforms_, 38(15), 1897-1906.

de Almeida, G. A., Bates, P., Freer, J. E., & Souvignet, M. (2012). Improving the stability of a simple formulation of the shallow water equations for 2‐D flood modeling. _Water Resources Research_, 48(5).

Hobley, D. E. J., Adams, J. M., Nudurupati, S. S., Gasparini, N. M., Hutton, E. W. H., Istanbulluoglu, E. and Tucker, G. E. (2017) Landlab: a new, open-source, modular, Python-based tool for modelling Earth surface dynamics. _Earth Surface Dynamics_, 5(1), 21–46.

Hunter, N. M., Horritt, M. S., Bates, P. D., Wilson, M. D., & Werner, M. G. (2005). An adaptive time step solution for raster-based storage cell modelling of floodplain inundation. _Advances in Water Resources_, 28(9), 975-991.

[Next CellLab-CTS User Guide](https://landlab.readthedocs.io/en/v2.9.2/user_guide/cell_lab_user_guide.html)[Previous Frequently Asked Questions](https://landlab.readthedocs.io/en/v2.9.2/user_guide/faq.html)

Copyright © 2024, The Landlab Team

Made with [Sphinx](https://www.sphinx-doc.org/) and [@pradyunsg](https://pradyunsg.me/)'s [Furo](https://github.com/pradyunsg/furo)

[**_Powered by CSDMS_**](https://csdms.colorado.edu/)

On this page

*   [Overland Flow Component User Manual](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#)
    *   [Background on OverlandFlow component](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#background-on-overlandflow-component)
    *   [Model parameters and variables](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#model-parameters-and-variables)
    *   [Basic steps of an OverlandFlow model](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#basic-steps-of-an-overlandflow-model)
        *   [Step 1. Import the necessary libraries](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-1-import-the-necessary-libraries)
        *   [Step 2. Defining the model domain](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-2-defining-the-model-domain)
            *   [Reading in a watershed DEM](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#reading-in-a-watershed-dem)
            *   [Setting up a generic RasterModelGrid](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#setting-up-a-generic-rastermodelgrid)
        *   [Step 3. Setting the boundary conditions](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-3-setting-the-boundary-conditions)
            *   [Other boundary condition options](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#other-boundary-condition-options)
        *   [Step 4. Pre-processing the DEM (_Optional_)](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-4-pre-processing-the-dem-optional)
        *   [Step 5. Initializing the OverlandFlow component](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-5-initializing-the-overlandflow-component)
            *   [Stability criteria](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#stability-criteria)
        *   [Step 6. Precipitation inputs](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-6-precipitation-inputs)
            *   [Constant precipitation input](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#constant-precipitation-input)
            *   [Single storm event](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#single-storm-event)
        *   [Step 7. Iterate through time](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#step-7-iterate-through-time)
            *   [Adaptive time step](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#adaptive-time-step)
    *   [Plotting and visualization](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#plotting-and-visualization)
        *   [Hydrographs](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#hydrographs)
            *   [Before time loop:](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#before-time-loop)
            *   [During time loop:](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#during-time-loop)
            *   [After model run:](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#after-model-run)
        *   [Water depth maps](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#water-depth-maps)
    *   [References](https://landlab.readthedocs.io/en/v2.9.2/user_guide/overland_flow_user_guide.html#references)