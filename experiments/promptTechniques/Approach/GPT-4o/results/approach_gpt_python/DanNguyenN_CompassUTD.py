from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='CompassUTD Chatbot Architecture')

# Set graph attributes
dot.attr(rankdir='TB', size='10')
dot.attr('node', shape='rectangle', style='filled', color='lightgrey')

# API Layer
dot.node('API', 'FastAPI Backend\n(fast_api_app/app/main.py)', color='lightblue')

# Inference Layer
dot.node('Inference', 'Inference Logic\n(CompassUTD/inference.py)', color='lightgreen')

# Tool Layer
dot.node('Tools', 'Information Retrieval Tools\n(CompassUTD/tools/)', color='lightcoral')

# Web Scraping Layer
dot.node('WebScrape', 'Web Scraping\n(CompassUTD/webscrape/)', color='lightpink')

# Database
dot.node('DB', 'MongoDB', color='lightyellow')

# LLM
dot.node('LLM', "Google's PaLM 2 via Vertex AI", color='lightcyan')

# Connect nodes
dot.edge('API', 'Inference', label='Handles Requests')
dot.edge('Inference', 'Tools', label='Orchestrates')
dot.edge('Inference', 'WebScrape', label='Utilizes')
dot.edge('Inference', 'DB', label='Stores/Retrieves')
dot.edge('Inference', 'LLM', label='Interacts with')

# Render the graph
dot.render('compassutd_architecture', format='png', cleanup=True)