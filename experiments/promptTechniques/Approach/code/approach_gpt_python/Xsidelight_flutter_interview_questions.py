from diagrams import Diagram, Cluster, Node
from diagrams.custom import Custom

with Diagram("Flutter Interview Preparation Repository Architecture", show=False, direction="TB"):
    with Cluster("Repository Structure"):
        readme = Custom("README.md", "./icons/markdown.png")
        flutter_internals = Custom("flutter_internals.md", "./icons/markdown.png")
        dart_internals = Custom("dart_internals.md", "./icons/markdown.png")

    with Cluster("Core Topics"):
        software_dev_arch = Node("Software Development & Architecture")
        dart = Node("Dart")
        flutter = Node("Flutter")

    with Cluster("Design Patterns"):
        creational = Node("Creational Patterns")
        structural = Node("Structural Patterns")
        behavioral = Node("Behavioral Patterns")
        dependency_injection = Node("Dependency Injection")

    readme >> [flutter_internals, dart_internals]
    
    flutter_internals >> flutter
    dart_internals >> dart
    
    software_dev_arch >> [creational, structural, behavioral, dependency_injection]

    software_dev_arch >> flutter