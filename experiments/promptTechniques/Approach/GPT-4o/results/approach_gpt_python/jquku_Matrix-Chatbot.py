from graphviz import Digraph

def generate_diagram():
    dot = Digraph(comment='Matrix Chatbot Architecture')

    # Define nodes for main components
    dot.node('A', 'Chatbot Core', shape='rectangle', style='filled', color='lightblue')
    dot.node('B', 'NLP', shape='rectangle', style='filled', color='lightgreen')
    dot.node('C', 'Knowledge Base', shape='cylinder', style='filled', color='lightgrey')
    dot.node('D', 'Database Interaction', shape='rectangle', style='filled', color='lightcoral')
    dot.node('E', 'Configuration', shape='rectangle', style='filled', color='lightyellow')
    dot.node('F', 'Matrix Homeserver', shape='ellipse', style='filled', color='lightpink')

    # Define submodules
    dot.node('G', 'Message Evaluation', shape='rectangle', style='dotted')
    dot.node('H', 'Response Management', shape='rectangle', style='dotted')
    dot.node('I', 'Index Evaluation', shape='rectangle', style='dotted')
    dot.node('J', 'Small Talk Evaluation', shape='rectangle', style='dotted')
    dot.node('K', 'Organisation Evaluation', shape='rectangle', style='dotted')

    # Define edges between components
    dot.edge('A', 'F', label='communicates via matrix-nio', dir='both')
    dot.edge('A', 'B', label='processes messages')
    dot.edge('B', 'C', label='queries for knowledge')
    dot.edge('C', 'D', label='stores and retrieves data')
    dot.edge('E', 'A', label='provides configuration')

    # Define edges for submodules
    dot.edge('G', 'A', label='evaluates messages')
    dot.edge('H', 'A', label='manages responses')
    dot.edge('I', 'C', label='scrapes and updates')
    dot.edge('J', 'C', label='adds small talk')
    dot.edge('K', 'C', label='parses and stores')

    # Render the diagram
    dot.render('matrix_chatbot_architecture', format='png', cleanup=True)

generate_diagram()