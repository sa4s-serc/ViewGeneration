from graphviz import Digraph

dot = Digraph(comment='Employee Management System Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded', fontname='Arial')
dot.attr('edge', fontname='Arial')

# Add main services
dot.node('frontend', 'Frontend\n(ReactJS)')
dot.node('gateway', 'API Gateway\n(Spring Boot)')
dot.node('webserver', 'Nginx\nWebserver')

# Add backend microservices
dot.node('attendance', 'Attendance Service\n(Golang/Gin)')
dot.node('employee', 'Employee Service\n(Golang/Gin)')
dot.node('salary', 'Salary Service\n(Golang/Gin)')
dot.node('notification', 'Notification Service\n(Python)')

# Add databases
dot.node('mysql', 'MySQL\n(Attendance Data)', shape='cylinder')
dot.node('elastic', 'Elasticsearch\n(Employee & Salary Data)', shape='cylinder')

# Connect components
dot.edge('webserver', 'frontend')
dot.edge('frontend', 'gateway')
dot.edge('gateway', 'attendance')
dot.edge('gateway', 'employee')
dot.edge('gateway', 'salary')
dot.edge('gateway', 'notification')

# Database connections
dot.edge('attendance', 'mysql')
dot.edge('employee', 'elastic')
dot.edge('salary', 'elastic')
dot.edge('notification', 'elastic')

# Add subgraph for services
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Microservices')
    c.attr('node', style='rounded')
    c.node('attendance')
    c.node('employee')
    c.node('salary')
    c.node('notification')

dot.render('employee_management_system_architecture', format='png', cleanup=True)