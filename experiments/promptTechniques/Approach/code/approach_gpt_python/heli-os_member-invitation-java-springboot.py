from graphviz import Digraph

dot = Digraph(comment='Member Invitation System Architecture')

# Define styles
dot.attr('node', shape='rectangle', style='filled', color='lightgrey')
dot.attr('edge', arrowhead='normal')

# API Layer
dot.node('API', 'API Layer\n(RestController)', shape='rectangle', color='lightblue')
dot.node('DTO', 'Data Transfer Objects\n(*Dto.java)', shape='rectangle', color='lightblue')

# Domain Layer
dot.node('Domain', 'Domain Logic', shape='rectangle', color='lightgreen')
dot.node('Member', 'Member Domain\n(Member.java)', shape='rectangle', color='lightgreen')
dot.node('Invitation', 'Invitation Domain\n(Invitation.java)', shape='rectangle', color='lightgreen')
dot.node('UseCase', 'Use Case Interfaces\n(*UseCase.java)', shape='rectangle', color='lightgreen')
dot.node('Service', 'Domain Services\n(*Service.java)', shape='rectangle', color='lightgreen')

# Infrastructure Layer
dot.node('Infrastructure', 'Infrastructure', shape='rectangle', color='lightcoral')
dot.node('PersistenceDB', 'Persistence Database\n(H2/JPA)', shape='rectangle', color='lightcoral')
dot.node('PersistenceRedis', 'Persistence Redis\n(Redis Adapter)', shape='rectangle', color='lightcoral')

# Commons
dot.node('CommonModel', 'Common Models\n(common-model)', shape='rectangle', color='orange')
dot.node('CommonUtil', 'Common Utils\n(common-util)', shape='rectangle', color='orange')

# API Layer connections
dot.edge('API', 'DTO', label='uses', style='dashed')
dot.edge('API', 'UseCase', label='calls', style='dashed')

# Domain connections
dot.edge('UseCase', 'Service', label='uses', style='dashed')
dot.edge('Service', 'Member', label='manipulates', style='dashed')
dot.edge('Service', 'Invitation', label='manipulates', style='dashed')

# Infrastructure connections
dot.edge('Service', 'PersistenceDB', label='persists', style='dashed')
dot.edge('Service', 'PersistenceRedis', label='persists', style='dashed')

# Common connections
dot.edge('API', 'CommonModel', label='uses', style='dashed')
dot.edge('API', 'CommonUtil', label='uses', style='dashed')
dot.edge('Service', 'CommonModel', label='uses', style='dashed')
dot.edge('Service', 'CommonUtil', label='uses', style='dashed')

# Render the diagram
dot.render('member_invitation_system_architecture', format='png', cleanup=True)