from graphviz import Digraph

# Create a Digraph object
diagram = Digraph(format='png')
diagram.attr(rankdir='LR', size='8,5')

# Define styles for nodes and edges
colors = {
    'smart_contract': 'lightblue',
    'backend_service': 'lightgreen',
    'frontend': 'lightyellow',
    'blockchain': 'lightcoral',
    'oracle': 'lightpink',
}

# Add nodes for core components
diagram.node('SmartContract', 'Smart Contract\n(PredictionCards.aes)', shape='rectangle', style='filled', fillcolor=colors['smart_contract'])
diagram.node('OracleService', 'Oracle Service\n(Java)', shape='rectangle', style='filled', fillcolor=colors['backend_service'])
diagram.node('ProcessPredictionService', 'Process Prediction Service\n(Java)', shape='rectangle', style='filled', fillcolor=colors['backend_service'])
diagram.node('Frontend', 'Frontend\n(React App)', shape='rectangle', style='filled', fillcolor=colors['frontend'])
diagram.node('AeternityBlockchain', 'Aeternity Blockchain', shape='rectangle', style='filled', fillcolor=colors['blockchain'])
diagram.node('Oracle', 'Oracle', shape='rectangle', style='filled', fillcolor=colors['oracle'])

# Add edges to represent interactions
diagram.edge('Frontend', 'SmartContract', label='Interact via API', dir='both')
diagram.edge('OracleService', 'AeternityBlockchain', label='Register & Query Oracle', dir='both')
diagram.edge('ProcessPredictionService', 'AeternityBlockchain', label='Monitor & Process', dir='both')
diagram.edge('OracleService', 'Oracle', label='Query Outcome', dir='both')
diagram.edge('ProcessPredictionService', 'OracleService', label='Trigger Query', dir='both')
diagram.edge('SmartContract', 'AeternityBlockchain', label='Execute & Store Data', dir='both')

# Render the diagram
diagram.render('architecture_diagram')