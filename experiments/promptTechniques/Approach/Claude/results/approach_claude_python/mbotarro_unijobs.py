from graphviz import Digraph

def create_unijobs_architecture():
    dot = Digraph('UniJobs_Architecture')
    dot.attr(rankdir='TB')

    # Global node styling
    dot.attr('node', shape='rectangle', style='filled,rounded', fontname='Arial')
    dot.attr('edge', fontname='Arial', fontsize='10')

    # Frontend Layer
    with dot.subgraph(name='cluster_0') as frontend:
        frontend.attr(label='Frontend (React Native)', style='rounded', color='lightblue', bgcolor='aliceblue')
        
        frontend.node('auth', 'Authentication\nLogin/Register', fillcolor='lightblue')
        frontend.node('feed', 'Offer/Request Feed\nFiltering & Search', fillcolor='lightblue')
        frontend.node('profile', 'User Profiles\nSettings', fillcolor='lightblue')
        frontend.node('creation', 'Offer/Request\nCreation Forms', fillcolor='lightblue')
        frontend.node('navigation', 'Navigation\nSide Drawer', fillcolor='lightblue')

    # Backend Layer
    with dot.subgraph(name='cluster_1') as backend:
        backend.attr(label='Backend (Go)', style='rounded', color='lightgreen', bgcolor='mintcream')
        
        backend.node('rest_api', 'RESTful API', fillcolor='palegreen')
        backend.node('handlers', 'HTTP Handlers', fillcolor='palegreen')
        backend.node('usecases', 'Business Logic\nUse Cases', fillcolor='palegreen')
        backend.node('dal', 'Data Access Layer', fillcolor='palegreen')

    # Storage Layer
    with dot.subgraph(name='cluster_2') as storage:
        storage.attr(label='Storage Layer', style='rounded', color='lightgray', bgcolor='whitesmoke')
        
        storage.node('postgres', 'PostgreSQL\nUser & Core Data', fillcolor='lightgray')
        storage.node('elastic', 'Elasticsearch\nSearch Engine', fillcolor='lightgray')

    # Frontend internal connections
    dot.edge('navigation', 'feed')
    dot.edge('navigation', 'profile')
    dot.edge('navigation', 'creation')
    dot.edge('auth', 'feed')
    dot.edge('feed', 'creation')

    # Backend internal connections
    dot.edge('rest_api', 'handlers')
    dot.edge('handlers', 'usecases')
    dot.edge('usecases', 'dal')

    # Cross-layer connections
    dot.edge('auth', 'rest_api', 'Authentication requests')
    dot.edge('feed', 'rest_api', 'Fetch offers/requests')
    dot.edge('profile', 'rest_api', 'Profile operations')
    dot.edge('creation', 'rest_api', 'Create new items')
    dot.edge('dal', 'postgres', 'CRUD operations')
    dot.edge('dal', 'elastic', 'Search queries')

    return dot

# Generate and save the diagram
architecture = create_unijobs_architecture()
architecture.render('unijobs_architecture', format='png', cleanup=True)