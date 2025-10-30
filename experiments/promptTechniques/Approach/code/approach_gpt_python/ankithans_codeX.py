from graphviz import Digraph

dot = Digraph(comment='CodeX Project Architecture')

# Frontend Components
dot.node('ReactJS', 'ReactJS Frontend')
dot.node('App.js', 'Main Application Component')
dot.node('Navbar.js', 'Navbar')
dot.node('PseudoCode.js', 'PseudoCode Component')
dot.node('Warnings.js', 'Warnings Component')
dot.node('Compile.js', 'Compile Component')

# Backend Components
dot.node('FastAPI', 'FastAPI Backend')
dot.node('main.py', 'Main Entry Point')
dot.node('app.py', 'API Gateway')
dot.node('compile.py', 'Compile Endpoint')
dot.node('convertPseudo.py', 'Convert to Pseudocode Endpoint')
dot.node('warnings.py', 'Warnings Endpoint')
dot.node('translatePseudo.py', 'Translate Pseudocode Endpoint')
dot.node('shareCode.py', 'Share Code Endpoint')
dot.node('flowchart.py', 'Flowchart Generation Endpoint')

# Services
dot.node('pylint.py', 'Pylint Service')
dot.node('pseudo_code.py', 'Pseudocode Conversion Service')
dot.node('hackerearth_compile.py', 'HackerEarth Compile Service')
dot.node('translate.py', 'Translation Logic Service')
dot.node('flowchart_service.py', 'Flowchart Generation Service')

# Infrastructure Files
dot.node('SQLite', 'SQLite Database')

# Connections
dot.edge('ReactJS', 'App.js')
dot.edge('App.js', 'Navbar.js')
dot.edge('App.js', 'PseudoCode.js')
dot.edge('App.js', 'Warnings.js')
dot.edge('App.js', 'Compile.js')
dot.edge('FastAPI', 'main.py')
dot.edge('main.py', 'app.py')
dot.edge('app.py', 'compile.py')
dot.edge('app.py', 'convertPseudo.py')
dot.edge('app.py', 'warnings.py')
dot.edge('app.py', 'translatePseudo.py')
dot.edge('app.py', 'shareCode.py')
dot.edge('app.py', 'flowchart.py')
dot.edge('compile.py', 'hackerearth_compile.py')
dot.edge('convertPseudo.py', 'pseudo_code.py')
dot.edge('warnings.py', 'pylint.py')
dot.edge('translatePseudo.py', 'translate.py')
dot.edge('flowchart.py', 'flowchart_service.py')
dot.edge('shareCode.py', 'SQLite')

# Render the diagram
dot.render('codex_project_architecture', format='png', cleanup=True)