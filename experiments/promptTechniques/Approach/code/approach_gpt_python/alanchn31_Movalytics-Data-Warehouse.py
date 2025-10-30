from graphviz import Digraph

dot = Digraph(comment='Movalytics: Data Warehouse Solution for Movie Analytics')

# Nodes
dot.node('A', 'Movie Data Extraction (Kaggle)')
dot.node('B', 'CPI Data Extraction (St. Louis FRED)')
dot.node('C', 'Data Transformation (Apache Spark)')
dot.node('D', 'Staging Tables (Redshift)')
dot.node('E', 'Final Dimension Tables (Redshift)')
dot.node('F', 'Orchestration (Apache Airflow)')
dot.node('G', 'Data Quality Checks (DataQualityOperator)')
dot.node('H', 'Containerization (Docker)')
dot.node('I', 'Infrastructure as Code (Docker Compose)')

# Edges
dot.edge('A', 'C', label='Extract & Transform')
dot.edge('B', 'C', label='Extract & Transform')
dot.edge('C', 'D', label='Load to Staging')
dot.edge('D', 'E', label='Upsert to Final')
dot.edge('E', 'G', label='Data Quality Checks')
dot.edge('F', 'A', label='Orchestrate')
dot.edge('F', 'B', label='Orchestrate')
dot.edge('F', 'C', label='Orchestrate')
dot.edge('F', 'D', label='Orchestrate')
dot.edge('F', 'E', label='Orchestrate')
dot.edge('F', 'G', label='Orchestrate')
dot.edge('H', 'F', label='Containerize')
dot.edge('I', 'H', label='Define Infrastructure')

# Render the graph
dot.render('movalytics_architecture_diagram', format='png', cleanup=True)