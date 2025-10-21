from diagrams import Diagram, Cluster, Node
from diagrams.custom import Custom

with Diagram("ZWT Framework Architecture", show=False):
    with Cluster("ZWT Framework"):
        core_abstraction = Custom("Core Abstraction", "./resources/core_abstraction.png")
        
        with Cluster("UI Components"):
            zwt_component = Custom("ZwtComponent", "./resources/component.png")
            zwt_container = Custom("ZwtContainer", "./resources/container.png")
            zwt_frame = Custom("ZwtFrame", "./resources/frame.png")
            zwt_panel = Custom("ZwtPanel", "./resources/panel.png")
            zwt_label = Custom("ZwtLabel", "./resources/label.png")
            zwt_button = Custom("ZwtButton", "./resources/button.png")
        
        with Cluster("Graphics and Input"):
            zwt_graphics = Custom("ZwtGraphics", "./resources/graphics.png")
            zwt_keyboard = Custom("ZwtKeyboard", "./resources/keyboard.png")
        
        with Cluster("Layout Management"):
            zwt_layout = Custom("ZwtLayout", "./resources/layout.png")
        
        with Cluster("Menus"):
            zwt_menu = Custom("ZwtMenu", "./resources/menu.png")
            zwt_menu_item = Custom("ZwtMenuItem", "./resources/menu_item.png")
            zwt_menu_container = Custom("ZwtMenuContainer", "./resources/menu_container.png")
        
        with Cluster("Styling"):
            zwt_color = Custom("ZwtColor", "./resources/color.png")
            zwt_font = Custom("ZwtFont", "./resources/font.png")
        
        with Cluster("Backgrounds (Floors)"):
            zwt_floor = Custom("ZwtFloor", "./resources/floor.png")
            zwt_transparent_floor = Custom("ZwtTransparentFloor", "./resources/transparent_floor.png")
            zwt_round_floor = Custom("ZwtRoundFloor", "./resources/round_floor.png")
        
        with Cluster("Utility"):
            zwt_drawing = Custom("ZwtDrawing", "./resources/drawing.png")
        
        core_abstraction >> zwt_component
        zwt_component >> zwt_container
        zwt_container >> [zwt_frame, zwt_panel]
        zwt_frame >> zwt_label
        zwt_panel >> zwt_button
        zwt_graphics - zwt_component
        zwt_keyboard - zwt_component
        zwt_layout - zwt_container
        zwt_menu_container >> zwt_menu
        zwt_menu >> zwt_menu_item
        zwt_color - zwt_component
        zwt_font - zwt_component
        zwt_floor >> [zwt_transparent_floor, zwt_round_floor]
        zwt_drawing - zwt_graphics