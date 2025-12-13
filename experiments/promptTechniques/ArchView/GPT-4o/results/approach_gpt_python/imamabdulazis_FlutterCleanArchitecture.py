from diagrams import Diagram, Cluster, Node
from diagrams.generic.blank import Blank

class Component(Node):
    _provider = "generic"
    _icon_dir = ""
    fontcolor = "#ffffff"

with Diagram("Flutter Clean Architecture", show=False, direction="TB"):
    with Cluster("Presentation Layer"):
        ui_components = Component("UI Components")
        bloc = Component("BLoC")

    with Cluster("Domain Layer"):
        use_cases = Component("Use Cases")
        entities = Component("Entities")

    with Cluster("Data Layer"):
        repositories = Component("Repositories")
        data_sources = Component("Data Sources")

    with Cluster("Core Layer"):
        networking = Component("Networking")
        dependency_injection = Component("Dependency Injection")
        error_handling = Component("Error Handling")

    # Connections
    ui_components >> bloc
    bloc >> use_cases
    use_cases >> entities
    use_cases >> repositories
    repositories >> data_sources

    # Core connections
    networking >> data_sources
    dependency_injection >> repositories
    error_handling >> ui_components