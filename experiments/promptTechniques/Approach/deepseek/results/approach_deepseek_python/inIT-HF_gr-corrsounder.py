from diagrams import Diagram
from diagrams.programming.language import Cpp, Python
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.client import User
from diagrams.generic.os import LinuxGeneral
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git

with Diagram("gr-corrsounder Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Diagram("GNU Radio Flowgraph Layer"):
        grc_interface = Airflow("GRC Interface")
        
        with Diagram("Signal Processing Blocks"):
            sequence_gen = Cpp("Sequence Generation\n(FZC/MLS)")
            correlation = Cpp("Correlation Block")
            error_correction = Cpp("Error Correction")
            moving_avg = Cpp("Moving Average")
            sequence_gate = Cpp("Sequence Gate")
            ramdisk_sink = Cpp("Ramdisk File Sink")
            ir_snr = Cpp("IR SNR Detection")
            
            sequence_gen >> correlation
            correlation >> error_correction
            error_correction >> moving_avg
            moving_avg >> sequence_gate
            sequence_gate >> ramdisk_sink
            ramdisk_sink >> ir_snr
    
    with Diagram("Python Integration Layer"):
        swig_bindings = Python("SWIG Bindings")
        pycorrsounder = Python("pycorrsounder\n(Standalone)")
        unit_tests = Python("Unit Tests")
        
        swig_bindings >> pycorrsounder
        pycorrsounder >> unit_tests
    
    with Diagram("Supporting Infrastructure"):
        cmake = LinuxGeneral("CMake Build System")
        doxygen = LinuxGeneral("Doxygen\nDocumentation")
        gnu_radio = LinuxGeneral("GNU Radio\nFramework")
        boost_libs = LinuxGeneral("Boost Libraries")
        
        cmake >> gnu_radio
        gnu_radio >> boost_libs
    
    user >> grc_interface
    grc_interface >> sequence_gen
    grc_interface >> swig_bindings
    swig_bindings >> sequence_gen
    pycorrsounder >> correlation
    cmake >> sequence_gen
    doxygen >> swig_bindings