from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='MLAB Architecture', format='png')

# Dashboard Component
dot.node('Dashboard', 'Dashboard (Flask)', shape='rectangle')
dot.node('Core', 'Dashboard Core', shape='rectangle')
dot.node('DAL', 'Data Access Layer', shape='rectangle')
dot.node('Interactors', 'Interactors', shape='rectangle')
dot.node('Monitoring', 'Real-time Monitoring', shape='rectangle')
dot.node('API', 'API Endpoints', shape='rectangle')
dot.node('Config', 'Configuration', shape='rectangle')
dot.node('Frontend', 'Frontend', shape='rectangle')
dot.node('ModelPub', 'Model Publication Control', shape='rectangle')

# Worker Service Component
dot.node('WorkerService', 'Worker Service', shape='rectangle')
dot.node('ModelLoading', 'Model Loading and Management', shape='rectangle')
dot.node('ZKIntegration', 'ZooKeeper Integration', shape='rectangle')
dot.node('ErrorHandling', 'Error Handling and Alerting', shape='rectangle')
dot.node('Logging', 'Logging', shape='rectangle')
dot.node('HTTPAPI', 'HTTP API', shape='rectangle')
dot.node('WorkerConfig', 'Configuration', shape='rectangle')

# External Services
dot.node('ZooKeeper', 'ZooKeeper', shape='ellipse')
dot.node('MongoDB', 'MongoDB', shape='ellipse')
dot.node('Docker', 'Docker', shape='ellipse')

# Relationships and Communication
dot.edges([
    ('Dashboard', 'Core'),
    ('Dashboard', 'DAL'),
    ('Dashboard', 'Interactors'),
    ('Dashboard', 'Monitoring'),
    ('Dashboard', 'API'),
    ('Dashboard', 'Config'),
    ('Dashboard', 'Frontend'),
    ('Dashboard', 'ModelPub'),
    ('WorkerService', 'ModelLoading'),
    ('WorkerService', 'ZKIntegration'),
    ('WorkerService', 'ErrorHandling'),
    ('WorkerService', 'Logging'),
    ('WorkerService', 'HTTPAPI'),
    ('WorkerService', 'WorkerConfig'),
    ('Core', 'ZooKeeper'),
    ('DAL', 'MongoDB'),
    ('Interactors', 'ZooKeeper'),
    ('Monitoring', 'ZooKeeper'),
    ('API', 'MongoDB'),
    ('ModelPub', 'MongoDB'),
    ('ModelLoading', 'MongoDB'),
    ('ZKIntegration', 'ZooKeeper'),
    ('ErrorHandling', 'MongoDB'),
    ('Logging', 'MongoDB'),
    ('HTTPAPI', 'MongoDB'),
    ('WorkerConfig', 'ZooKeeper'),
    ('ZooKeeper', 'Docker'),
    ('MongoDB', 'Docker')
])

# Render the graph to a file
dot.render('mlab_architecture')