import graphviz

# Create a new directed graph
dot = graphviz.Digraph('CodeX Architecture', comment='CodeX System Architecture')
dot.attr(rankdir='TB')

# Define node attributes
dot.attr('node', shape='rectangle', style='rounded', fontname='Arial')
dot.attr('edge', fontname='Arial')

# Frontend Components
with dot.subgraph(name='cluster_frontend') as frontend:
    frontend.attr(label='Frontend (ReactJS)', style='rounded', color='lightblue')
    frontend.node('app', 'App.js\n(Main Component)')
    frontend.node('navbar', 'Navbar.js\n(Navigation + Code Sharing)')
    frontend.node('pseudo', 'PseudoCode.js\n(Display & Translation)')
    frontend.node('warnings', 'Warnings.js\n(Code Analysis)')
    frontend.node('compile', 'Compile.js\n(Code Execution)')
    
    # Frontend component relationships
    frontend.edge('app', 'navbar')
    frontend.edge('app', 'pseudo')
    frontend.edge('app', 'warnings')
    frontend.edge('app', 'compile')

# Backend Components
with dot.subgraph(name='cluster_backend') as backend:
    backend.attr(label='Backend (FastAPI)', style='rounded', color='lightgreen')
    backend.node('main', 'main.py\n(Entry Point)')
    backend.node('app_gateway', 'app.py\n(API Gateway)')
    backend.node('routes', 'Routes\n(API Endpoints)')
    backend.node('services', 'Services\n(Business Logic)')
    
    # Backend component relationships
    backend.edge('main', 'app_gateway')
    backend.edge('app_gateway', 'routes')
    backend.edge('routes', 'services')

# External Services
with dot.subgraph(name='cluster_external') as external:
    external.attr(label='External Services', style='rounded', color='lightpink')
    external.node('hackerearth', 'HackerEarth API\n(Code Compilation)')
    external.node('translate', 'Google Translate\n(Translation)')
    external.node('db', 'SQLite\n(Code Storage)')

# Cross-component relationships
dot.edge('pseudo', 'routes', 'HTTP/REST')
dot.edge('warnings', 'routes', 'HTTP/REST')
dot.edge('compile', 'routes', 'HTTP/REST')
dot.edge('services', 'hackerearth', 'API Calls')
dot.edge('services', 'translate', 'API Calls')
dot.edge('services', 'db', 'CRUD Operations')

# Render the graph
dot.render('codex_architecture', format='png', cleanup=True)