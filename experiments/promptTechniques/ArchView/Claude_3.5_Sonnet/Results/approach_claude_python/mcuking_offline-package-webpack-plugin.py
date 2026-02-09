import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='Offline Package Webpack Plugin Architecture')
dot.attr(rankdir='TB')
dot.attr('node', shape='box', style='rounded')

# Add nodes with styling
dot.node('webpack', 'Webpack Build Process', fillcolor='lightblue', style='filled,rounded')
dot.node('plugin', 'OfflinePackagePlugin', fillcolor='lightgreen', style='filled,rounded')
dot.node('jszip', 'JSZip Library', fillcolor='lightyellow', style='filled,rounded')
dot.node('mime', 'MIME-Types Library', fillcolor='lightyellow', style='filled,rounded')
dot.node('output', 'Output\n- Zip Archive\n- index.json', fillcolor='lightpink', style='filled,rounded')
dot.node('config', 'Configuration\n- fileTypes\n- excludeFileName', fillcolor='lightgrey', style='filled,rounded')

# Add edges with labels and styling
dot.edge('webpack', 'plugin', 'emit hook', fontsize='10')
dot.edge('config', 'plugin', 'configure', fontsize='10')
dot.edge('plugin', 'jszip', 'create archive', fontsize='10')
dot.edge('plugin', 'mime', 'detect types', fontsize='10')
dot.edge('jszip', 'output', 'generate zip', fontsize='10')
dot.edge('mime', 'output', 'create manifest', fontsize='10')

# Set graph attributes
dot.attr(label='Offline Package Webpack Plugin Architecture\n', labelloc='t', fontsize='16')
dot.attr(rankdir='TB')
dot.attr(splines='ortho')

# Render the graph
dot.render('offline_package_webpack_architecture', format='png', cleanup=True)