import graphviz

dot = graphviz.Digraph('Factom_SDK_Architecture', 
                       comment='Factom Harmony Connect API Python SDK Architecture',
                       graph_attr={'rankdir': 'TB', 'splines': 'ortho'})

# Add client layer components
with dot.subgraph(name='cluster_clients') as clients:
    clients.attr(label='Client Layer')
    clients.node('factom_client', 'FactomClient\n(Facade)', shape='rectangle')
    clients.node('chains_client', 'ChainsClient', shape='rectangle')
    clients.node('entries_client', 'EntriesClient', shape='rectangle')
    clients.node('identities_client', 'IdentitiesClient', shape='rectangle')
    clients.node('receipts_client', 'ReceiptsClient', shape='rectangle')
    clients.node('anchors_client', 'AnchorsClient', shape='rectangle')
    clients.node('apiinfo_client', 'ApiInfoClient', shape='rectangle')

# Add utility layer components
with dot.subgraph(name='cluster_utils') as utils:
    utils.attr(label='Utilities Layer')
    utils.node('key_common', 'KeyCommon', shape='rectangle')
    utils.node('utils', 'Utils', shape='rectangle')
    utils.node('validate_sig', 'ValidateSignatureUtil', shape='rectangle')
    utils.node('common_util', 'CommonUtil', shape='rectangle')

# Add request handler layer
with dot.subgraph(name='cluster_handler') as handler:
    handler.attr(label='Request Handler Layer')
    handler.node('request_handler', 'RequestHandler', shape='rectangle')

# Add sample application
dot.node('notary_app', 'Notary Sample App', shape='rectangle', style='filled', fillcolor='lightgrey')

# Add connections
dot.edge('factom_client', 'chains_client')
dot.edge('factom_client', 'entries_client')
dot.edge('factom_client', 'identities_client')
dot.edge('factom_client', 'receipts_client')
dot.edge('factom_client', 'anchors_client')
dot.edge('factom_client', 'apiinfo_client')

dot.edge('chains_client', 'request_handler')
dot.edge('entries_client', 'request_handler')
dot.edge('identities_client', 'request_handler')
dot.edge('receipts_client', 'request_handler')
dot.edge('anchors_client', 'request_handler')
dot.edge('apiinfo_client', 'request_handler')

dot.edge('chains_client', 'validate_sig')
dot.edge('entries_client', 'validate_sig')
dot.edge('chains_client', 'common_util')
dot.edge('entries_client', 'common_util')

dot.edge('validate_sig', 'key_common')
dot.edge('validate_sig', 'utils')

dot.edge('notary_app', 'factom_client')

print(dot.source)
dot.render('factom_sdk_architecture', view=True, format='png')