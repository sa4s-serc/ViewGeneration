from graphviz import Digraph

dot = Digraph(comment='Budget App Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('UI', 'UI Controller\n(UIController)')
dot.node('CTRL', 'Controller\n(Main Controller)')
dot.node('DATA', 'Budget Controller\n(budgetController)')
dot.node('HTML', 'index.html')
dot.node('CSS', 'style.css')
dot.node('JS', 'script.js')

# Add subcomponents
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='View Layer')
    c.node('income_view', 'Income View')
    c.node('expense_view', 'Expense View')
    c.node('budget_view', 'Budget Overview')

# Add connections
dot.edge('HTML', 'UI')
dot.edge('CSS', 'UI')
dot.edge('JS', 'CTRL')
dot.edge('UI', 'CTRL', 'UI Events')
dot.edge('CTRL', 'DATA', 'Data Operations')
dot.edge('DATA', 'CTRL', 'Budget Updates')
dot.edge('CTRL', 'UI', 'UI Updates')
dot.edge('UI', 'income_view')
dot.edge('UI', 'expense_view')
dot.edge('UI', 'budget_view')

# Generate diagram
dot.render('budget_app_architecture', format='png', cleanup=True)