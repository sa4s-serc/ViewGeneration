from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='codahale/sneaker Architecture')

# Define nodes
dot.node('M', 'Manager (Central Component)', shape='rectangle')
dot.node('S3', 'AWS S3 Integration', shape='rectangle')
dot.node('KMS', 'AWS KMS Integration', shape='rectangle')
dot.node('E', 'Envelope (Encryption/Decryption)', shape='rectangle')
dot.node('CLI', 'Command-line Interface', shape='rectangle')
dot.node('Upload', 'Upload Function', shape='rectangle')
dot.node('Download', 'Download Function', shape='rectangle')
dot.node('List', 'List Function', shape='rectangle')
dot.node('Rm', 'Rm Function', shape='rectangle')
dot.node('Pack', 'Pack Function', shape='rectangle')
dot.node('Unpack', 'Unpack Function', shape='rectangle')
dot.node('Rotate', 'Rotate Function', shape='rectangle')

# Define edges
dot.edge('CLI', 'Upload', label='calls', dir='forward')
dot.edge('CLI', 'Download', label='calls', dir='forward')
dot.edge('CLI', 'List', label='calls', dir='forward')
dot.edge('CLI', 'Rm', label='calls', dir='forward')
dot.edge('CLI', 'Pack', label='calls', dir='forward')
dot.edge('CLI', 'Unpack', label='calls', dir='forward')
dot.edge('CLI', 'Rotate', label='calls', dir='forward')

dot.edge('Upload', 'M', label='uses', dir='forward')
dot.edge('Download', 'M', label='uses', dir='forward')
dot.edge('List', 'M', label='uses', dir='forward')
dot.edge('Rm', 'M', label='uses', dir='forward')
dot.edge('Pack', 'M', label='uses', dir='forward')
dot.edge('Unpack', 'M', label='uses', dir='forward')
dot.edge('Rotate', 'M', label='uses', dir='forward')

dot.edge('M', 'S3', label='interacts', dir='forward')
dot.edge('M', 'KMS', label='interacts', dir='forward')
dot.edge('M', 'E', label='uses', dir='forward')

# Output the diagram to a file
dot.render('sneaker_architecture', format='png', cleanup=True)