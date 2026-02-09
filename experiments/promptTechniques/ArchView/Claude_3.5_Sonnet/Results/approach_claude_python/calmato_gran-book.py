from graphviz import Digraph

dot = Digraph(comment='Gran Book Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('web_admin', 'Web Admin Panel\n(Nuxt.js)')
dot.node('mobile', 'Mobile App')
dot.node('api_gateway', 'API Gateway')
dot.node('auth_svc', 'Auth Service\n(Firebase)')
dot.node('book_svc', 'Book Service')
dot.node('user_svc', 'User Service')
dot.node('chat_svc', 'Chat Service')
dot.node('review_svc', 'Review Service')
dot.node('db', 'Database')
dot.node('storage', 'Storage\n(Images)')

# Add edges
dot.edge('web_admin', 'api_gateway')
dot.edge('mobile', 'api_gateway')
dot.edge('api_gateway', 'auth_svc')
dot.edge('api_gateway', 'book_svc')
dot.edge('api_gateway', 'user_svc')
dot.edge('api_gateway', 'chat_svc')
dot.edge('api_gateway', 'review_svc')
dot.edge('book_svc', 'db')
dot.edge('user_svc', 'db')
dot.edge('chat_svc', 'db')
dot.edge('review_svc', 'db')
dot.edge('book_svc', 'storage')

# Render the graph
dot.render('gran_book_architecture', format='png', cleanup=True)