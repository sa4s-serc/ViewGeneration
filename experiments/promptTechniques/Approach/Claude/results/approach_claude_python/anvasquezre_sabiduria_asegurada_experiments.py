import graphviz

dot = graphviz.Digraph(comment='Policy Guru Chatbot Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('frontend', 'Chainlit Frontend\n(app/app.py)')
dot.node('agent', 'Langchain Agent\n(app/agent_utils.py)')
dot.node('qdrant', 'Qdrant Vector DB')
dot.node('preloader', 'Data Preloader\n(data_preloader/main.py)')
dot.node('s3', 'S3 Storage')
dot.node('google', 'Google Search API')

# Add subgraph for tools
with dot.subgraph(name='cluster_tools') as c:
    c.attr(label='Agent Tools')
    c.node('policy_tool', 'Policy Search Tool')
    c.node('web_tool', 'Web Search Tool')
    c.node('greeting_tool', 'Greeting Tool')

# Add edges
dot.edge('frontend', 'agent', 'User Questions')
dot.edge('agent', 'policy_tool', 'Policy Queries')
dot.edge('agent', 'web_tool', 'News Queries')
dot.edge('agent', 'greeting_tool', 'Greetings')
dot.edge('policy_tool', 'qdrant', 'Vector Search')
dot.edge('web_tool', 'google', 'Web Search')
dot.edge('s3', 'preloader', 'PDF Documents')
dot.edge('preloader', 'qdrant', 'Embeddings')
dot.edge('qdrant', 'agent', 'Search Results')
dot.edge('google', 'agent', 'Web Results')

# Save the diagram
dot.render('policy_guru_architecture', format='png', cleanup=True)