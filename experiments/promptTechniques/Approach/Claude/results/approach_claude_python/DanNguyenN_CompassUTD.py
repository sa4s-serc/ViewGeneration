from graphviz import Digraph

def create_architecture_diagram():
    # Initialize digraph
    dot = Digraph('CompassUTD_Architecture')
    dot.attr(rankdir='TB')

    # Define node styles
    dot.attr('node', shape='rectangle', style='rounded', fontname='Arial')

    # External Services Subgraph
    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='External Services', style='rounded', bgcolor='lightgrey')
        c.node('palm2', 'Google PaLM 2\n(Vertex AI)', shape='cylinder')
        c.node('mongodb', 'MongoDB\n(Chat History)', shape='cylinder')

    # Main Application Layers Subgraph
    with dot.subgraph(name='cluster_1') as c:
        c.attr(label='CompassUTD Application', style='rounded', bgcolor='lightblue')
        
        # API Layer
        c.node('api', 'API Layer\n(FastAPI)')
        
        # Inference Layer
        c.node('inference', 'Inference Layer\n(CompassInference)')
        
        # Tools Layer Subgraph
        with dot.subgraph(name='cluster_2') as tools:
            tools.attr(label='Tool Layer', style='rounded', bgcolor='lightgreen')
            tools.node('course_tool', 'Course Search')
            tools.node('degree_tool', 'Degree Search')
            tools.node('general_tool', 'General UTD Info')
            tools.node('rmp_tool', 'RateMyProfessor')
            tools.node('def_tool', 'Definition Lookup')
        
        # Web Scraping Layer
        c.node('webscrape', 'Web Scraping Layer')

    # Add edges
    dot.edge('api', 'inference', 'HTTP/REST')
    dot.edge('api', 'mongodb', 'Store/Retrieve\nChat History')
    dot.edge('inference', 'palm2', 'API Calls')
    dot.edge('inference', 'course_tool')
    dot.edge('inference', 'degree_tool')
    dot.edge('inference', 'general_tool')
    dot.edge('inference', 'rmp_tool')
    dot.edge('inference', 'def_tool')
    dot.edge('course_tool', 'webscrape')
    dot.edge('degree_tool', 'webscrape')
    dot.edge('general_tool', 'webscrape')
    dot.edge('rmp_tool', 'webscrape')

    # Save the diagram
    dot.render('compassutd_architecture', format='png', cleanup=True)

if __name__ == "__main__":
    create_architecture_diagram()