from graphviz import Digraph

dot = Digraph(comment='Deep Deblurring Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('frontend', 'Frontend\n(Vue.js)')
dot.node('backend', 'Backend\n(Flask)')
dot.node('model', 'Model Serving\n(TensorFlow Serving)')
dot.node('storage', 'Data Storage\n(Cloudinary)')
dot.node('redis', 'Redis\n(Caching)')
dot.node('postgres', 'PostgreSQL\n(Database)')

# Add connections
dot.edge('frontend', 'backend', 'REST API')
dot.edge('backend', 'model', 'gRPC')
dot.edge('backend', 'storage', 'API')
dot.edge('backend', 'redis', 'Cache Operations')
dot.edge('backend', 'postgres', 'SQL')

# Generate the diagram
dot.render('architecture', format='png', cleanup=True)