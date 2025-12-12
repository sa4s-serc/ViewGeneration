import graphviz

dot = graphviz.Digraph(comment='Factom Harmony Connect API Python SDK Architecture')
dot.attr(rankdir='TB', size='8,10')

with dot.subgraph(name='cluster_sdk') as sdk:
    sdk.attr(label='Factom Harmony Connect Python SDK', style='filled', color='lightgrey')
    
    with sdk.subgraph(name='cluster_core') as core:
        core.attr(label='Core Components', style='filled', color='lightblue')
        core.node('factom_client', 'FactomClient\n(Facade Pattern)', shape='rectangle')
        core.node('chains_client', 'ChainsClient', shape='rectangle')
        core.node('entries_client', 'EntriesClient', shape='rectangle')
        core.node('identities_client', 'IdentitiesClient', shape='rectangle')
        core.node('api_info_client', 'ApiInfoClient', shape='rectangle')
        core.node('receipts_client', 'ReceiptsClient', shape='rectangle')
        core.node('anchors_client', 'AnchorsClient', shape='rectangle')
    
    with sdk.subgraph(name='cluster_utils') as utils:
        utils.attr(label='Utilities', style='filled', color='lightgreen')
        utils.node('utils', 'Utils\n(Key Generation)', shape='rectangle')
        utils.node('key_common', 'KeyCommon\n(Crypto Management)', shape='rectangle')
        utils.node('validate_sig', 'ValidateSignatureUtil\n(Strategy Pattern)', shape='rectangle')
        utils.node('common_util', 'CommonUtil\n(Base64 Encoding)', shape='rectangle')
    
    sdk.node('request_handler', 'Request Handler\n(HTTP Communication)', shape='rectangle')

dot.node('sample_app', 'Sample Application\n(simulate_notary.py)', shape='ellipse')
dot.node('factom_api', 'Factom Harmony\nConnect API', shape='cylinder', color='orange')

dot.edge('factom_client', 'chains_client', style='dashed')
dot.edge('factom_client', 'entries_client', style='dashed')
dot.edge('factom_client', 'identities_client', style='dashed')
dot.edge('factom_client', 'api_info_client', style='dashed')
dot.edge('factom_client', 'receipts_client', style='dashed')
dot.edge('factom_client', 'anchors_client', style='dashed')

dot.edge('chains_client', 'validate_sig', style='dotted', label='uses')
dot.edge('entries_client', 'validate_sig', style='dotted', label='uses')
dot.edge('chains_client', 'common_util', style='dotted', label='uses')
dot.edge('entries_client', 'common_util', style='dotted', label='uses')

dot.edge('request_handler', 'factom_api', label='HTTP/REST', color='blue')
dot.edge('factom_client', 'request_handler', label='delegates to')
dot.edge('sample_app', 'factom_client', label='uses', color='green')

dot.render('factom_sdk_architecture', format='png', cleanup=True)