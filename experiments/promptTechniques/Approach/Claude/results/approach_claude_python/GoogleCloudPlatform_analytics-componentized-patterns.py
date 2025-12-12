from graphviz import Digraph

dot = Digraph(comment='Retail Analytics Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded', fontname='Arial')

# Add components
dot.node('bqml', 'BigQuery ML\nModel Training & Evaluation')
dot.node('kfp', 'Kubeflow Pipelines\nWorkflow Orchestration')
dot.node('vertex', 'Vertex AI\nModel Serving')
dot.node('storage', 'Cloud Storage\nModel Artifacts')
dot.node('dataflow', 'Dataflow\nData Processing')
dot.node('datastore', 'Datastore\nItem Metadata')
dot.node('scann', 'ScaNN Service\nSimilarity Search')
dot.node('flask', 'Flask + Gunicorn\nServing Layer')
dot.node('ads', 'Google Ads API\nAudience Activation')
dot.node('studio', 'Data Studio\nVisualization')

# Add edges
dot.edge('dataflow', 'bqml', 'Data Transformation')
dot.edge('bqml', 'storage', 'Export Models')
dot.edge('storage', 'vertex', 'Deploy Models')
dot.edge('storage', 'scann', 'Load Embeddings')
dot.edge('kfp', 'bqml', 'Orchestrate Training')
dot.edge('kfp', 'vertex', 'Manage Deployment')
dot.edge('vertex', 'flask', 'Serve Predictions')
dot.edge('scann', 'flask', 'Real-time Search')
dot.edge('datastore', 'flask', 'Metadata Lookup')
dot.edge('bqml', 'ads', 'Audience Export')
dot.edge('bqml', 'studio', 'Model Analytics')

# Set graph attributes
dot.attr(label='Retail Analytics Architecture\nRecommendation & Prediction System')
dot.attr(fontname='Arial')
dot.attr(fontsize='16')

# Save the diagram
dot.render('retail_analytics_architecture', format='png', cleanup=True)