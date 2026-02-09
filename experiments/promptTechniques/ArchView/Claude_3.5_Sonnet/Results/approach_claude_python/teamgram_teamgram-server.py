from graphviz import Digraph

def create_teamgram_architecture():
    dot = Digraph('teamgram_architecture')
    dot.attr(rankdir='TB')
    dot.attr('node', shape='box', style='filled', fillcolor='lightgray')
    dot.attr('edge', arrowhead='vee')

    # Client Layer
    with dot.subgraph(name='cluster_client') as client:
        client.attr(label='Client Layer', style='rounded')
        client.node('bff', 'Backend for Frontend (BFF)\nMessages, Privacy Settings', shape='component')

    # Core Services Layer
    with dot.subgraph(name='cluster_services') as services:
        services.attr(label='Core Services Layer', style='rounded')
        services.node('msg', 'Message Service\nSend, Edit, Delete')
        services.node('chat', 'Chat Service\nManage Chats, Members')
        services.node('user', 'User Service\nProfiles, Settings')
        services.node('auth', 'Auth Service\nKeys, Sessions')
        services.node('media', 'Media Service\nFiles, Processing')
        services.node('username', 'Username Service\nManagement')
        services.node('dialog', 'Dialog Service\nLists, States')
        services.node('updates', 'Updates Service\nDelivery')
        services.node('idgen', 'ID Generator\nUnique IDs')

    # Data Layer
    with dot.subgraph(name='cluster_data') as data:
        data.attr(label='Data Layer', style='rounded')
        data.node('mysql', 'MySQL\nPersistent Storage')
        data.node('redis', 'Redis\nCaching')
        data.node('kafka', 'Kafka\nAsync Events')
        data.node('minio', 'MinIO\nObject Storage')
        data.node('etcd', 'Etcd\nService Discovery')

    # Add connections between layers
    # BFF to Services
    services_list = ['msg', 'chat', 'user', 'auth', 'media', 'username', 'dialog', 'updates']
    for service in services_list:
        dot.edge('bff', service, 'gRPC')

    # Services to Data stores
    dot.edge('msg', 'mysql', 'persist')
    dot.edge('chat', 'mysql', 'persist')
    dot.edge('user', 'mysql', 'persist')
    dot.edge('username', 'mysql', 'persist')
    dot.edge('dialog', 'mysql', 'persist')

    dot.edge('user', 'redis', 'cache')
    dot.edge('auth', 'redis', 'cache')
    dot.edge('updates', 'kafka', 'events')
    dot.edge('media', 'minio', 'store')

    # Service Discovery
    for service in services_list + ['idgen']:
        dot.edge(service, 'etcd', 'register')

    dot.render('teamgram_architecture', view=True, format='png')

if __name__ == "__main__":
    create_teamgram_architecture()