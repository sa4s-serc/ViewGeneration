from graphviz import Digraph

dot = Digraph(comment='BTCPay Server Documentation Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Core Components
dot.node('docs', 'Documentation Core\n(VuePress)')
dot.node('user_guides', 'User Guides')
dot.node('deploy_docs', 'Deployment\nDocumentation')
dot.node('dev_docs', 'Development\nDocumentation')
dot.node('api_docs', 'API Integration')
dot.node('trouble_faq', 'Troubleshooting\n& FAQ')
dot.node('theme_docs', 'Theming')

# Key Files & Components
dot.node('content', 'Content\n(Markdown Files)')
dot.node('config', 'VuePress Config\n(.vuepress/config.js)')
dot.node('theme', 'Custom Theme\n(.vuepress/theme/)')
dot.node('scripts', 'Build Scripts')
dot.node('workflows', 'GitHub Actions')

# Connections
dot.edge('docs', 'user_guides')
dot.edge('docs', 'deploy_docs')
dot.edge('docs', 'dev_docs')
dot.edge('docs', 'api_docs')
dot.edge('docs', 'trouble_faq')
dot.edge('docs', 'theme_docs')

dot.edge('content', 'docs')
dot.edge('config', 'docs')
dot.edge('theme', 'docs')
dot.edge('scripts', 'docs')
dot.edge('workflows', 'docs')

# Subcomponents
dot.edge('dev_docs', 'API Integration')
dot.edge('theme_docs', 'theme')
dot.edge('deploy_docs', 'scripts')

print(dot.source)
dot.render('btcpay_docs_architecture', view=True, format='png')