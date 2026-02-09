from graphviz import Digraph

dot = Digraph(comment='PyJailBreak Frontend Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Frontend Components
dot.node('ui', 'UI Layer\n(React + Next.js)')
dot.node('state', 'State Management\n(Redux Toolkit)')
dot.node('components', 'React Components')
dot.node('api_client', 'API Client Layer')

# Components within UI Layer
with dot.subgraph(name='cluster_components') as c:
    c.attr(label='Core Components')
    c.node('req_form', 'RequestForm.tsx')
    c.node('exec_attack', 'ExecuteAttack.tsx')
    c.node('dialog_editor', 'DialogEditor.tsx')
    c.node('data_grid', 'DataGridFooters.tsx')

# State Management Components
with dot.subgraph(name='cluster_state') as s:
    s.attr(label='State Slices')
    s.node('payload_slice', 'payloadsSlice.ts')
    s.node('emulate_slice', 'emulateSlice.ts')
    s.node('endpoint_slice', 'endPointsSlice.ts')
    s.node('dialog_slice', 'dialogSlice.ts')

# Add edges
dot.edge('ui', 'components')
dot.edge('components', 'state')
dot.edge('components', 'api_client')
dot.edge('api_client', 'Backend API')

# Component relationships
dot.edge('req_form', 'exec_attack')
dot.edge('req_form', 'payload_slice')
dot.edge('dialog_editor', 'dialog_slice')
dot.edge('data_grid', 'payload_slice')
dot.edge('exec_attack', 'endpoint_slice')
dot.edge('exec_attack', 'emulate_slice')

# Generate diagram
dot.render('pyjailbreak_frontend_architecture', format='png', cleanup=True)