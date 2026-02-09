from graphviz import Digraph

dot = Digraph(comment='Apache APISIX Dashboard Frontend Architecture')
dot.attr(rankdir='TB')

# Add nodes for main components
dot.node('UI', 'UI Components\n(Mantine UI, Ant Design Pro)', shape='box')
dot.node('routing', 'Routing\n(TanStack Router)', shape='box')
dot.node('state', 'State Management\n(MobX, TanStack Query)', shape='box')
dot.node('api', 'API Layer\n(Axios)', shape='box')
dot.node('forms', 'Form Handling\n(React Hook Form, Zod)', shape='box')
dot.node('i18n', 'Internationalization\n(react-i18next)', shape='box')

# Add edges to show relationships
dot.edge('UI', 'routing', 'navigates')
dot.edge('UI', 'state', 'consumes/updates')
dot.edge('state', 'api', 'fetches data')
dot.edge('UI', 'forms', 'validates input')
dot.edge('forms', 'api', 'submits data')
dot.edge('UI', 'i18n', 'translates')

# Add subgraph for CRUD operations
with dot.subgraph(name='cluster_crud') as crud:
    crud.attr(label='CRUD Operations')
    crud.node('create', 'Create')
    crud.node('read', 'Read')
    crud.node('update', 'Update')
    crud.node('delete', 'Delete')
    crud.edge('create', 'api')
    crud.edge('read', 'api')
    crud.edge('update', 'api')
    crud.edge('delete', 'api')

# Render the diagram
dot.render('apisix_dashboard_architecture', format='png', cleanup=True)