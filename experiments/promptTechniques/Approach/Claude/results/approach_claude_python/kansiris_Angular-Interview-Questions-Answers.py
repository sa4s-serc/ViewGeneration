from graphviz import Digraph

dot = Digraph(comment='Angular Interview Questions Repository Architecture')
dot.attr(rankdir='TB')

# Add nodes
dot.node('qa_collection', 'Q&A Collection\nExtensive Interview Questions', shape='box')
dot.node('code_examples', 'Code Examples\nPractical Snippets', shape='box')
dot.node('navigation', 'Navigation\nTable of Contents', shape='box')
dot.node('readme', 'README\nProject Documentation', shape='box')
dot.node('license', 'License\nApache 2.0', shape='box')

# Add core components
dot.node('core', 'Core Repository', shape='box', style='filled', fillcolor='lightgray')

# Add knowledge areas
dot.node('basics', 'Angular Basics', shape='box')
dot.node('advanced', 'Advanced Topics', shape='box')
dot.node('rxjs', 'RxJS', shape='box')
dot.node('material', 'Angular Material', shape='box')
dot.node('cli', 'Angular CLI', shape='box')

# Add relationships
dot.edge('core', 'qa_collection')
dot.edge('core', 'code_examples')
dot.edge('core', 'navigation')
dot.edge('core', 'readme')
dot.edge('core', 'license')

# Connect knowledge areas
dot.edge('qa_collection', 'basics')
dot.edge('qa_collection', 'advanced')
dot.edge('qa_collection', 'rxjs')
dot.edge('qa_collection', 'material')
dot.edge('qa_collection', 'cli')

# Add code examples relationships
dot.edge('code_examples', 'basics')
dot.edge('code_examples', 'advanced')
dot.edge('code_examples', 'rxjs')

print(dot.source)
dot.render('angular_interview_architecture', format='png', cleanup=True)