from graphviz import Digraph

dot = Digraph(comment='Qubes OS CTAP Proxy Architecture')

# Define nodes for VMs
dot.node('Browser VM', 'Browser VM\n(Client)', shape='rect', style='filled', fillcolor='lightblue')
dot.node('sys-usb VM', 'sys-usb VM\n(Server)', shape='rect', style='filled', fillcolor='lightgreen')

# Define nodes for key components
dot.node('CTAPHID Emulation', 'CTAPHID Emulation', shape='rect', style='filled', fillcolor='lightgrey')
dot.node('Qrexec Transport', 'Qrexec Transport', shape='rect', style='filled', fillcolor='lightgrey')
dot.node('CTAP Protocol Handlers', 'CTAP Protocol Handlers\n(CTAP1/U2F, CTAP2)', shape='rect', style='filled', fillcolor='lightgrey')
dot.node('Policy Enforcement', 'Policy Enforcement', shape='rect', style='filled', fillcolor='lightgrey')
dot.node('Systemd Services', 'Systemd Services', shape='rect', style='filled', fillcolor='lightgrey')
dot.node('Udev Rules', 'Udev Rules', shape='rect', style='filled', fillcolor='lightgrey')

# Define edges for communication
dot.edge('Browser VM', 'CTAPHID Emulation', 'HID Interaction')
dot.edge('CTAPHID Emulation', 'Qrexec Transport', 'Request Forwarding')
dot.edge('Qrexec Transport', 'sys-usb VM', 'IPC Channel', dir='both')
dot.edge('sys-usb VM', 'CTAP Protocol Handlers', 'Protocol Handling')
dot.edge('CTAP Protocol Handlers', 'Policy Enforcement', 'Policy Check')
dot.edge('sys-usb VM', 'Systemd Services', 'Service Management')
dot.edge('sys-usb VM', 'Udev Rules', 'Device Configuration')

# Add legend
with dot.subgraph(name='cluster_legend') as c:
    c.attr(label='Legend')
    c.node('Client', 'Client', shape='rect', style='filled', fillcolor='lightblue')
    c.node('Server', 'Server', shape='rect', style='filled', fillcolor='lightgreen')
    c.node('Component', 'Component', shape='rect', style='filled', fillcolor='lightgrey')

# Render the diagram
dot.render('qubes_os_ctap_proxy_architecture', format='png', cleanup=True)