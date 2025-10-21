from graphviz import Digraph

dot = Digraph(comment='Retail Analytics Componentized Patterns')

# Nodes
dot.node('A', 'Recommendation Systems', shape='box', style='filled', color='lightblue')
dot.node('B', 'Predictive Modeling', shape='box', style='filled', color='lightgreen')
dot.node('C', 'BigQuery ML', shape='box', style='filled', color='lightyellow')
dot.node('D', 'Workflow Orchestration', shape='box', style='filled', color='lightcoral')
dot.node('E', 'Serving Infrastructure', shape='box', style='filled', color='lightgray')
dot.node('F', 'Feature Engineering', shape='box', style='filled', color='lightpink')
dot.node('G', 'Data Handling', shape='box', style='filled', color='lightcyan')
dot.node('H', 'Model Evaluation', shape='box', style='filled', color='wheat')
dot.node('I', 'Marketing Activation', shape='box', style='filled', color='lemonchiffon')
dot.node('J', 'Data Visualization', shape='box', style='filled', color='lavender')

# Edges
dot.edge('A', 'C', 'Uses')
dot.edge('B', 'C', 'Uses')
dot.edge('C', 'D', 'Automates')
dot.edge('C', 'E', 'Deploys to')
dot.edge('F', 'C', 'Feeds into')
dot.edge('G', 'C', 'Data Source')
dot.edge('H', 'C', 'Evaluates')
dot.edge('I', 'C', 'Activates')
dot.edge('J', 'C', 'Visualizes')

# Render
dot.render('retail_analytics_componentized_patterns', view=True)