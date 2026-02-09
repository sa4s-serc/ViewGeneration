from graphviz import Digraph

def create_tiramisu_architecture():
    dot = Digraph('Tiramisu Architecture')
    dot.attr(rankdir='TB')
    
    # Define node styles
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')
    
    # Create subgraph for client layer
    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='Client Layer', style='rounded', color='blue')
        c.node('mobile_client', 'Mobile Client\n(Ionic/Angular)')
        c.node('local_storage', 'Local Storage')
        c.node('push_notif', 'Push Notifications')
        
    # Create subgraph for frontend layer
    with dot.subgraph(name='cluster_1') as c:
        c.attr(label='Frontend Layer', style='rounded', color='green')
        c.node('java_frontend', 'Java Frontend')
        c.node('schedules_servlet', 'SchedulesServlet')
        c.node('fav_route_servlet', 'FavRouteServlet')
        c.node('status_log_servlet', 'StatusLogServlet')
        c.node('alarm_servlet', 'AlarmServlet')

    # Create subgraph for backend layer
    with dot.subgraph(name='cluster_2') as c:
        c.attr(label='Backend Layer', style='rounded', color='red')
        c.node('feed_grabber', 'FeedGrabber')
        c.node('obs_processor', 'ObservationProcessor')
        c.node('dynamo_cleaner', 'DynamoCleaner')
        c.node('alarm_processor', 'AlarmProcessor')

    # Create subgraph for prediction layer
    with dot.subgraph(name='cluster_3') as c:
        c.attr(label='Prediction Layer', style='rounded', color='purple')
        c.node('route_predictor', 'Route Predictor\n(Random Forest)')

    # Create subgraph for storage layer
    with dot.subgraph(name='cluster_4') as c:
        c.attr(label='Storage Layer', style='rounded', color='orange')
        c.node('dynamodb', 'DynamoDB', shape='cylinder')
        c.node('postgres', 'PostgreSQL', shape='cylinder')
        c.node('sqs', 'AWS SQS', shape='cylinder')

    # Add edges between components
    # Client layer connections
    dot.edge('mobile_client', 'local_storage')
    dot.edge('mobile_client', 'push_notif')
    dot.edge('mobile_client', 'java_frontend')

    # Frontend layer connections
    dot.edge('java_frontend', 'schedules_servlet')
    dot.edge('java_frontend', 'fav_route_servlet')
    dot.edge('java_frontend', 'status_log_servlet')
    dot.edge('java_frontend', 'alarm_servlet')

    # Backend layer connections
    dot.edge('feed_grabber', 'sqs')
    dot.edge('sqs', 'obs_processor')
    dot.edge('obs_processor', 'dynamodb')
    dot.edge('dynamo_cleaner', 'dynamodb')
    dot.edge('alarm_processor', 'dynamodb')

    # Data access connections
    dot.edge('schedules_servlet', 'dynamodb')
    dot.edge('fav_route_servlet', 'postgres')
    dot.edge('status_log_servlet', 'postgres')
    dot.edge('route_predictor', 'postgres')
    dot.edge('alarm_servlet', 'alarm_processor')

    # Save the diagram
    dot.render('tiramisu_architecture', format='png', cleanup=True)

create_tiramisu_architecture()