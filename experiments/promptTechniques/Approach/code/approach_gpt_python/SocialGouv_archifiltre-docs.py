from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='SocialGouv_archifiltre-docs Architecture')

# Define nodes with labels
dot.node('A', 'File System Loading and Processing')
dot.node('B', 'Data Export')
dot.node('C', 'Metadata Management')
dot.node('D', 'Asynchronous Processing')
dot.node('E', 'State Management')
dot.node('F', 'Tracking and Monitoring')
dot.node('G', 'User Configuration')
dot.node('H', 'Internationalization (i18n)')
dot.node('I', 'Automated Updates')
dot.node('J', 'Font Management')
dot.node('K', 'File Deletion Scripts')
dot.node('L', 'CI/CD')
dot.node('M', 'Translation Utilities')
dot.node('N', 'React Devtools')
dot.node('O', 'App Notarization')
dot.node('P', 'Installer Customization')

# Define edges between nodes
dot.edge('A', 'B', label='Structured Data Export')
dot.edge('A', 'C', label='Metadata Extraction')
dot.edge('A', 'D', label='Async Processing')
dot.edge('E', 'A', label='State Management')
dot.edge('F', 'A', label='Error Logging')
dot.edge('G', 'A', label='User Settings')
dot.edge('H', 'A', label='Language Support')
dot.edge('I', 'A', label='Automated Updates')
dot.edge('J', 'A', label='Font Handling')
dot.edge('K', 'A', label='Script Generation')
dot.edge('L', 'A', label='Continuous Integration')
dot.edge('M', 'H', label='Translation Scripts')
dot.edge('N', 'A', label='Debugging Tools')
dot.edge('O', 'A', label='Security Notarization')
dot.edge('P', 'A', label='Installer Scripts')

# Set graph attributes
dot.attr(rankdir='LR', size='10,10')
dot.attr('node', shape='rectangle', style='filled', color='lightblue')
dot.attr('edge', style='dashed')

# Generate and render the diagram
dot.render('socialgouv_archifiltre_docs_architecture', format='png', cleanup=True)