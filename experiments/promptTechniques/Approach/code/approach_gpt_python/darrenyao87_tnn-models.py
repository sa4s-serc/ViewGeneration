from diagrams import Diagram, Cluster, Node
from diagrams.custom import Custom

# Creating custom node types for different technologies
class HiAI(Node):
    _provider = "custom"
    _icon_dir = "."
    _icon = "custom_hiai.png"

class TNN(Node):
    _provider = "custom"
    _icon_dir = "."
    _icon = "custom_tnn.png"

class ONNX(Node):
    _provider = "custom"
    _icon_dir = "."
    _icon = "custom_onnx.png"

class EncoderDecoder(Node):
    _provider = "custom"
    _icon_dir = "."
    _icon = "custom_encoder_decoder.png"

class ObjectDetection(Node):
    _provider = "custom"
    _icon_dir = "."
    _icon = "custom_object_detection.png"

class OCR(Node):
    _provider = "custom"
    _icon_dir = "."
    _icon = "custom_ocr.png"

class BERT(Node):
    _provider = "custom"
    _icon_dir = "."
    _icon = "custom_bert.png"

class PreProcessing(Node):
    _provider = "custom"
    _icon_dir = "."
    _icon = "custom_preprocessing.png"

class Hardware(Node):
    _provider = "custom"
    _icon_dir = "."
    _icon = "custom_hardware.png"

# Creating the diagram
with Diagram("AI Deployment Architecture", show=False, direction="TB"):

    with Cluster("Model Management"):
        hiai = HiAI("HiAI DDK")
        tnn = TNN("TNN Framework")
        onnx = ONNX("ONNX")

    with Cluster("AI Pre-Processing"):
        aipp = PreProcessing("AIPP Configuration")

    with Cluster("Neural Network Layers"):
        encoder_decoder = EncoderDecoder("Encoder-Decoder Structure")
        object_detection = ObjectDetection("Object Detection & Classification")
        ocr = OCR("OCR")
        bert = BERT("BERT Models")

    with Cluster("Hardware Acceleration"):
        hardware = Hardware("ION Buffer")

    # Defining relationships
    hiai >> aipp
    hiai >> encoder_decoder
    tnn >> encoder_decoder
    onnx >> tnn
    encoder_decoder >> object_detection
    encoder_decoder >> ocr
    encoder_decoder >> bert
    encoder_decoder >> hardware