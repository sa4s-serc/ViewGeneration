from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='CodeX Web Application Architecture', format='png')

# Define styles
styles = {
    'graph': {
        'fontsize': '12',
        'fontname': 'Helvetica',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'rectangle',
        'style': 'filled',
        'fillcolor': '#CCCCFF',
    },
    'edges': {
        'arrowhead': 'open',
        'fontname': 'Helvetica',
        'fontsize': '10',
    }
}

def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph

# Define nodes for frontend components
dot.node('Frontend', 'Frontend (ReactJS)', fillcolor='#FFDD44')
dot.node('App', 'App.js')
dot.node('Navbar', 'Navbar.js')
dot.node('PseudoCode', 'PseudoCode.js')
dot.node('Warnings', 'Warnings.js')
dot.node('Compile', 'Compile.js')

# Define nodes for backend components
dot.node('Backend', 'Backend (FastAPI)', fillcolor='#44FFDD')
dot.node('Main', 'main.py')
dot.node('AppInstance', 'app/app.py')
dot.node('CompileRoute', 'compile.py')
dot.node('ConvertPseudoRoute', 'convertPseudo.py')
dot.node('WarningsRoute', 'warnings.py')
dot.node('TranslatePseudoRoute', 'translatePseudo.py')
dot.node('ShareCodeRoute', 'shareCode.py')
dot.node('FlowchartRoute', 'flowchart.py')

# Define nodes for services
dot.node('PylintService', 'pylint.py', fillcolor='#DDFF44')
dot.node('PseudoCodeService', 'pseudo_code.py', fillcolor='#DDFF44')
dot.node('HackerEarthService', 'hackerearth_compile.py', fillcolor='#DDFF44')
dot.node('TranslateService', 'translate.py', fillcolor='#DDFF44')
dot.node('FlowchartService', 'flowchart.py', fillcolor='#DDFF44')

# Define edges
dot.edge('Frontend', 'Backend', label='REST API Calls')
dot.edge('App', 'Navbar')
dot.edge('App', 'PseudoCode')
dot.edge('App', 'Warnings')
dot.edge('App', 'Compile')
dot.edge('Backend', 'AppInstance', label='API Gateway')
dot.edge('AppInstance', 'CompileRoute', label='Route')
dot.edge('AppInstance', 'ConvertPseudoRoute', label='Route')
dot.edge('AppInstance', 'WarningsRoute', label='Route')
dot.edge('AppInstance', 'TranslatePseudoRoute', label='Route')
dot.edge('AppInstance', 'ShareCodeRoute', label='Route')
dot.edge('AppInstance', 'FlowchartRoute', label='Route')
dot.edge('CompileRoute', 'HackerEarthService', label='API Call')
dot.edge('ConvertPseudoRoute', 'PseudoCodeService', label='Service Call')
dot.edge('WarningsRoute', 'PylintService', label='Service Call')
dot.edge('TranslatePseudoRoute', 'TranslateService', label='Service Call')
dot.edge('FlowchartRoute', 'FlowchartService', label='Service Call')

# Apply styles
dot = apply_styles(dot, styles)

# Render the diagram
dot.render('codex_architecture')