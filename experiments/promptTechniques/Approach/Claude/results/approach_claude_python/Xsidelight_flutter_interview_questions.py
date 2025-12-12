from diagrams import Cluster, Diagram, Edge
from diagrams.programming.framework import Flutter
from diagrams.programming.language import Dart
from diagrams.onprem.vcs import Github
from diagrams.generic.blank import Blank

with Diagram("Flutter Interview Preparation Repository Architecture", show=False):
    with Cluster("Documentation"):
        readme = Blank("README.md")
        flutter_internals = Blank("flutter_internals.md")
        dart_internals = Blank("dart_internals.md")

    with Cluster("Core Content"):
        software_dev = Blank("Software Development")
        dart_content = Dart("Dart")
        flutter_content = Flutter("Flutter")

    with Cluster("Topics"):
        with Cluster("Software Development"):
            arch = Blank("Architecture")
            patterns = Blank("Design Patterns")
            solid = Blank("SOLID")

        with Cluster("Dart"):
            vm = Blank("Dart VM")
            async_dart = Blank("Async/Await")
            isolates = Blank("Isolates")

        with Cluster("Flutter"):
            widgets = Blank("Widget System")
            state = Blank("State Management")
            testing = Blank("Testing")

    github = Github("Repository")

    # Connect main sections
    github >> [readme, flutter_internals, dart_internals]
    readme >> [software_dev, dart_content, flutter_content]

    # Connect topics to their sections
    software_dev >> [arch, patterns, solid]
    dart_content >> [vm, async_dart, isolates]
    flutter_content >> [widgets, state, testing]

    # Documentation connections
    flutter_internals >> flutter_content
    dart_internals >> dart_content