import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='MAAV Bot Architecture')
dot.attr(rankdir='TB')
dot.attr(fontname='Arial')
dot.attr('node', shape='box', style='rounded', fontname='Arial')

# Define node attributes for different types
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')

# Core Components
dot.node('bot_core', 'Bot Core\n(bot.js)\nDialog Management\nConversation Flow')
dot.node('display', 'Display Manager\n(botdisplay.js)\nAdaptive Cards\nMarkdown Rendering')
dot.node('entry', 'Entry Point\n(index.js)\nRestify Server\nAzure Functions')

# External Services
dot.attr('node', shape='cylinder', style='filled', fillcolor='lightgreen')
dot.node('azure_sql', 'Azure SQL Database\nConversation Data\nAuth Codes')
dot.node('powerbi', 'Power BI Dashboard\nData Visualization')

# Channels & Integration
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightyellow')
dot.node('channels', 'Bot Channels\nEmulator\nWebchat\nEmail')
dot.node('auth', 'Authentication\nPin-Based Access')
dot.node('fuzzy', 'Fuzzy Matching\nCompany Names')

# Create subgraph for presentation layer
with dot.subgraph(name='cluster_0') as s:
    s.attr(label='Presentation Layer', style='rounded', color='gray')
    s.node('ui_cards', 'Adaptive Cards\nInteractive UI')
    s.node('email_parse', 'Email Parser\nTemplate Processing')

# Add edges
dot.edge('entry', 'bot_core', 'initializes')
dot.edge('bot_core', 'display', 'renders UI')
dot.edge('bot_core', 'azure_sql', 'stores/retrieves')
dot.edge('channels', 'bot_core', 'user interaction')
dot.edge('display', 'ui_cards', 'generates')
dot.edge('bot_core', 'auth', 'validates')
dot.edge('bot_core', 'fuzzy', 'matches')
dot.edge('azure_sql', 'powerbi', 'feeds')
dot.edge('channels', 'email_parse', 'processes')
dot.edge('email_parse', 'bot_core', 'structured data')

# Set graph attributes
dot.attr(label='MAAV Bot Architecture\nMulti-Channel Conversation Recording System', labelloc='t')

# Render the graph
dot.render('maav_bot_architecture', format='png', cleanup=True)