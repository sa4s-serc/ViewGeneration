from diagrams import Diagram, Cluster
from diagrams.generic.compute import Rack
from diagrams.programming.flowchart import Action, Decision

with Diagram("RNN Language Modeling Architecture", show=False):
    with Cluster("Jupyter Notebook Controller"):
        jupyter = Rack("RecurrentNeuralNetworkUsingTensorFlow.ipynb")

    with Cluster("RNN/LSTM Model"):
        embedding_layer = Action("Embedding Layer")
        lstm_layer = Action("LSTM Layer")
        dense_layer = Action("Dense Layer with Softmax")

    with Cluster("Penn Treebank Dataset"):
        dataset_loader = Action("Data Loader")
        data_iterator = Action("Data Iterator")

    with Cluster("Training & Evaluation"):
        training = Decision("Train Model")
        evaluation = Decision("Evaluate Performance")

    jupyter >> dataset_loader >> data_iterator
    jupyter >> embedding_layer >> lstm_layer >> dense_layer
    dense_layer >> training >> evaluation