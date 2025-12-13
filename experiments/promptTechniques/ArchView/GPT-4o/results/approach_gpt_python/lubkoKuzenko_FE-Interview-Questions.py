from graphviz import Digraph

def generate_architecture_diagram():
    dot = Digraph(comment='Architecture Diagram', format='png')

    # Define nodes for different components
    dot.node('A', 'Interview Question Database', shape='rectangle', style='filled', fillcolor='lightblue')
    dot.node('B', 'Detailed Answers', shape='rectangle', style='filled', fillcolor='lightgreen')
    dot.node('C', 'Code Snippets', shape='rectangle', style='filled', fillcolor='lightyellow')
    dot.node('D', 'Topic Coverage', shape='rectangle', style='filled', fillcolor='lightpink')
    dot.node('E', 'External Resources', shape='rectangle', style='filled', fillcolor='lightgrey')

    # Define edges for dependencies/interactions
    dot.edge('A', 'B', label='provides')
    dot.edge('B', 'C', label='demonstrates')
    dot.edge('A', 'D', label='categorized by')
    dot.edge('D', 'C', label='includes examples of')
    dot.edge('B', 'E', label='links to')

    # Render the diagram to a file
    dot.render('architecture_diagram')

# Generate and visualize the architecture diagram
generate_architecture_diagram()