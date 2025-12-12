import graphviz

dot = graphviz.Digraph('OfflinePackageWebpackPlugin', comment='Architectural View of OfflinePackageWebpackPlugin')
dot.attr(rankdir='TB')

# Main components
dot.node('webpack', 'Webpack', shape='ellipse', style='filled', fillcolor='lightblue')
dot.node('plugin', 'OfflinePackagePlugin\n(plugin.js)', shape='box', style='filled', fillcolor='lightgreen')
dot.node('index', 'Entry Point\n(index.js)', shape='box', style='filled', fillcolor='lightyellow')
dot.node('zip', 'Zip Archive', shape='folder', style='filled', fillcolor='lightcoral')
dot.node('manifest', 'JSON Manifest\n(index.json)', shape='note', style='filled', fillcolor='lightpink')

# Dependencies
dot.node('jszip', 'JSZip', shape='component', style='filled', fillcolor='wheat')
dot.node('lodash', 'Lodash', shape='component', style='filled', fillcolor='wheat')
dot.node('mime', 'mime-types', shape='component', style='filled', fillcolor='wheat')

# Configuration and test
dot.node('config', 'Configuration\nOptions', shape='parallelogram', style='filled', fillcolor='lightgrey')
dot.node('test', 'Test Project\n(vue-project)', shape='box3d', style='filled', fillcolor='lightsteelblue')

# Edges for main flow
dot.edge('webpack', 'plugin', label='hooks into emit phase')
dot.edge('plugin', 'zip', label='creates')
dot.edge('plugin', 'manifest', label='generates')
dot.edge('index', 'plugin', label='requires')

# Dependencies edges
dot.edge('plugin', 'jszip', label='uses', style='dashed')
dot.edge('plugin', 'lodash', label='uses', style='dashed')
dot.edge('plugin', 'mime', label='uses', style='dashed')

# Configuration and test edges
dot.edge('config', 'plugin', label='configures', style='dotted')
dot.edge('test', 'plugin', label='tests', style='dotted')

dot.render(format='png', cleanup=True)