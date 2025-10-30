from graphviz import Digraph

def create_diagram():
    dot = Digraph(comment='Rinkako_CStoreDB Architecture')

    # Layers
    dot.node('Interface', 'DBInterface', shape='rectangle', style='filled', color='lightblue')
    dot.node('Compiler', 'DBCompiler', shape='rectangle', style='filled', color='lightgreen')
    dot.node('Engine', 'DBEngine', shape='rectangle', style='filled', color='lightcoral')

    # Components
    dot.node('DBController', 'DBController', shape='rectangle')
    dot.node('DBConnectionPool', 'DBConnectionPool', shape='rectangle')
    dot.node('LexicalAnalyzer', 'LexicalAnalyzer', shape='rectangle')
    dot.node('SyntaxParser', 'SyntaxParser', shape='rectangle')
    dot.node('Pile', 'Pile', shape='rectangle')
    dot.node('CSDatabase', 'CSDatabase', shape='rectangle')
    dot.node('DBBridge', 'DBBridge', shape='rectangle')
    dot.node('FileManager', 'FileManager', shape='rectangle')
    dot.node('TableManager', 'TableManager', shape='rectangle')
    dot.node('DBAllocator', 'DBAllocator', shape='rectangle')
    dot.node('DBLock', 'DBLock', shape='rectangle')
    dot.node('DBTransaction', 'DBTransaction', shape='rectangle')

    # Grouping components into layers
    dot.edge('Interface', 'DBController')
    dot.edge('Interface', 'DBConnectionPool')
    dot.edge('Compiler', 'LexicalAnalyzer')
    dot.edge('Compiler', 'SyntaxParser')
    dot.edge('Compiler', 'Pile')
    dot.edge('Compiler', 'CSDatabase')
    dot.edge('Compiler', 'DBBridge')
    dot.edge('Engine', 'FileManager')
    dot.edge('Engine', 'TableManager')
    dot.edge('Engine', 'DBAllocator')
    dot.edge('Engine', 'DBLock')
    dot.edge('Engine', 'DBTransaction')

    # Connectors and interactions
    dot.edge('DBController', 'DBConnectionPool', label='uses', dir='forward')
    dot.edge('DBConnectionPool', 'DBBridge', label='connects to', dir='forward')
    dot.edge('LexicalAnalyzer', 'SyntaxParser', label='parses', dir='forward')
    dot.edge('SyntaxParser', 'Pile', label='translates', dir='forward')
    dot.edge('Pile', 'CSDatabase', label='executes', dir='forward')
    dot.edge('CSDatabase', 'FileManager', label='manages', dir='forward')
    dot.edge('CSDatabase', 'TableManager', label='manages', dir='forward')
    dot.edge('CSDatabase', 'DBAllocator', label='allocates', dir='forward')
    dot.edge('TableManager', 'DBLock', label='locks', dir='forward')
    dot.edge('TableManager', 'DBTransaction', label='handles', dir='forward')

    dot.render('rinkako_cstoredb_architecture', format='png', cleanup=True)

create_diagram()