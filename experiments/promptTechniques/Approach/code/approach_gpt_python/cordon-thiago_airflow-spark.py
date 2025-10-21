from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Apache Spark Integration Architecture')

# Set graph attributes
dot.attr(rankdir='LR', size='8,5')

# Add nodes for core components
dot.node('A', 'Core Spark Operations', shape='box')
dot.node('B', 'Spark SQL', shape='box')
dot.node('C', 'Spark MLlib', shape='box')
dot.node('D', 'Spark Streaming', shape='box')
dot.node('E', 'GraphX', shape='box')

# Add nodes for technology stack
dot.node('F', 'Apache Airflow', shape='cylinder')
dot.node('G', 'Kubernetes', shape='cylinder')
dot.node('H', 'PostgreSQL', shape='cylinder')
dot.node('I', 'R Language', shape='cylinder')
dot.node('J', 'Java Interoperability', shape='cylinder')

# Add edges to represent data flow and integration
dot.edge('F', 'A', label='Orchestrates', arrowhead='vee')
dot.edge('G', 'A', label='Deploys', arrowhead='vee')
dot.edge('A', 'B', label='Uses', arrowhead='vee')
dot.edge('A', 'C', label='Uses', arrowhead='vee')
dot.edge('A', 'D', label='Uses', arrowhead='vee')
dot.edge('A', 'E', label='Uses', arrowhead='vee')
dot.edge('H', 'A', label='Reads/Writes', arrowhead='vee')
dot.edge('I', 'A', label='SparkR', arrowhead='vee')
dot.edge('J', 'C', label='MLlib Algorithms', arrowhead='vee')

# Render the diagram
dot.render('spark_integration_architecture', format='png', cleanup=True)