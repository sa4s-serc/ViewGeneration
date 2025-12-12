from diagrams import Diagram, Cluster
from diagrams.gcp.compute import KubernetesEngine
from diagrams.programming.language import Python
from diagrams.aws.storage import S3
from diagrams.azure.ml import AzureOpenAI
from diagrams.firebase.develop import Functions
from diagrams.gcp.ml import AIPlatform

with Diagram("RNN Language Modeling Architecture", show=False):
    with Cluster("Training Infrastructure"):
        model = AIPlatform("LSTM Model")
        code = Python("RecurrentNeuralNetworkUsingTensorFlow.ipynb")
        
    with Cluster("Data Storage & Processing"):
        data = S3("Penn Treebank Dataset")
        helper = Functions("Data Processing Scripts")
        
    with Cluster("Model Deployment"):
        api = AzureOpenAI("Language Model API")

    data >> helper >> code >> model >> api