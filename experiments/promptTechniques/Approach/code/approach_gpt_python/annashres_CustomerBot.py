from graphviz import Digraph

def generate_diagram():
    dot = Digraph(comment='MAAV Bot Framework Architecture')
    
    # Set graph attributes
    dot.attr(rankdir='LR')
    
    # Components
    dot.node('A', 'Bot (messages/index.js)', shape='rectangle')
    dot.node('B', 'Bot Logic (messages/bot.js)', shape='rectangle')
    dot.node('C', 'Display Management (messages/botdisplay.js)', shape='rectangle')
    dot.node('D', 'Azure Bot Service', shape='rectangle')
    dot.node('E', 'Azure SQL Database', shape='rectangle')
    dot.node('F', 'Power BI Dashboard', shape='rectangle')
    dot.node('G', 'Adaptive Cards', shape='rectangle')
    dot.node('H', 'User Authentication', shape='rectangle')
    
    # Channels
    dot.node('I', 'Emulator', shape='ellipse')
    dot.node('J', 'Webchat', shape='ellipse')
    dot.node('K', 'Email', shape='ellipse')
    
    # Connections
    dot.edge('A', 'D', label='Connects to')
    dot.edge('A', 'B', label='Executes')
    dot.edge('B', 'E', label='Stores/Retrieves Data')
    dot.edge('B', 'G', label='Renders')
    dot.edge('C', 'G', label='Manages')
    dot.edge('C', 'F', label='Integrates with')
    dot.edge('B', 'H', label='Verifies Users')
    dot.edge('D', 'I', label='Channel')
    dot.edge('D', 'J', label='Channel')
    dot.edge('D', 'K', label='Channel')
    
    # Display diagram
    dot.render('maav_bot_architecture', format='png', cleanup=True)

generate_diagram()