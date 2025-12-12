from diagrams import Diagram, Cluster
from diagrams.aws.mobile import Mobile
from diagrams.aws.compute import EC2
from diagrams.aws.ml import MachineLearning
from diagrams.aws.storage import S3
from diagrams.onprem.client import Client
from diagrams.programming.framework import Flask
from diagrams.generic.os import Android
from diagrams.generic.compute import Rack

with Diagram("Graphrec Mobile Application Architecture", show=False, direction="TB"):
    user = Client("User")
    
    with Cluster("Mobile Client"):
        android_app = Android("Android Application")
        main_activity = Mobile("MainActivity")
        camera_activity = Mobile("CameraActivity")
        result_activity = Mobile("ResultActivity")
        image_upload_task = Mobile("ImageUploadTask")
        
        android_app >> main_activity
        main_activity >> camera_activity
        camera_activity >> image_upload_task
        image_upload_task >> result_activity
    
    with Cluster("Backend Server"):
        flask_server = Flask("Flask Server")
        server_py = EC2("server.py")
        graph_classifier = MachineLearning("graph_classifier.py")
        graph_images = S3("graph_images.py")
        generate_data = EC2("generate_data.py")
        cn_py = MachineLearning("cn.py")
        
        flask_server >> server_py
        server_py >> graph_classifier
        server_py >> graph_images
        server_py >> generate_data
        server_py >> cn_py
    
    neural_network = MachineLearning("Neural Network (CNN)")
    data_generation = Rack("Data Generation")
    
    user >> android_app
    image_upload_task >> flask_server
    flask_server >> neural_network
    data_generation >> neural_network
    neural_network >> result_activity