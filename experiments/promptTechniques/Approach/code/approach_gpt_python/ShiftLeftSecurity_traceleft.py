from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Repository Architecture', format='png')

# Define styles for different components
dot.attr('node', shape='rectangle', style='filled', fillcolor='lightblue')
dot.attr('edge', style='dashed')

# Main sections
dot.node('A', 'Internationalized Text Processing (golang.org/x/text)')
dot.node('B', 'Low-Level System Interaction (golang.org/x/sys)')
dot.node('C', 'Command-Line Interface (github.com/spf13/cobra)')
dot.node('D', 'Core Library Components')

# Components under Internationalized Text Processing
dot.node('A1', 'Unicode Normalization')
dot.node('A2', 'Collation')
dot.node('A3', 'BiDi Text Handling')
dot.node('A4', 'IDNA')
dot.node('A5', 'Unicode Case Conversion')
dot.node('A6', 'Character Encoding')
dot.node('A7', 'gotext Command-Line Tool')
dot.node('A8', 'CLDR Integration')

# Components under Low-Level System Interaction
dot.node('B1', 'OS Abstraction (unix)')
dot.node('B2', 'System Calls')
dot.node('B3', 'Windows and Linux API Binding')
dot.node('B4', 'Platform-Specific Code')

# Components under Command-Line Interface
dot.node('C1', 'Hierarchical Commands')
dot.node('C2', 'Arguments and Flags')
dot.node('C3', 'Command-Line Generator')

# Components under Core Library Components
dot.node('D1', 'eBPF Interaction')
dot.node('D2', 'YAML Processing')
dot.node('D3', 'Caching Mechanisms')
dot.node('D4', 'File System Event Watching')
dot.node('D5', 'Text Processing Functions')
dot.node('D6', 'Command Line Interaction')

# Connect main sections to their components
dot.edge('A', 'A1')
dot.edge('A', 'A2')
dot.edge('A', 'A3')
dot.edge('A', 'A4')
dot.edge('A', 'A5')
dot.edge('A', 'A6')
dot.edge('A', 'A7')
dot.edge('A', 'A8')

dot.edge('B', 'B1')
dot.edge('B', 'B2')
dot.edge('B', 'B3')
dot.edge('B', 'B4')

dot.edge('C', 'C1')
dot.edge('C', 'C2')
dot.edge('C', 'C3')

dot.edge('D', 'D1')
dot.edge('D', 'D2')
dot.edge('D', 'D3')
dot.edge('D', 'D4')
dot.edge('D', 'D5')
dot.edge('D', 'D6')

# Connections between different main sections
dot.edge('A7', 'C')  # gotext CLI tool in Text Processing to CLI section
dot.edge('D2', 'C2')  # YAML Processing to CLI Arguments and Flags
dot.edge('D3', 'D')  # Caching Mechanisms to Core Library Components

# Render the diagram
dot.render('repository_architecture_diagram', view=True)