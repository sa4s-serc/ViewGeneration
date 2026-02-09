from diagrams import Diagram
from diagrams.custom import Custom
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Internet
from diagrams.programming.framework import React
from diagrams.programming.language import JavaScript

with Diagram("Autopatzer Chess Board Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Diagram("Software Layer", show=False, direction="TB"):
        ui = React("React UI")
        electron = JavaScript("Electron App")
        perl_script = Custom("Perl Script", "./custom/perl.png")
        arduino = Custom("Arduino/Teensy", "./custom/arduino.png")
        
        ui >> electron
        electron >> perl_script
        perl_script >> arduino
    
    with Diagram("Hardware Layer", show=False, direction="TB"):
        motors = Custom("Stepper Motors", "./custom/motor.png")
        sensors = Custom("Hall Effect Sensors", "./custom/sensor.png")
        electromagnet = Custom("Electromagnet", "./custom/magnet.png")
        multiplexers = Custom("CD4051B Multiplexers", "./custom/chip.png")
        
        arduino >> motors
        arduino >> electromagnet
        sensors >> multiplexers >> arduino
    
    with Diagram("External Services", show=False, direction="TB"):
        lichess = Internet("Lichess API")
        websocket = Custom("WebSocket", "./custom/websocket.png")
        
        ui >> websocket >> lichess
        electron >> websocket
    
    user >> ui