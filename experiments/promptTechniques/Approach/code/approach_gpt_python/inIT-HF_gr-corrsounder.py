from diagrams import Diagram, Cluster, Node
from diagrams.custom import Custom

with Diagram("gr-corrsounder Architecture", show=False, direction="TB"):

    with Cluster("GNU Radio Integration"):
        gr_blocks = Custom("Custom Blocks", "./icons/gr_icon.png")
        
        seq_gen = Node("Sequence Generation")
        correlation = Node("Correlation")
        error_correction = Node("Error Correction")
        moving_avg = Node("Moving Average")
        sequence_gate = Node("Sequence Gate")
        ramdisk_sink = Node("Ramdisk File Sink")
        ir_snr = Node("IR SNR")
        
        gr_blocks >> seq_gen
        gr_blocks >> correlation
        gr_blocks >> error_correction
        gr_blocks >> moving_avg
        gr_blocks >> sequence_gate
        gr_blocks >> ramdisk_sink
        gr_blocks >> ir_snr

    with Cluster("SWIG - Python Bindings"):
        swig = Node("SWIG Interface")
        python_bindings = Node("Python Bindings")
        
        gr_blocks >> swig
        swig >> python_bindings

    with Cluster("Standalone Python Package"):
        pycorrsounder = Node("pycorrsounder")
        
        algos = Node("Algorithms")
        pycorrsounder >> algos

    with Cluster("GRC Integration"):
        grc_xml = Node("GRC XML Files")
        grc_tool = Node("GNU Radio Companion")
        
        gr_blocks >> grc_xml
        grc_xml >> grc_tool

    with Cluster("Testing Infrastructure"):
        unit_tests = Node("Unit Tests")
        validation = Node("Validation")
        
        pycorrsounder >> unit_tests
        unit_tests >> validation

    with Cluster("Documentation Parsing"):
        doxygen = Node("Doxygen XML")
        parse_docs = Node("Parse and Simplify")
        
        doxygen >> parse_docs