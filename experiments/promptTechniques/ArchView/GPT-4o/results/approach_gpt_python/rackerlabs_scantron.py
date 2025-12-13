from graphviz import Digraph

def generate_scantron_architecture_diagram():
    dot = Digraph(comment='Scantron Project Architecture')

    # Components
    dot.node('Console', 'Console (Web Front-End)', shape='rectangle', style='filled', fillcolor='lightblue')
    dot.node('Engines', 'Engines (Scanning Nodes)', shape='rectangle', style='filled', fillcolor='lightgreen')
    dot.node('REST API', 'REST API', shape='rectangle', style='filled', fillcolor='lightyellow')
    dot.node('NFS', 'NFS (Shared Storage)', shape='rectangle', style='filled', fillcolor='lightgrey')
    dot.node('Scheduler', 'Scan Scheduler', shape='rectangle', style='filled', fillcolor='lightcoral')
    dot.node('Results', 'Scan Results Processing', shape='rectangle', style='filled', fillcolor='lightpink')
    dot.node('Email Alerts', 'Email Alerts', shape='rectangle', style='filled', fillcolor='lightgoldenrodyellow')
    dot.node('Ansible', 'Ansible Automation', shape='rectangle', style='filled', fillcolor='lightcyan')

    # Connectors
    dot.edge('Console', 'REST API', label='Communicates via')
    dot.edge('REST API', 'Engines', label='Polls for jobs')
    dot.edge('Engines', 'NFS', label='Stores results on')
    dot.edge('NFS', 'Results', label='Accesses results from')
    dot.edge('Scheduler', 'Console', label='Schedules scans using django-recurrence')
    dot.edge('Results', 'Console', label='Processes results into CSV')
    dot.edge('Scheduler', 'Engines', label='Distributes tasks')
    dot.edge('Console', 'Email Alerts', label='Sends alerts upon completion/errors')
    dot.edge('Ansible', 'Console', label='Deploys using playbooks')
    dot.edge('Ansible', 'Engines', label='Deploys using playbooks')

    # Additional annotations for non-functional requirements
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('REST API', style='dashed', label='REST API\n(Scalability & Fault Tolerance)')

    # Render the diagram
    dot.render('scantron_architecture_diagram', format='png', cleanup=True)

generate_scantron_architecture_diagram()