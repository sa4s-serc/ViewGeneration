from diagrams import Diagram
from diagrams.generic.blank import Blank
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3

with Diagram("Tengine Lite Architecture", show=False):
    with Diagram("Model Conversion"):
        input_formats = Blank("Input Formats\n(ONNX, Caffe, TensorFlow, MXNet, TFLite, Darknet, NCNN)")
        tmfile_converter = Blank("TM2 Converter")
        tmfile_output = Blank("TM2 Format")
        
        input_formats >> tmfile_converter >> tmfile_output
    
    with Diagram("Core Inference Engine"):
        model_loader = Blank("Model Loader")
        inference_engine = Blank("Inference Engine")
        operator_library = Blank("Operator Library")
        
        tmfile_output >> model_loader >> inference_engine
        operator_library >> inference_engine
    
    with Diagram("Device Abstraction Layer"):
        device_interface = Blank("Device Interface")
        cpu_backend = Blank("CPU Backend")
        gpu_backend = Blank("GPU Backend")
        npu_backend = Blank("NPU Backend")
        
        inference_engine >> device_interface
        device_interface >> cpu_backend
        device_interface >> gpu_backend
        device_interface >> npu_backend
    
    with Diagram("Memory Management"):
        memory_allocator = Blank("Memory Allocator")
        gpu_memory = Blank("GPU Memory")
        cpu_memory = Blank("CPU Memory")
        
        device_interface >> memory_allocator
        memory_allocator >> gpu_memory
        memory_allocator >> cpu_memory
    
    with Diagram("Testing Framework"):
        test_runner = Blank("Test Runner")
        operator_tests = Blank("Operator Tests")
        model_tests = Blank("Model Tests")
        backend_tests = Blank("Backend Tests")
        
        inference_engine >> test_runner
        test_runner >> operator_tests
        test_runner >> model_tests
        test_runner >> backend_tests
    
    with Diagram("Python Interface"):
        pytengine = Blank("PyTengine")
        python_api = Blank("Python API")
        
        inference_engine >> pytengine >> python_api

    # Connect main components
    tmfile_output >> model_loader
    inference_engine >> device_interface
    device_interface >> memory_allocator