import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='CTFLOW Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded', fontname='Arial')

# Add main components
dot.node('vscode', 'VS Code Extension\n(extension.ts)')
dot.node('webview', 'React Webview UI\n(dnd-ui)')
dot.node('compiler', 'Test Compiler')
dot.node('cypress', 'Cypress Engine')
dot.node('storage', 'Storage\n(.ctflow files)')
dot.node('firebase', 'Firebase\n(Real-time Collab)')

# Add subcomponents
with dot.subgraph(name='cluster_ui') as ui:
    ui.attr(label='Webview UI Components')
    ui.node('flow', 'Flow Editor')
    ui.node('nodes', 'Node Components')
    ui.node('panels', 'Control Panels')

# Add connections
dot.edge('vscode', 'webview', 'VS Code API')
dot.edge('webview', 'flow', 'Renders')
dot.edge('flow', 'nodes', 'Contains')
dot.edge('flow', 'panels', 'Contains')
dot.edge('webview', 'compiler', 'Generates Code')
dot.edge('compiler', 'cypress', 'Executes Tests')
dot.edge('webview', 'storage', 'Saves/Loads')
dot.edge('webview', 'firebase', 'Sync (Optional)')

# Print the source code
print(dot.source)

# Render the diagram
dot.render('ctflow_architecture', format='png', cleanup=True)