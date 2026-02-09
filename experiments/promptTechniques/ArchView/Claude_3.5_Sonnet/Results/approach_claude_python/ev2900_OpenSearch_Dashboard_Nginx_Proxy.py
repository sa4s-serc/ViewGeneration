from graphviz import Digraph

# Create a new directed graph
g = Digraph('OpenSearch_Dashboard_Architecture')
g.attr(rankdir='TB')

# Add global styles
g.attr('node', shape='rectangle', style='filled', fontname='Arial')
g.attr('edge', fontname='Arial', fontsize='10')

# Create VPC cluster
with g.subgraph(name='cluster_vpc') as vpc:
    vpc.attr(label='AWS VPC', style='dashed', color='gray')
    
    # Create public subnet cluster
    with vpc.subgraph(name='cluster_public') as public:
        public.attr(label='Public Subnet', style='dashed', color='blue')
        public.node('nginx', 'Nginx Proxy\nServer', fillcolor='lightblue')
        
    # Create private subnet cluster
    with vpc.subgraph(name='cluster_private') as private:
        private.attr(label='Private Subnet', style='dashed', color='green')
        private.node('dashboard', 'OpenSearch\nDashboard', fillcolor='lightgreen')
        private.node('opensearch', 'OpenSearch\nDomain', fillcolor='lightgreen')

# Add external user
g.node('user', 'Public Internet\nUser', shape='oval', fillcolor='lightgray')

# Add security group indicators
g.node('sg_public', 'Security Group\n(Allow HTTPS)', shape='note', fillcolor='lightyellow')
g.node('sg_private', 'Security Group\n(Internal Traffic)', shape='note', fillcolor='lightyellow')

# Add connections
g.edge('user', 'nginx', 'HTTPS (443)')
g.edge('nginx', 'dashboard', 'Forward Request')
g.edge('dashboard', 'opensearch', 'Query Data')

# Add invisible edges for layout
g.edge('sg_public', 'nginx', '', style='invisible')
g.edge('sg_private', 'dashboard', '', style='invisible')

# Add legend
with g.subgraph(name='cluster_legend') as legend:
    legend.attr(label='Legend', style='solid')
    legend.node('l1', 'Public Component', fillcolor='lightblue')
    legend.node('l2', 'Private Component', fillcolor='lightgreen')
    legend.node('l3', 'Security Control', fillcolor='lightyellow')

# Save the diagram
g.render('opensearch_dashboard_architecture', format='png', cleanup=True)