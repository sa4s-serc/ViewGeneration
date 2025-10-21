from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Rinkako_CStoreDB Architecture')

# Define the styles for the nodes and edges
dot.attr('node', shape='rectangle', style='filled', color='lightblue')
dot.attr('edge', arrowhead='normal')

# Add nodes for each layer
dot.node('DBInterface', 'DBInterface\n(DBController, DBConnectionPool)')
dot.node('DBCompiler', 'DBCompiler\n(LexicalAnalyzer, SyntaxParser, Pile, CSDatabase, DBBridge)')
dot.node('DBEngine', 'DBEngine\n(FileManager, TableManager, DBAllocator, DBLock, DBTransaction)')

# Add edges to represent dependencies and interactions
dot.edge('DBInterface', 'DBCompiler', label='calls')
dot.edge('DBCompiler', 'DBEngine', label='executes')

# Add nodes for design patterns
dot.node('Singleton', 'Singleton\n(FileManager, DBAllocator, DBConnectionPool, TableManager)', color='lightgrey')
dot.node('Base Class', 'Base Class\n(DBObject)', color='lightgrey')
dot.node('Bridge', 'Bridge\n(DBBridge)', color='lightgrey')

# Add edges to represent design patterns
dot.edge('DBEngine', 'Singleton', label='uses', style='dashed')
dot.edge('DBEngine', 'Base Class', label='extends', style='dashed')
dot.edge('DBCompiler', 'Bridge', label='implements', style='dashed')

# Render the diagram to a file
dot.render('rinkako_cstoredb_architecture', view=True)