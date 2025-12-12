import graphviz

# Create directed graph
g = graphviz.Digraph('Qubes_CTAP_Architecture', engine='dot')
g.attr(rankdir='TB', splines='ortho')

# Define styles
g.attr('node', shape='rectangle', style='rounded,filled', fillcolor='lightgrey')
g.attr('edge', arrowhead='normal')

# Create Browser VM cluster
with g.subgraph(name='cluster_browser') as browser:
    browser.attr(label='Browser VM', style='rounded,filled', fillcolor='lightblue')
    browser.node('browser', 'Web Browser')
    browser.node('ctap_client', 'CTAP Client')
    browser.node('hid_emu', 'HID Emulation')
    browser.edge('browser', 'ctap_client')
    browser.edge('ctap_client', 'hid_emu')

# Create sys-usb VM cluster 
with g.subgraph(name='cluster_sysusb') as sysusb:
    sysusb.attr(label='sys-usb VM', style='rounded,filled', fillcolor='lightgreen')
    sysusb.node('ctap_server', 'CTAP Server')
    sysusb.node('usb_stack', 'USB Stack')
    sysusb.node('token', 'Physical CTAP Token')
    sysusb.edge('ctap_server', 'usb_stack')
    sysusb.edge('usb_stack', 'token')

# Create qrexec service
g.node('qrexec', 'Qrexec Service\n(Secure IPC)', shape='diamond', style='filled', fillcolor='orange')

# Add connections between VMs through qrexec
g.edge('hid_emu', 'qrexec')
g.edge('qrexec', 'ctap_server')

# Add title
g.attr(label='\nQubes OS CTAP Proxy Architecture\nSecure CTAP authentication between isolated VMs', labelloc='t', fontsize='16')

# Save the diagram
g.render('qubes_ctap_architecture', format='png', cleanup=True)