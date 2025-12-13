from graphviz import Digraph

dot = Digraph(comment='jseats Architecture', format='png')

# Components
dot.node('CLI', 'Command-Line Interface')
dot.node('SeatAllocatorLauncher', 'SeatAllocatorLauncher.java')
dot.node('ProcessorConfig', 'ProcessorConfig.java')
dot.node('SeatAllocatorProcessor', 'SeatAllocatorProcessor.java')
dot.node('SeatAllocatorResolver', 'SeatAllocatorResolver.java')
dot.node('SeatAllocatorDefaultResolver', 'SeatAllocatorDefaultResolver.java')
dot.node('Tally', 'Tally Object')
dot.node('XML', 'XML Serialization/Deserialization')

# Seat Allocation Methods
dot.node('Majority', 'Majority-based')
dot.node('LargestRemainder', 'Largest Remainder')
dot.node('HighestAverages', 'Highest Averages')
dot.node('EqualProportions', 'Equal Proportions')
dot.node('RankedVotes', 'Ranked by Votes')

# Customization
dot.node('TallyFilters', 'Tally Filters')
dot.node('ResultDecorators', 'Result Decorators')
dot.node('TieBreakers', 'Tie Breakers')

# Logging
dot.node('Logging', 'Logging (SLF4J & Logback)')

# Relationships
dot.edge('CLI', 'SeatAllocatorLauncher')
dot.edge('SeatAllocatorLauncher', 'SeatAllocatorProcessor')
dot.edge('SeatAllocatorProcessor', 'ProcessorConfig')
dot.edge('SeatAllocatorProcessor', 'SeatAllocatorResolver')
dot.edge('SeatAllocatorProcessor', 'Tally')
dot.edge('SeatAllocatorResolver', 'SeatAllocatorDefaultResolver')
dot.edge('ProcessorConfig', 'XML')

# Seat Allocation Methods Relationships
dot.edge('SeatAllocatorProcessor', 'Majority')
dot.edge('SeatAllocatorProcessor', 'LargestRemainder')
dot.edge('SeatAllocatorProcessor', 'HighestAverages')
dot.edge('SeatAllocatorProcessor', 'EqualProportions')
dot.edge('SeatAllocatorProcessor', 'RankedVotes')

# Customization Relationships
dot.edge('SeatAllocatorProcessor', 'TallyFilters')
dot.edge('SeatAllocatorProcessor', 'ResultDecorators')
dot.edge('SeatAllocatorProcessor', 'TieBreakers')

# Logging Relationship
dot.edge('SeatAllocatorProcessor', 'Logging')

# Save and render the diagram
dot.render('jseats_architecture_diagram')