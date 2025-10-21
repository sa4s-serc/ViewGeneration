from graphviz import Digraph

def generate_factom_sdk_diagram():
    dot = Digraph(comment='Factom Harmony Connect API Python SDK Architecture')
    
    # Define nodes
    dot.node('FactomSDK', 'FactomSDK Class', shape='rectangle', style='filled', fillcolor='lightblue')
    dot.node('Client', 'FactomClient', shape='rectangle', style='filled', fillcolor='lightgrey')
    dot.node('ChainsClient', 'ChainsClient', shape='rectangle')
    dot.node('EntriesClient', 'EntriesClient', shape='rectangle')
    dot.node('IdentitiesClient', 'IdentitiesClient', shape='rectangle')
    dot.node('ApiInfoClient', 'ApiInfoClient', shape='rectangle')
    dot.node('ReceiptsClient', 'ReceiptsClient', shape='rectangle')
    dot.node('AnchorsClient', 'AnchorsClient', shape='rectangle')
    dot.node('Utils', 'Utils', shape='rectangle', style='filled', fillcolor='lightyellow')
    dot.node('KeyCommon', 'KeyCommon', shape='rectangle', style='filled', fillcolor='lightyellow')
    dot.node('ValidateSignatureUtil', 'ValidateSignatureUtil', shape='rectangle', style='filled', fillcolor='lightyellow')
    dot.node('CommonUtil', 'CommonUtil', shape='rectangle', style='filled', fillcolor='lightyellow')
    dot.node('RequestHandler', 'request_handler.py', shape='rectangle', style='filled', fillcolor='lightgreen')
    dot.node('SampleApp', 'simulate_notary.py', shape='rectangle', style='filled', fillcolor='lightpink')
    
    # Define edges
    dot.edge('FactomSDK', 'Client', label='manages')
    dot.edge('Client', 'ChainsClient', label='facilitates')
    dot.edge('Client', 'EntriesClient', label='facilitates')
    dot.edge('Client', 'IdentitiesClient', label='facilitates')
    dot.edge('Client', 'ApiInfoClient', label='facilitates')
    dot.edge('Client', 'ReceiptsClient', label='facilitates')
    dot.edge('Client', 'AnchorsClient', label='facilitates')
    dot.edge('Client', 'RequestHandler', label='communicates')
    dot.edge('FactomSDK', 'Utils', label='uses')
    dot.edge('FactomSDK', 'KeyCommon', label='uses')
    dot.edge('FactomSDK', 'ValidateSignatureUtil', label='uses')
    dot.edge('FactomSDK', 'CommonUtil', label='uses')
    dot.edge('FactomSDK', 'SampleApp', label='demonstrates')

    # Render the diagram
    dot.render('factom_sdk_diagram', format='png', cleanup=True)

generate_factom_sdk_diagram()