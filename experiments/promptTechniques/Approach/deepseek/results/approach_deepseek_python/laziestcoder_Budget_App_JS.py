import graphviz

dot = graphviz.Digraph(comment='Budget App Architecture')
dot.attr(rankdir='TB', size='8,5')

# Define nodes with styles
dot.node('UI', 'User Interface\n(HTML/CSS)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('Controller', 'Controller\n(script.js)', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('BudgetController', 'Budget Controller\n(script.js)', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('UIController', 'UI Controller\n(script.js)', shape='rectangle', style='filled', fillcolor='lightyellow')

# Define edges to show interactions
dot.edge('UI', 'Controller', label='User Input')
dot.edge('Controller', 'BudgetController', label='Data Update')
dot.edge('Controller', 'UIController', label='UI Update Request')
dot.edge('BudgetController', 'Controller', label='Budget Data')
dot.edge('UIController', 'UI', label='Render Updates')

# Render the diagram
dot.render('budget_app_architecture', format='png', cleanup=True)