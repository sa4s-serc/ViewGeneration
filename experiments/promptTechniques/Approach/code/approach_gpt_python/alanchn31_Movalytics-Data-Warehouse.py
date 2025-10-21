from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Movalytics: Data Warehouse Solution', format='png')

# Define nodes for the main components
dot.node('K', 'Kaggle (MovieLens)', shape='cylinder', style='filled', color='lightblue')
dot.node('F', 'St. Louis FRED', shape='cylinder', style='filled', color='lightblue')
dot.node('D', 'Docker', shape='box3d', style='filled', color='lightgrey')
dot.node('A', 'Apache Airflow', shape='ellipse', style='filled', color='lightgreen')
dot.node('S', 'Apache Spark', shape='ellipse', style='filled', color='lightgreen')
dot.node('R', 'Amazon Redshift', shape='cylinder', style='filled', color='lightblue')
dot.node('P', 'PostgreSQL', shape='cylinder', style='filled', color='lightblue')

# Define nodes for scripts and operators
dot.node('LST', 'load_staging_table.sh', shape='note', style='filled', color='white')
dot.node('LSR', 'load_staging_ratings.py', shape='note', style='filled', color='white')
dot.node('LSM', 'load_staging_movies.py', shape='note', style='filled', color='white')
dot.node('DQ', 'DataQualityOperator', shape='note', style='filled', color='white')

# Define edges between components to show data flow
dot.edge('K', 'LST', label='Data Extraction', color='blue')
dot.edge('F', 'LST', label='Data Extraction', color='blue')
dot.edge('LST', 'S', label='Data Load', color='blue')
dot.edge('S', 'LSR', label='Transform & Load Ratings', color='blue')
dot.edge('S', 'LSM', label='Transform & Load Movies', color='blue')
dot.edge('LSR', 'R', label='Load to Redshift', color='blue')
dot.edge('LSM', 'R', label='Load to Redshift', color='blue')
dot.edge('A', 'LSR', label='Orchestration', color='green')
dot.edge('A', 'LSM', label='Orchestration', color='green')
dot.edge('A', 'DQ', label='Data Quality Check', color='green')
dot.edge('DQ', 'R', label='Quality Assured', color='green')
dot.edge('P', 'A', label='Metadata Storage', color='black')
dot.edge('D', 'A', label='Containerized Environment', color='black')

# Save and render the graph
dot.render('movalytics_architecture_diagram')