from graphviz import Digraph

dot = Digraph(comment='Visual Fiha Architecture', format='png')

# Define nodes
dot.node('VFExtension', 'VFExtension\n(src/extension/VFExtension.ts)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('WebServer', 'WebServer\n(src/extension/WebServer.ts)', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('DisplayWorker', 'DisplayWorker\n(src/display/DisplayWorker.ts)', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('Layers', 'Layers\n(src/layers)', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('ScriptRunner', 'ScriptRunner\n(src/utils/ScriptRunner.ts)', shape='rectangle', style='filled', fillcolor='lightcyan')
dot.node('Scriptable', 'Scriptable\n(src/utils/Scriptable.ts)', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('ReduxStore', 'Redux Store\n(src/extension/store.ts,\n src/webviews/store.ts)', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('Webviews', 'Webviews\n(src/webviews)', shape='rectangle', style='filled', fillcolor='lightgoldenrod')
dot.node('Capture', 'Capture\n(src/capture)', shape='rectangle', style='filled', fillcolor='lightsteelblue')
dot.node('Com', 'Com\n(src/utils/com.ts)', shape='rectangle', style='filled', fillcolor='lightseagreen')
dot.node('Commands', 'Commands\n(src/extension/commands)', shape='rectangle', style='filled', fillcolor='lightcoral')

# Define relationships
dot.edge('VFExtension', 'WebServer', label='manages', dir='forward')
dot.edge('VFExtension', 'DisplayWorker', label='interacts with', dir='forward')
dot.edge('VFExtension', 'Layers', label='manages', dir='forward')
dot.edge('VFExtension', 'ReduxStore', label='uses', dir='forward')
dot.edge('VFExtension', 'Webviews', label='manages', dir='forward')
dot.edge('WebServer', 'Com', label='broadcasts', dir='forward')
dot.edge('DisplayWorker', 'Layers', label='renders', dir='forward')
dot.edge('Layers', 'ScriptRunner', label='uses', dir='forward')
dot.edge('Layers', 'Scriptable', label='manages', dir='forward')
dot.edge('Webviews', 'Com', label='communicates', dir='forward')
dot.edge('Capture', 'Com', label='captures', dir='forward')
dot.edge('ReduxStore', 'Com', label='centralizes', dir='forward')
dot.edge('Commands', 'VFExtension', label='exposes', dir='forward')

# Render the diagram
dot.render('visual_fiha_architecture')