from graphviz import Digraph

def generate_solenya_architecture_diagram():
    dot = Digraph(comment='Solenya Framework Architecture', format='png')
    
    # Core Components
    dot.node('App', 'App', shape='box', style='filled', fillcolor='lightblue')
    dot.node('Component', 'Component', shape='box')
    dot.node('Router', 'Router', shape='box')
    dot.node('Validator', 'Validator', shape='box')
    dot.node('Storage', 'Storage', shape='box')
    dot.node('TimeTravel', 'TimeTravel', shape='box')
    
    # Helper Functions
    dot.node('HTML Helpers', 'HTML Helper Functions', shape='ellipse', style='filled', fillcolor='lightgrey')
    dot.node('Widget Functions', 'Widget Functions', shape='ellipse', style='filled', fillcolor='lightgrey')
    
    # Files
    dot.node('index.ts', 'index.ts', shape='note')
    dot.node('component.ts', 'component.ts', shape='note')
    dot.node('app.ts', 'app.ts', shape='note')
    dot.node('router.ts', 'router.ts', shape='note')
    dot.node('validation.ts', 'validation.ts', shape='note')
    dot.node('dom.ts', 'dom.ts', shape='note')
    dot.node('storage.ts', 'storage.ts', shape='note')
    dot.node('timeTravel.ts', 'timeTravel.ts', shape='note')
    dot.node('lifecycle.ts', 'lifecycle.ts', shape='note')
    dot.node('widgets.ts', 'widgets.ts', shape='note')
    dot.node('html.ts', 'html.ts', shape='note')
    dot.node('util.ts', 'util.ts', shape='note')

    # Relationships
    dot.edge('App', 'Component')
    dot.edge('App', 'Router')
    dot.edge('App', 'Validator')
    dot.edge('App', 'Storage')
    dot.edge('App', 'TimeTravel')
    dot.edge('Component', 'HTML Helpers', style='dashed')
    dot.edge('Component', 'Widget Functions', style='dashed')
    
    # Files to Components
    dot.edge('index.ts', 'App')
    dot.edge('component.ts', 'Component')
    dot.edge('app.ts', 'App')
    dot.edge('router.ts', 'Router')
    dot.edge('validation.ts', 'Validator')
    dot.edge('dom.ts', 'Component')
    dot.edge('storage.ts', 'Storage')
    dot.edge('timeTravel.ts', 'TimeTravel')
    
    # Style
    dot.attr('node', shape='box', style='rounded')
    
    dot.render('solenya_architecture_diagram', view=True)

generate_solenya_architecture_diagram()