from graphviz import Digraph

dot = Digraph(comment='Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('frontend', 'Frontend\nReact Components')
dot.node('questions', 'Interview Questions\nMarkdown Content')
dot.node('topics', 'Topic Categories\nHTML/CSS/JS/React/Redux')
dot.node('answers', 'Detailed Answers\nCode Examples')
dot.node('resources', 'External Resources\nLinks')
dot.node('readme', 'README.md\nNavigation')

# Add relationships
dot.edge('readme', 'topics', 'organizes')
dot.edge('topics', 'questions', 'contains')
dot.edge('questions', 'answers', 'includes')
dot.edge('answers', 'resources', 'references')
dot.edge('frontend', 'readme', 'displays')
dot.edge('frontend', 'questions', 'renders')
dot.edge('frontend', 'answers', 'shows')

# Save diagram
dot.render('architecture_view', format='png', cleanup=True)