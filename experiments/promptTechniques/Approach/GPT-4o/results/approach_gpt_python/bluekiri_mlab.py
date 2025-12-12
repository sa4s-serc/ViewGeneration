from graphviz import Digraph

def create_mlab_architecture_diagram():
    dot = Digraph(comment='MLAB Architecture')

    # Dashboard Components
    dot.node('Dashboard', 'Flask Dashboard', shape='box', style='filled', color='lightblue')
    dot.node('Repositories', 'Data Access Layer (Repositories)', shape='box')
    dot.node('Interactors', 'Interactors (Use Cases)', shape='box')
    dot.node('API', 'API Endpoints', shape='box')
    dot.node('Frontend', 'Frontend (HTML/CSS/JS)', shape='box')

    # Worker Service Components
    dot.node('Worker', 'Worker Service', shape='box', style='filled', color='lightgreen')
    dot.node('ModelRepo', 'Model Repository', shape='box')
    dot.node('WorkerRepo', 'Worker Repository', shape='box')
    dot.node('Zookeeper', 'ZooKeeper', shape='ellipse', style='filled', color='lightgrey')
    dot.node('MongoDB', 'MongoDB', shape='cylinder', style='filled', color='lightgrey')

    # Communication and Interaction
    dot.edge('Dashboard', 'Repositories', label='Data Access')
    dot.edge('Dashboard', 'Interactors', label='Use Cases')
    dot.edge('Dashboard', 'API', label='Expose Endpoints')
    dot.edge('Dashboard', 'Frontend', label='UI Interaction')
    dot.edge('Worker', 'ModelRepo', label='Model Management')
    dot.edge('Worker', 'WorkerRepo', label='ZooKeeper Integration')
    dot.edge('Zookeeper', 'Worker', label='Model Events')
    dot.edge('MongoDB', 'ModelRepo', label='Model Data')
    dot.edge('MongoDB', 'Dashboard', label='Logs/Messages')

    # Styles and Patterns
    dot.attr(rankdir='LR', size='8,5')
    dot.attr('node', shape='box', style='rounded')

    return dot

if __name__ == "__main__":
    diagram = create_mlab_architecture_diagram()
    diagram.render('mlab_architecture', format='png', cleanup=True)