from graphviz import Digraph

def create_salesforce_integration_diagram():
    # Create a new directed graph
    dot = Digraph(comment='Salesforce REST Integration Architecture')
    dot.attr(rankdir='TB')
    
    # Set default node attributes
    dot.attr('node', shape='rectangle', style='filled', fillcolor='lightgrey')
    
    # Create clusters/subgraphs
    with dot.subgraph(name='cluster_0') as core:
        core.attr(label='Core Framework Components', style='rounded', bgcolor='lightblue')
        
        # Core framework components
        core.node('rest_wrapper', 'RestWrapper\n(Abstract Base Class)', shape='component')
        core.node('rest_response', 'RestResponse', shape='component')
        core.node('rest_callout', 'RestCallout\n(Base Class)', shape='component')
        core.node('rest_log_builder', 'RestLogBuilder', shape='component')
        core.node('rest_log', 'Rest_Log__c\nCustom Object', shape='cylinder')
        
        # Core framework relationships
        core.edge('rest_wrapper', 'rest_response', 'extends')
        core.edge('rest_callout', 'rest_log_builder', 'uses')
        core.edge('rest_log_builder', 'rest_log', 'creates')

    with dot.subgraph(name='cluster_1') as example:
        example.attr(label='Example Implementation', style='rounded', bgcolor='lightgreen')
        
        # Example implementation components
        example.node('example_rating', 'ExampleRatingRestResource', shape='component')
        example.node('example_callout', 'ExampleRatingCallout', shape='component')
        
        # Example implementation relationships
        example.edge('example_rating', 'rest_response', 'uses')
        example.edge('example_callout', 'rest_callout', 'extends')
        example.edge('example_callout', 'rest_log_builder', 'uses')

    with dot.subgraph(name='cluster_2') as external:
        external.attr(label='External Systems', style='rounded', bgcolor='lightpink')
        
        # External systems
        external.node('external_api', 'External Rating API', shape='cloud')
        
        # External system relationships
        external.edge('example_callout', 'external_api', 'HTTP calls')

    # Add legend
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', style='rounded', bgcolor='white')
        legend.node('comp_legend', 'Component', shape='component')
        legend.node('obj_legend', 'Custom Object', shape='cylinder')
        legend.node('ext_legend', 'External System', shape='cloud')

    # Set graph title
    dot.attr(label='Salesforce REST Integration Architecture\nArchitectural View', labelloc='t', fontsize='20')

    # Save the diagram
    dot.render('salesforce_integration_architecture', format='png', cleanup=True)

# Generate the diagram
create_salesforce_integration_diagram()