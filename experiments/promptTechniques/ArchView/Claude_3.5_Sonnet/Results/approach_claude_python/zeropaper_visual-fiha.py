import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='Visual Fiha Architecture')
dot.attr(rankdir='TB')

# Add nodes
dot.node('vf_extension', 'VFExtension\n(Core Orchestrator)', shape='rectangle')
dot.node('webserver', 'WebServer', shape='rectangle')
dot.node('display_worker', 'DisplayWorker', shape='rectangle')
dot.node('redux_store', 'Redux Store', shape='cylinder')
dot.node('script_runner', 'ScriptRunner', shape='rectangle')
dot.node('scriptable', 'Scriptable', shape='rectangle')
dot.node('com', 'Com\n(Message Passing)', shape='rectangle')
dot.node('layers', 'Layers\n(Canvas2D/ThreeJS)', shape='rectangle')
dot.node('webviews', 'Webviews\n(UI Panels)', shape='rectangle')
dot.node('commands', 'Commands', shape='rectangle')
dot.node('capture', 'Capture\n(Audio/MIDI)', shape='rectangle')

# Add edges with labels
dot.edge('vf_extension', 'webserver', 'manages')
dot.edge('vf_extension', 'redux_store', 'updates')
dot.edge('vf_extension', 'webviews', 'controls')
dot.edge('webserver', 'display_worker', 'serves')
dot.edge('display_worker', 'layers', 'renders')
dot.edge('display_worker', 'script_runner', 'executes')
dot.edge('script_runner', 'scriptable', 'manages')
dot.edge('com', 'vf_extension', 'messages')
dot.edge('com', 'webviews', 'messages')
dot.edge('com', 'display_worker', 'messages')
dot.edge('redux_store', 'webviews', 'state')
dot.edge('redux_store', 'display_worker', 'state')
dot.edge('capture', 'com', 'input')
dot.edge('commands', 'vf_extension', 'executes')

# Set graph attributes
dot.attr(label='Visual Fiha Architecture\nMulti-Process Live-Coding VJ Environment')
dot.attr(fontsize='16')

# Save the diagram
dot.render('visual_fiha_architecture', format='png', cleanup=True)