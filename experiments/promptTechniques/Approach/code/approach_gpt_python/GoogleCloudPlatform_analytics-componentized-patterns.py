from graphviz import Digraph

dot = Digraph(comment='Retail Analytics Componentized Patterns')

# Define nodes for key components
dot.node('BQML', 'BigQuery ML')
dot.node('KFP', 'Kubeflow Pipelines')
dot.node('RS', 'Recommendation Systems')
dot.node('PM', 'Predictive Modeling')
dot.node('FE', 'Feature Engineering')
dot.node('DH', 'Data Handling')
dot.node('MI', 'Model Infrastructure')
dot.node('ME', 'Model Evaluation')
dot.node('MA', 'Marketing Activation')
dot.node('DV', 'Data Visualization')

# Define edges for interactions
dot.edge('BQML', 'RS', label='Trains & Deploys Models')
dot.edge('BQML', 'PM', label='Trains & Deploys Models')
dot.edge('BQML', 'FE', label='Feature Engineering')
dot.edge('KFP', 'RS', label='Orchestrates Pipelines')
dot.edge('KFP', 'PM', label='Orchestrates Pipelines')
dot.edge('KFP', 'ME', label='CI/CD Integration')
dot.edge('RS', 'MI', label='Serves Models')
dot.edge('PM', 'MI', label='Serves Models')
dot.edge('DH', 'BQML', label='Processes Data')
dot.edge('DH', 'KFP', label='Processes Data')
dot.edge('MI', 'DV', label='Visualizes Data')
dot.edge('ME', 'MA', label='Activates Marketing')

# Render the diagram
dot.render('retail_analytics_componentized_patterns', format='png', view=True)