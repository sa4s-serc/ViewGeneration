from diagrams import Diagram, Cluster
from diagrams.programming.language import Java
from diagrams.generic.os import Android, Windows, LinuxGeneral
from diagrams.generic.device import Mobile, Tablet
from diagrams.onprem.client import Client

with Diagram("ZWT Framework Architecture", show=False, direction="TB"):
    with Cluster("Platform Layer"):
        android = Android("Android")
        windows = Windows("Windows")
        linux = LinuxGeneral("Linux")
        embedded = Java("ME Embedded")
    
    with Cluster("ZWT Framework"):
        with Cluster("Core Abstraction"):
            zwt_component = Java("ZwtComponent")
            zwt_container = Java("ZwtContainer")
            zwt_graphics = Java("ZwtGraphics")
            zwt_keyboard = Java("ZwtKeyboard")
        
        with Cluster("UI Components"):
            zwt_frame = Java("ZwtFrame")
            zwt_panel = Java("ZwtPanel")
            zwt_label = Java("ZwtLabel")
            zwt_button = Java("ZwtButton")
        
        with Cluster("Layout Management"):
            zwt_layout = Java("ZwtLayout")
        
        with Cluster("Menus"):
            zwt_menu = Java("ZwtMenu")
            zwt_menuitem = Java("ZwtMenuItem")
        
        with Cluster("Styling"):
            zwt_color = Java("ZwtColor")
            zwt_font = Java("ZwtFont")
        
        with Cluster("Backgrounds"):
            zwt_floor = Java("ZwtFloor")
            zwt_transparent = Java("ZwtTransparentFloor")
            zwt_round = Java("ZwtRoundFloor")
    
    with Cluster("Application Layer"):
        app = Client("Java Application")
    
    app >> zwt_component
    zwt_component >> zwt_container
    zwt_component >> zwt_graphics
    zwt_component >> zwt_keyboard
    zwt_container >> zwt_frame
    zwt_container >> zwt_panel
    zwt_container >> zwt_label
    zwt_container >> zwt_button
    zwt_frame >> zwt_layout
    zwt_menu >> zwt_menuitem
    zwt_color >> zwt_component
    zwt_color >> zwt_button
    zwt_color >> zwt_label
    zwt_font >> zwt_component
    zwt_font >> zwt_button
    zwt_font >> zwt_label
    zwt_floor >> zwt_panel
    zwt_transparent >> zwt_panel
    zwt_round >> zwt_panel
    
    zwt_component >> android
    zwt_component >> windows
    zwt_component >> linux
    zwt_component >> embedded