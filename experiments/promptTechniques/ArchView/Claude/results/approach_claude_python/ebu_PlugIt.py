from graphviz import Digraph

dot = Digraph(comment='Rate Limit Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('API_Client', 'API Client')
dot.node('Quota_Monitor', 'Quota Monitor')
dot.node('Gemini_API', 'Gemini API')
dot.node('Retry_Handler', 'Retry Handler')
dot.node('Token_Counter', 'Token Counter')
dot.node('Cache', 'Cache')
dot.node('Error_Handler', 'Error Handler')

# Add connections
dot.edge('API_Client', 'Quota_Monitor', 'Requests')
dot.edge('Quota_Monitor', 'Gemini_API', 'Validated Requests')
dot.edge('Gemini_API', 'Token_Counter', 'Track Usage')
dot.edge('Token_Counter', 'Quota_Monitor', 'Update Limits')
dot.edge('Gemini_API', 'Error_Handler', '429 Error')
dot.edge('Error_Handler', 'Retry_Handler', 'Trigger Retry')
dot.edge('Retry_Handler', 'Cache', 'Store Failed Request')
dot.edge('Cache', 'Quota_Monitor', 'Retry After Delay')

# Print the source code
print(dot.source)

# Render the diagram
dot.render('rate_limit_architecture', format='png', cleanup=True)