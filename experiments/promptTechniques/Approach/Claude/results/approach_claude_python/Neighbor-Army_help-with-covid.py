from graphviz import Digraph

def create_architecture_diagram():
    # Create a new directed graph
    dot = Digraph(comment='Help-with-COVID System Architecture')
    dot.attr(rankdir='TB')

    # Define node styles
    dot.attr('node', shape='box', style='rounded', fontname='Arial')

    # Add main components
    dot.node('frontend', 'Frontend\n(Next.js)', fillcolor='lightblue', style='filled,rounded')
    dot.node('firebase', 'Firebase\nBackend', fillcolor='orange', style='filled,rounded')
    dot.node('auth', 'Firebase\nAuthentication', fillcolor='yellow', style='filled,rounded')
    dot.node('firestore', 'Firebase\nFirestore', fillcolor='lightgreen', style='filled,rounded')

    # Add external services
    with dot.subgraph(name='cluster_external') as ext:
        ext.attr(label='External Services', style='dashed')
        ext.node('onfleet', 'Onfleet\nTask Management', fillcolor='lightpink', style='filled,rounded')
        ext.node('sendgrid', 'Sendgrid\nEmail Service', fillcolor='lightgrey', style='filled,rounded')
        ext.node('gmaps', 'Google Maps API\nAddress Service', fillcolor='lightcyan', style='filled,rounded')
        ext.node('twilio', 'Twilio\nPhone Verification', fillcolor='lightyellow', style='filled,rounded')

    # Add connections
    dot.edge('frontend', 'firebase', 'API Calls')
    dot.edge('frontend', 'auth', 'User Authentication')
    dot.edge('firebase', 'firestore', 'CRUD Operations')
    dot.edge('firebase', 'onfleet', 'Task Management')
    dot.edge('firebase', 'sendgrid', 'Email Communications')
    dot.edge('frontend', 'gmaps', 'Address Autocomplete')
    dot.edge('firebase', 'twilio', 'Phone/Zipcode Verification')

    # Save the diagram
    dot.render('architecture_diagram', format='png', cleanup=True)

if __name__ == "__main__":
    create_architecture_diagram()