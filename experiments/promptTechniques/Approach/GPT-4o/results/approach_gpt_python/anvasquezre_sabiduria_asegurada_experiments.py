from graphviz import Digraph

def create_architecture_diagram():
    dot = Digraph(comment='Policy Guru Chatbot Architecture')

    # Define nodes for services
    dot.node('A', 'Chainlit Front-end', shape='rectangle', style='filled', fillcolor='lightblue')
    dot.node('B', 'Langchain Agent', shape='rectangle', style='filled', fillcolor='lightgreen')
    dot.node('C', 'Qdrant Database', shape='cylinder', style='filled', fillcolor='orange')
    dot.node('D', 'Data Preloader', shape='rectangle', style='filled', fillcolor='lightcoral')
    dot.node('E', 'Google Search', shape='rectangle', style='filled', fillcolor='lightyellow')

    # Define edges for communication
    dot.edge('A', 'B', label='User Queries', dir='both')
    dot.edge('B', 'C', label='Semantic Retrieval', dir='both')
    dot.edge('B', 'E', label='Web Search', dir='both')
    dot.edge('D', 'C', label='Load Embeddings', dir='both')
    dot.edge('D', 'S3', label='Download PDFs', dir='both', style='dashed')
    dot.edge('A', 'Feedback', label='User Feedback', dir='both', style='dashed')

    # Define node for S3 bucket
    dot.node('S3', 'S3 Bucket', shape='cylinder', style='dotted', fillcolor='lightgray')

    # Define edge for feedback
    dot.node('Feedback', 'Feedback Mechanism', shape='ellipse', style='dotted', fillcolor='lightgray')

    # Render diagram
    dot.render('policy_guru_chatbot_architecture', format='png', cleanup=True)

create_architecture_diagram()