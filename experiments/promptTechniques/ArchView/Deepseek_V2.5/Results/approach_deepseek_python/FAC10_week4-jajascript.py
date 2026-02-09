import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='Nobel Prize Laureates Autocomplete Application Architecture')

# Set graph attributes for better layout
dot.attr(rankdir='TB', size='8,8', concentrate='false')

# Define node attributes
dot.attr('node', shape='rectangle', style='filled', fillcolor='lightblue', fontname='Arial')

# Front-end components
dot.node('index_html', 'index.html\n(UI with search input)')
dot.node('main_css', 'main.css\n(Styling)')
dot.node('main_js', 'main.js\n(Front-end logic)')

# Back-end components
dot.node('server_js', 'server.js\n(Node.js server)')
dot.node('router_js', 'router.js\n(Request routing)')
dot.node('handler_js', 'handler.js\n(Request handling)')
dot.node('algorithm_js', 'algorithm.js\n(Autocomplete logic)')
dot.node('data_json', 'data.json\n(Laureates data)')

# Testing components
dot.node('qunit_html', 'qunit.html\n(Test runner)')
dot.node('frontend_tests', 'frontendTests.js\n(Front-end tests)')
dot.node('backend_tests', 'backendTests.js\n(Back-end tests)')

# Documentation
dot.node('readme_md', 'README.md\n(Documentation)')

# Define edges to show relationships
# Front-end relationships
dot.edge('index_html', 'main_css', label='uses')
dot.edge('index_html', 'main_js', label='uses')
dot.edge('main_js', 'server_js', label='HTTP requests', style='dashed')

# Back-end relationships
dot.edge('server_js', 'router_js', label='uses')
dot.edge('router_js', 'handler_js', label='routes to')
dot.edge('handler_js', 'algorithm_js', label='calls')
dot.edge('algorithm_js', 'data_json', label='reads')

# Testing relationships
dot.edge('qunit_html', 'frontend_tests', label='runs')
dot.edge('frontend_tests', 'main_js', label='tests', style='dotted')
dot.edge('backend_tests', 'algorithm_js', label='tests', style='dotted')

# Group components
with dot.subgraph(name='cluster_frontend') as c:
    c.attr(style='filled', color='lightgrey', label='Front-end (Public Directory)')
    c.node('index_html')
    c.node('main_css')
    c.node('main_js')

with dot.subgraph(name='cluster_backend') as c:
    c.attr(style='filled', color='lightyellow', label='Back-end (Src Directory)')
    c.node('server_js')
    c.node('router_js')
    c.node('handler_js')
    c.node('algorithm_js')
    c.node('data_json')

with dot.subgraph(name='cluster_testing') as c:
    c.attr(style='filled', color='lightgreen', label='Testing (Test Directory)')
    c.node('qunit_html')
    c.node('frontend_tests')
    c.node('backend_tests')

with dot.subgraph(name='cluster_docs') as c:
    c.attr(style='filled', color='lightcoral', label='Documentation')
    c.node('readme_md')

# Render the diagram
dot.render('nobel_prize_architecture', format='png', cleanup=True)