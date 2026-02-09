from graphviz import Digraph

dot = Digraph(comment='Movalytics Data Warehouse Architecture')
dot.attr(rankdir='TB', splines='ortho')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded,filled', fillcolor='lightblue')

# Add main components
dot.node('kaggle', 'Kaggle\nMovieLens Dataset')
dot.node('fred', 'FRED\nCPI Dataset')
dot.node('s3', 'Amazon S3\nData Lake')
dot.node('airflow', 'Apache Airflow\nOrchestration')
dot.node('spark', 'Apache Spark\nData Processing')
dot.node('redshift', 'Amazon Redshift\nData Warehouse')
dot.node('quality', 'Data Quality\nChecks')

# Add container components
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Docker Container Environment')
    c.attr('node', style='rounded,filled', fillcolor='lightgreen')
    c.node('webserver', 'Airflow\nWebserver')
    c.node('scheduler', 'Airflow\nScheduler')
    c.node('postgres', 'PostgreSQL\nMetadata DB')

# Add connections
dot.edge('kaggle', 's3', 'Extract')
dot.edge('fred', 's3', 'Extract')
dot.edge('s3', 'spark', 'Load')
dot.edge('spark', 'redshift', 'Transform & Load')
dot.edge('airflow', 'spark', 'Orchestrate')
dot.edge('airflow', 'quality', 'Trigger')
dot.edge('quality', 'redshift', 'Validate')

# Container connections
dot.edge('webserver', 'scheduler', 'Schedule DAGs')
dot.edge('scheduler', 'postgres', 'Store Metadata')
dot.edge('webserver', 'airflow', 'Control')

# Generate diagram
dot.render('movalytics_architecture', format='png', cleanup=True)