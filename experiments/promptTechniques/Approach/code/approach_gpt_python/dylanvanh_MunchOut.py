from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='MunchOut Application Architecture')

# Define node attributes
frontend_style = {'shape': 'box', 'style': 'filled', 'color': 'lightblue'}
backend_style = {'shape': 'box', 'style': 'filled', 'color': 'lightgreen'}
repo_style = {'shape': 'box', 'style': 'dotted'}
bloc_style = {'shape': 'ellipse', 'style': 'filled', 'color': 'lightyellow'}
api_style = {'shape': 'ellipse', 'style': 'dashed'}

# Frontend components
dot.node('FE', 'Flutter Frontend', **frontend_style)
dot.node('AppWidget', 'App Widget', **frontend_style)
dot.node('AuthBloc', 'Auth BLoC', **bloc_style)
dot.node('LoginBloc', 'Login BLoC', **bloc_style)
dot.node('SignupBloc', 'Signup BLoC', **bloc_style)
dot.node('UserRepo', 'User Repository', **repo_style)
dot.node('RestaurantRepo', 'Restaurant Repository', **repo_style)
dot.node('CustomerRepo', 'Customer Repository', **repo_style)

# Backend components
dot.node('BE', 'Flask Backend', **backend_style)
dot.node('API', 'REST API', **api_style)
dot.node('CustomerModel', 'Customer Model', **backend_style)
dot.node('RestaurantModel', 'Restaurant Model', **backend_style)
dot.node('EventModel', 'Event Model', **backend_style)
dot.node('BookingModel', 'Booking Model', **backend_style)

# Frontend subsystem connections
dot.edge('FE', 'AppWidget', label='contains')
dot.edge('AppWidget', 'AuthBloc', label='uses')
dot.edge('AppWidget', 'LoginBloc', label='uses')
dot.edge('AppWidget', 'SignupBloc', label='uses')
dot.edge('AuthBloc', 'UserRepo', label='manages')
dot.edge('LoginBloc', 'UserRepo', label='manages')
dot.edge('SignupBloc', 'UserRepo', label='manages')
dot.edge('AuthBloc', 'RestaurantRepo', label='manages')
dot.edge('AuthBloc', 'CustomerRepo', label='manages')

# Backend subsystem connections
dot.edge('BE', 'API', label='exposes')
dot.edge('API', 'CustomerModel', label='manages')
dot.edge('API', 'RestaurantModel', label='manages')
dot.edge('API', 'EventModel', label='manages')
dot.edge('API', 'BookingModel', label='manages')

# Cross-system connections
dot.edge('UserRepo', 'API', label='calls', dir='both')
dot.edge('RestaurantRepo', 'API', label='calls', dir='both')
dot.edge('CustomerRepo', 'API', label='calls', dir='both')

# Render the graph
dot.render('munchout_architecture', format='png', cleanup=True)