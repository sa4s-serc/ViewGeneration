from diagrams import Diagram
from diagrams.programming.language import Dart
from diagrams.programming.framework import Flutter
from diagrams.generic.os import Android, IOS
from diagrams.generic.blank import Blank
from diagrams.onprem.database import PostgreSQL

with Diagram("Flutter Interview Preparation Repository Architecture", show=False, direction="TB"):
    with Diagram("Core Content Layer"):
        readme = Blank("README.md")
        flutter_internals = Blank("docs/flutter_internals.md")
        dart_internals = Blank("docs/dart_internals.md")
        
        content_group = [readme, flutter_internals, dart_internals]
    
    with Diagram("Question Categories"):
        software_dev = Blank("Software Development & Architecture")
        dart_lang = Dart("Dart")
        flutter_fw = Flutter("Flutter")
        
        categories_group = [software_dev, dart_lang, flutter_fw]
    
    with Diagram("Design Patterns"):
        creational = Blank("Creational Patterns")
        structural = Blank("Structural Patterns")
        behavioral = Blank("Behavioral Patterns")
        dependency_injection = Blank("Dependency Injection")
        
        patterns_group = [creational, structural, behavioral, dependency_injection]
    
    with Diagram("Target Platforms"):
        android = Android("Android")
        ios = IOS("iOS")
        
        platforms_group = [android, ios]
    
    # Connect core content to categories
    readme >> categories_group
    flutter_internals >> flutter_fw
    dart_internals >> dart_lang
    
    # Connect categories to design patterns
    software_dev >> patterns_group
    dart_lang >> patterns_group
    flutter_fw >> patterns_group
    
    # Connect to target platforms
    flutter_fw >> platforms_group