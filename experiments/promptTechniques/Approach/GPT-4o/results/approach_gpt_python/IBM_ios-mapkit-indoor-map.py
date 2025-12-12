from diagrams import Diagram, Cluster
from diagrams.programming.language import Swift
from diagrams.programming.framework import React
from diagrams.onprem.client import Client
from diagrams.generic.database import SQL
from diagrams.onprem.compute import Server

with Diagram("Indoor Map with Heatmap Application", show=False, direction="LR"):
    
    ios_client = Client("iOS App")
    
    with Cluster("iOS Application"):
        view_controller = Swift("ViewController.swift")
        floorplan_overlay = Swift("FloorplanOverlay.swift")
        floorplan_overlay_renderer = Swift("FloorplanOverlayRenderer.swift")
        coordinate_converter = Swift("CoordinateConverter.swift")
        visible_map_region_delegate = Swift("VisibleMapRegionDelegate.swift")
        custom_polygons = Swift("CustomPolygons.swift")
        utilities = Swift("Utilities.swift")
        
    ios_client >> view_controller
    view_controller >> floorplan_overlay
    view_controller >> floorplan_overlay_renderer
    view_controller >> coordinate_converter
    view_controller >> visible_map_region_delegate
    view_controller >> custom_polygons
    view_controller >> utilities
    
    with Cluster("Backend Application"):
        backend_server = Server("Node.js Backend")
        app_js = React("app.js")
        routes_js = React("routes/*.js")
        models_js = React("models/*.js")
        real_data_js = React("real-data.js")
        random_js = React("random.js")
        
    backend_server >> app_js
    backend_server >> routes_js
    backend_server >> models_js
    backend_server >> real_data_js
    backend_server >> random_js
    
    with Cluster("Database"):
        mongo_db = SQL("MongoDB")
    
    backend_server >> mongo_db
    
    ios_client >> backend_server