from graphviz import Digraph

dot = Digraph(comment='Spark Architecture Overview')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Core Components
dot.node('core', 'Spark Core\n(RDD Operations, Data Loading)', style='filled', fillcolor='lightblue')

# Higher Level Components
dot.node('sql', 'Spark SQL\n(DataFrames, SQL Queries)', style='filled', fillcolor='lightgreen')
dot.node('mllib', 'Spark MLlib\n(Machine Learning)', style='filled', fillcolor='lightpink')
dot.node('streaming', 'Spark Streaming\n(Real-time Processing)', style='filled', fillcolor='lightyellow')
dot.node('graphx', 'GraphX\n(Graph Processing)', style='filled', fillcolor='lightgray')

# Integration Components
dot.node('airflow', 'Apache Airflow\n(Orchestration)', style='filled', fillcolor='wheat')
dot.node('k8s', 'Kubernetes\n(Container Management)', style='filled', fillcolor='lightcyan')
dot.node('postgres', 'PostgreSQL\n(Data Storage)', style='filled', fillcolor='peachpuff')

# Add edges
dot.edge('core', 'sql')
dot.edge('core', 'mllib')
dot.edge('core', 'streaming')
dot.edge('core', 'graphx')
dot.edge('airflow', 'core', 'orchestrates')
dot.edge('k8s', 'core', 'manages')
dot.edge('sql', 'postgres', 'reads/writes')

# Render the diagram
dot.render('spark_architecture', format='png', cleanup=True)