from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='JSeats Architecture')

# Define nodes for key components
dot.node('CLI', 'Command-Line Interface', shape='rectangle')
dot.node('PConfig', 'ProcessorConfig', shape='rectangle')
dot.node('SProcessor', 'SeatAllocatorProcessor', shape='rectangle')
dot.node('SResolver', 'SeatAllocatorResolver', shape='rectangle')
dot.node('SDefaultResolver', 'SeatAllocatorDefaultResolver', shape='rectangle')
dot.node('Tally', 'Tally', shape='rectangle')
dot.node('Candidate', 'Candidate', shape='rectangle')
dot.node('Methods', 'Seat Allocation Methods', shape='rectangle')
dot.node('Filters', 'Tally Filters', shape='rectangle')
dot.node('Decorators', 'Result Decorators', shape='rectangle')
dot.node('TieBreakers', 'Tie Breakers', shape='rectangle')
dot.node('XML', 'XML Serialization/Deserialization', shape='rectangle')
dot.node('Logging', 'Logging (SLF4J & Logback)', shape='rectangle')

# Define edges to represent communication and data flow
dot.edge('CLI', 'SProcessor', label='executes', style='dashed')
dot.edge('SProcessor', 'PConfig', label='uses', style='dashed')
dot.edge('SProcessor', 'SResolver', label='resolves', style='dashed')
dot.edge('SProcessor', 'SDefaultResolver', label='defaults', style='dashed')
dot.edge('SProcessor', 'Methods', label='applies', style='dashed')
dot.edge('SProcessor', 'Filters', label='applies', style='dashed')
dot.edge('SProcessor', 'Decorators', label='applies', style='dashed')
dot.edge('SProcessor', 'TieBreakers', label='uses', style='dashed')
dot.edge('SProcessor', 'Tally', label='processes', style='dashed')
dot.edge('Tally', 'Candidate', label='contains', style='dashed')
dot.edge('PConfig', 'XML', label='serializes/deserializes', style='dashed')
dot.edge('SProcessor', 'Logging', label='logs', style='dashed')

# Render the diagram
dot.render('jseats_architecture_diagram', format='png', cleanup=True)