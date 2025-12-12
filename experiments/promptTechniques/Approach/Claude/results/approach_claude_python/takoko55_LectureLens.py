from graphviz import Digraph

def create_architecture_diagram():
    dot = Digraph('LectureLens Architecture')
    dot.attr(rankdir='TB', splines='ortho')
    
    # Global node styling
    dot.attr('node', shape='rectangle', style='rounded', fontname='Arial')
    dot.attr('edge', fontname='Arial', fontsize='10')
    
    # Create clusters/subgraphs
    with dot.subgraph(name='cluster_frontend') as frontend:
        frontend.attr(label='Frontend (React)', style='rounded', color='lightblue')
        
        # Frontend components
        frontend.node('app', 'App.jsx\n(Main Router)')
        frontend.node('search', 'SyllabusSearch.jsx\n(Search Interface)')
        frontend.node('lecture', 'LecturePage.jsx\n(Lecture Details)')
        frontend.node('review', 'ReviewPost.jsx\n(Review Management)')
        frontend.node('auth', 'Auth.jsx\n(Authentication)')
        frontend.node('store', 'Zustand Store\n(State Management)')
        
        # Frontend connections
        frontend.edge('app', 'search')
        frontend.edge('app', 'lecture')
        frontend.edge('app', 'review')
        frontend.edge('app', 'auth')
        frontend.edge('store', 'review')
    
    with dot.subgraph(name='cluster_backend') as backend:
        backend.attr(label='Backend (Go/Echo)', style='rounded', color='lightgreen')
        
        # Backend components
        backend.node('router', 'Router\n(API Routes)')
        backend.node('controller', 'Controllers\n(Request Handling)')
        backend.node('usecase', 'Usecases\n(Business Logic)')
        backend.node('repository', 'Repositories\n(Data Access)')
    
        # Backend connections
        backend.edge('router', 'controller')
        backend.edge('controller', 'usecase')
        backend.edge('usecase', 'repository')
    
    # Database
    dot.node('db', 'PostgreSQL\n(Database)', shape='cylinder', color='orange')
    
    # Cross-component connections
    dot.edge('auth', 'router', 'JWT Authentication', dir='both')
    dot.edge('search', 'router', 'REST API Calls', dir='both')
    dot.edge('lecture', 'router', 'REST API Calls', dir='both')
    dot.edge('review', 'router', 'REST API Calls', dir='both')
    dot.edge('repository', 'db', 'GORM\n(ORM Layer)')
    
    # Save the diagram
    dot.render('lecturelens_architecture', format='png', cleanup=True)

if __name__ == "__main__":
    create_architecture_diagram()