from graphviz import Digraph

dot = Digraph(comment='Terraform Security Dojo Architecture')

# Define nodes for main components
dot.node('IaC', 'Infrastructure as Code', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('EnvIso', 'Environment Isolation', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('LoadBal', 'Load Balancing', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('NetSec', 'Network Security', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('Tut', 'Exercise/Tutorial', shape='rectangle', style='filled', fillcolor='lightgray')
dot.node('VSCode', 'VSCode Remote Boxes', shape='rectangle', style='filled', fillcolor='lightcoral')

# Define nodes for important files
dot.node('main_tf', 'main.tf', shape='ellipse', style='filled', fillcolor='white')
dot.node('output_tf', 'output.tf', shape='ellipse', style='filled', fillcolor='white')
dot.node('variables_tf', 'variables.tf', shape='ellipse', style='filled', fillcolor='white')
dot.node('network_tf', 'network.tf', shape='ellipse', style='filled', fillcolor='white')
dot.node('prd_tfvars', 'prd.tfvars', shape='ellipse', style='filled', fillcolor='white')
dot.node('dev_tfvars', 'dev.tfvars', shape='ellipse', style='filled', fillcolor='white')
dot.node('providers_tf', '_providers.tf', shape='ellipse', style='filled', fillcolor='white')
dot.node('backend_tf', '_backend.tf', shape='ellipse', style='filled', fillcolor='white')
dot.node('install_apache_tpl', 'install_apache.sh.tpl', shape='ellipse', style='filled', fillcolor='white')
dot.node('bootstrap_main_tf', 'bootstrap/main.tf', shape='ellipse', style='filled', fillcolor='white')
dot.node('bootstrap_output_tf', 'bootstrap/output.tf', shape='ellipse', style='filled', fillcolor='white')
dot.node('env_tfvars_tpl', 'env.tfvars.tpl', shape='ellipse', style='filled', fillcolor='white')
dot.node('vscode_box', 'vscode-box/*', shape='ellipse', style='filled', fillcolor='white')

# Define edges for connectivity
dot.edge('IaC', 'main_tf')
dot.edge('IaC', 'output_tf')
dot.edge('IaC', 'variables_tf')
dot.edge('IaC', 'network_tf')
dot.edge('EnvIso', 'prd_tfvars')
dot.edge('EnvIso', 'dev_tfvars')
dot.edge('LoadBal', 'main_tf')
dot.edge('NetSec', 'network_tf')
dot.edge('Tut', 'main_tf')
dot.edge('Tut', 'install_apache_tpl')
dot.edge('VSCode', 'vscode_box')
dot.edge('IaC', 'providers_tf')
dot.edge('IaC', 'backend_tf')
dot.edge('EnvIso', 'bootstrap_main_tf')
dot.edge('EnvIso', 'bootstrap_output_tf')
dot.edge('EnvIso', 'env_tfvars_tpl')

# Render the diagram
dot.render('terraform_security_dojo_architecture', format='png', cleanup=True)