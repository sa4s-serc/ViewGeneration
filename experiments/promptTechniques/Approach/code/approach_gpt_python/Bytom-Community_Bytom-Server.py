from graphviz import Digraph

# Initialize the graph
dot = Digraph(comment='Bytom Server Architecture')

# Define nodes
dot.node('A', 'Blockchain Core', shape='rectangle')
dot.node('B', 'Peer-to-Peer Networking', shape='rectangle')
dot.node('C', 'Block Synchronization', shape='rectangle')
dot.node('D', 'Mining', shape='rectangle')
dot.node('E', 'Data Store Abstraction', shape='rectangle')
dot.node('F', 'gRPC API', shape='rectangle')
dot.node('G', 'Access Token Management', shape='rectangle')
dot.node('H', 'Transaction Processing', shape='rectangle')
dot.node('I', 'Transaction Builder', shape='rectangle')
dot.node('J', 'Transaction Indexing', shape='rectangle')
dot.node('K', 'Bytom VM', shape='rectangle')
dot.node('L', 'State Management', shape='rectangle')
dot.node('M', 'Wallet Functionality', shape='rectangle')
dot.node('N', 'Pseudohsm', shape='rectangle')
dot.node('O', 'Secure Connections', shape='rectangle')
dot.node('P', 'Overlap Checking', shape='rectangle')

# Define edges
dot.edge('A', 'B', label='BlockRequest/Response, TransactionNotify')
dot.edge('A', 'C', label='Fetch blocks & transactions')
dot.edge('A', 'D', label='Tensority algorithm')
dot.edge('A', 'E', label='LevelDB')
dot.edge('F', 'G', label='Secures RPC API')
dot.edge('H', 'I', label='Composable actions')
dot.edge('H', 'J', label='Handles UTXOs')
dot.edge('H', 'K', label='Executes smart contracts')
dot.edge('L', 'H', label='UTXO model')
dot.edge('M', 'N', label='For development/testing')
dot.edge('O', 'B', label='Encrypted connections')
dot.edge('P', 'E', label='Improves data consistency')

# Render the graph
dot.render('bytom_server_architecture', format='png', cleanup=True)