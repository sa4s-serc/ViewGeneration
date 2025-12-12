from diagrams import Diagram
from diagrams.generic.device import Mobile
from diagrams.generic.compute import Rack
from diagrams.generic.storage import Storage
from diagrams.generic.network import Firewall
from diagrams.generic.os import Windows
from diagrams.programming.framework import Angular
from diagrams.programming.language import TypeScript
from diagrams.onprem.client import User

with Diagram("Solenya Framework Architecture", show=False, direction="TB"):
    user = User("User")
    browser = Angular("Browser")
    app = Rack("App")
    component = Rack("Component")
    router = Rack("Router")
    validator = Rack("Validator")
    storage = Storage("Storage")
    time_travel = Rack("TimeTravel")
    virtual_dom = Rack("Virtual DOM")
    html_helpers = Rack("HTML Helpers")
    widgets = Rack("Widgets")
    typestyle = TypeScript("Typestyle")

    user >> browser
    browser >> app
    app >> component
    component >> router
    component >> validator
    component >> storage
    component >> time_travel
    component >> virtual_dom
    virtual_dom >> html_helpers
    virtual_dom >> widgets
    component >> typestyle