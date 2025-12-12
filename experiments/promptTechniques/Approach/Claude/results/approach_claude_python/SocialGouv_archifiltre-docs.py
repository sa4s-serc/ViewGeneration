from graphviz import Digraph

dot = Digraph(comment='Archifiltre-docs Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main components
dot.node('UI', 'User Interface\n(React)')
dot.node('State', 'State Management\n(Redux + Undoable)')
dot.node('FileSystem', 'File System\nProcessing')
dot.node('Workers', 'Async Workers\n(Node.js Child Processes)')
dot.node('Export', 'Export System\n(Multiple Formats)')
dot.node('Meta', 'Metadata\nManagement')
dot.node('Track', 'Tracking System\n(Sentry + Matomo)')
dot.node('Config', 'User Configuration')
dot.node('I18n', 'Internationalization\n(i18next)')
dot.node('Update', 'Auto Updates\n(electron-updater)')

# Add relationships
dot.edge('UI', 'State', 'Updates/Queries')
dot.edge('State', 'FileSystem', 'File Operations')
dot.edge('FileSystem', 'Workers', 'Async Tasks')
dot.edge('State', 'Export', 'Export Data')
dot.edge('State', 'Meta', 'Metadata Operations')
dot.edge('UI', 'Track', 'Usage/Errors')
dot.edge('UI', 'Config', 'Settings')
dot.edge('UI', 'I18n', 'Translations')
dot.edge('Update', 'UI', 'Update Notifications')
dot.edge('Workers', 'State', 'Task Results')

# Generate the diagram
dot.render('archifiltre_architecture', format='png', cleanup=True)