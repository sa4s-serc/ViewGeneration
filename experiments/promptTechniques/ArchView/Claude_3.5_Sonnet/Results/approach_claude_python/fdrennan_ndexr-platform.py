from graphviz import Digraph

def create_architecture_diagram():
    # Initialize diagram
    dot = Digraph(comment='Data Pipeline Architecture')
    dot.attr(rankdir='TB')

    # Define node styles
    dot.attr('node', shape='rectangle', style='rounded,filled', fillcolor='lightgray')
    dot.attr('edge', fontsize='10')

    # Create clusters/subgraphs
    with dot.subgraph(name='cluster_frontend') as frontend:
        frontend.attr(label='Frontend Layer', style='rounded', color='blue')
        frontend.node('shiny', 'Shiny Application\n(redditor-shiny.Rproj)')

    with dot.subgraph(name='cluster_api') as api:
        api.attr(label='API Layer', style='rounded', color='green')
        api.node('plumber', 'R Plumber API\n(redditor-api/plumber.R)')

    with dot.subgraph(name='cluster_orchestration') as orchestration:
        orchestration.attr(label='Orchestration Layer', style='rounded', color='orange')
        orchestration.node('airflow', 'Airflow DAGs\n(Data Pipeline Control)')

    with dot.subgraph(name='cluster_data') as data:
        data.attr(label='Data Layer', style='rounded', color='red')
        data.node('reddit', 'Reddit Data Ingestion\n(PRAW)')
        data.node('postgres', 'PostgreSQL\nDatabase')
        data.node('elastic', 'Elasticsearch\n(Search)')

    with dot.subgraph(name='cluster_cloud') as cloud:
        cloud.attr(label='Cloud Infrastructure', style='rounded', color='purple')
        cloud.node('s3', 'AWS S3\n(Storage)')
        cloud.node('ec2', 'AWS EC2\n(Compute)')
        cloud.node('sns', 'AWS SNS\n(Messaging)')

    # Add monitoring component
    dot.node('monitoring', 'System Monitoring\n(Glances)', shape='rectangle')

    # Define relationships
    dot.edge('shiny', 'plumber', 'HTTP/REST')
    dot.edge('plumber', 'postgres', 'Data Queries')
    dot.edge('airflow', 'reddit', 'Schedule & Control')
    dot.edge('reddit', 'postgres', 'Store Data')
    dot.edge('postgres', 's3', 'Backup')
    dot.edge('postgres', 'elastic', 'Index')
    dot.edge('ec2', 'airflow', 'Hosts')
    dot.edge('airflow', 'sns', 'Notifications')
    dot.edge('monitoring', 'sns', 'Alerts')

    # Save the diagram
    dot.render('architecture_diagram', format='png', cleanup=True)

if __name__ == "__main__":
    create_architecture_diagram()