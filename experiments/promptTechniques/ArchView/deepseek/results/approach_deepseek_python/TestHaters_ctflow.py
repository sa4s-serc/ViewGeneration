from diagrams import Diagram
from diagrams.programming.language import TypeScript, JavaScript
from diagrams.programming.framework import React
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.aws.ml import MachineLearning
from diagrams.generic.storage import Storage
from diagrams.custom import Custom

with Diagram("CTFLOW Architecture", show=False, direction="TB"):
    user = User("User")
    vscode = Custom("VS Code", "./vscode.png")
    webview_ui = React("React Webview UI")
    extension = TypeScript("VS Code Extension")
    compiler = JavaScript("Compiler")
    cypress = MachineLearning("Cypress")
    firebase = Custom("Firebase", "./firebase.png")
    custom_nodes = Custom("Custom Nodes", "./custom.png")
    test_flows = Storage(".ctflow Files")
    
    user >> vscode
    vscode >> extension
    extension >> webview_ui
    webview_ui >> custom_nodes
    webview_ui >> test_flows
    webview_ui >> compiler
    compiler >> cypress
    webview_ui >> firebase
    firebase >> webview_ui