from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Salesforce REST/JSON Integration Architecture')

# Define nodes with distinct colors for different roles
dot.node('A', 'RestWrapper.cls', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('B', 'RestResponse.cls', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('C', 'RestCallout.cls', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('D', 'RestLogBuilder.cls', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('E', 'Rest_Log__c.object', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('F', 'ExampleRatingRestResource', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('G', 'ExampleRatingCallout', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('H', 'Test Classes', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('I', 'Salesforce DX Scripts', shape='rectangle', style='filled', fillcolor='lightyellow')

# Add edges between nodes to represent relationships
dot.edge('A', 'B', label='extends')
dot.edge('A', 'C', label='template method')
dot.edge('C', 'E', label='logs')
dot.edge('D', 'E', label='builds')
dot.edge('F', 'A', label='uses')
dot.edge('G', 'C', label='extends')
dot.edge('H', 'F', label='tests')
dot.edge('H', 'G', label='tests')
dot.edge('I', 'All Classes', label='deploys')

# Add legend
dot.node('Legend', 'Legend:\nBlue: Core Classes\nGreen: Example Implementations\nRed: Testing\nYellow: Configuration & Build', shape='note')

# Render the diagram
dot.render('salesforce_integration_architecture', format='png', cleanup=True)