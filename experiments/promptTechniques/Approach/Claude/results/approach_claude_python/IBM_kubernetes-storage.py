from graphviz import Digraph

dot = Digraph(comment='Kubernetes Storage Workshop Architecture')
dot.attr(rankdir='TB')

# Global graph attributes
dot.attr('graph', fontname='Arial', pad='0.5')
dot.attr('node', fontname='Arial', shape='box', style='rounded,filled', fillcolor='lightgray')
dot.attr('edge', fontname='Arial')

# Define clusters
with dot.subgraph(name='cluster_docs') as docs:
    docs.attr(label='Documentation Layer', style='rounded', bgcolor='lightblue')
    docs.node('mkdocs', 'MkDocs Site\nConfiguration & Content')
    docs.node('labs', 'Lab Guides\n(Lab 0-7)')
    docs.node('admin', 'Admin Guide')
    
with dot.subgraph(name='cluster_app') as app:
    app.attr(label='Application Layer', style='rounded', bgcolor='lightgreen')
    app.node('guestbook', 'Guestbook App\n(Node.js)')
    app.node('yaml', 'Deployment YAMLs')

with dot.subgraph(name='cluster_storage') as storage:
    storage.attr(label='Storage Layer', style='rounded', bgcolor='lightyellow')
    storage.node('block', 'IBM Cloud\nBlock Storage')
    storage.node('file', 'IBM Cloud\nFile Storage') 
    storage.node('object', 'IBM Cloud\nObject Storage')
    storage.node('portworx', 'Portworx SDS')

with dot.subgraph(name='cluster_ci') as ci:
    ci.attr(label='CI/CD Layer', style='rounded', bgcolor='lightpink')
    ci.node('travis', 'Travis CI\n(Markdown Lint)')
    ci.node('actions', 'GitHub Actions\n(Build & Deploy)')

# Add edges
dot.edge('mkdocs', 'labs')
dot.edge('mkdocs', 'admin')
dot.edge('labs', 'guestbook', 'deploys')
dot.edge('yaml', 'guestbook', 'configures')
dot.edge('guestbook', 'block', 'uses')
dot.edge('guestbook', 'file', 'uses')
dot.edge('guestbook', 'object', 'uses')
dot.edge('guestbook', 'portworx', 'uses')
dot.edge('travis', 'mkdocs', 'validates')
dot.edge('actions', 'mkdocs', 'publishes')

# Save diagram
dot.render('kubernetes_storage_workshop', format='png', cleanup=True)