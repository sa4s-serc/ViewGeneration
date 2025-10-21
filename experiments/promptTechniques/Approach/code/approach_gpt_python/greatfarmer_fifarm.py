from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='FIFArm Application Architecture', format='png')

# Define nodes for key components
dot.node('A', 'HttpRequestService', shape='rectangle')
dot.node('B', 'MongoService', shape='rectangle')
dot.node('C', 'Scheduler', shape='rectangle')
dot.node('D', 'IndexController', shape='rectangle')
dot.node('E', 'PathController', shape='rectangle')
dot.node('F', 'JsonController', shape='rectangle')
dot.node('G', 'Thymeleaf Templates', shape='cylinder')
dot.node('H', 'MongoDB', shape='cylinder')
dot.node('I', 'LogService', shape='rectangle')
dot.node('J', 'EA Sports FUT API', shape='cylinder')

# Define edges for communication
dot.edge('A', 'J', label='Fetch Player Data', arrowhead='normal')
dot.edge('A', 'B', label='Store Data', arrowhead='normal')
dot.edge('B', 'H', label='MongoDB Operations', arrowhead='normal')
dot.edge('C', 'A', label='Scheduled Data Refresh', arrowhead='normal')
dot.edge('F', 'B', label='Search Player Data', arrowhead='normal')
dot.edge('D', 'G', label='Render View', arrowhead='normal')
dot.edge('E', 'G', label='Render View', arrowhead='normal')
dot.edge('F', 'G', label='Render View', arrowhead='normal')
dot.edge('F', 'J', label='RESTful API', arrowhead='normal')
dot.edge('D', 'I', label='Logging', arrowhead='normal')
dot.edge('E', 'I', label='Logging', arrowhead='normal')
dot.edge('F', 'I', label='Logging', arrowhead='normal')

# Save and render the diagram
dot.render('fifarm_architecture', view=False)