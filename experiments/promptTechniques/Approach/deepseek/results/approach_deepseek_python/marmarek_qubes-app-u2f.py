from graphviz import Digraph

dot = Digraph(comment='Qubes OS CTAP Proxy Architecture')
dot.attr(rankdir='TB', splines='ortho')

with dot.subgraph(name='cluster_browser_vm') as c:
    c.attr(label='Browser VM', style='filled', color='lightgrey')
    c.node('hid_emu', 'CTAPHID Emulation\n(HID Device Emulator)', shape='box', style='filled', color='lightblue')
    c.node('client_comp', 'Client Components\n(CTAP Protocol Handlers)', shape='box', style='filled', color='lightblue')

with dot.subgraph(name='cluster_sys_usb_vm') as c:
    c.attr(label='sys-usb VM', style='filled', color='lightgrey')
    c.node('sys_usb_comp', 'sys-usb Components\n(USB Device Communication)', shape='box', style='filled', color='lightcoral')
    c.node('policy_enforce', 'Policy Enforcement', shape='box', style='filled', color='lightcoral')

dot.node('qrexec', 'Qrexec Transport\n(Secure IPC)', shape='ellipse', style='filled', color='lightgreen')
dot.node('config', 'Configuration Files\n(/etc/qubes, /usr/local/etc/qubes)', shape='note', style='filled', color='lightyellow')
dot.node('udev', 'Udev Rules\n(Device Permissions)', shape='note', style='filled', color='lightyellow')
dot.node('systemd', 'Systemd Services\n(Daemon Management)', shape='note', style='filled', color='lightyellow')

dot.edge('hid_emu', 'qrexec', label='CTAP Requests/Responses', dir='both')
dot.edge('client_comp', 'hid_emu', label='Protocol Handling', dir='both')
dot.edge('qrexec', 'sys_usb_comp', label='CTAP Forwarding', dir='both')
dot.edge('sys_usb_comp', 'policy_enforce', label='Access Control', dir='both')
dot.edge('config', 'client_comp', label='Protocol Settings', style='dashed')
dot.edge('config', 'sys_usb_comp', label='Debugging Config', style='dashed')
dot.edge('udev', 'hid_emu', label='Device Access', style='dashed')
dot.edge('systemd', 'hid_emu', label='Service Management', style='dashed')
dot.edge('systemd', 'sys_usb_comp', label='Service Management', style='dashed')

dot.render('qubes_ctap_proxy_architecture', format='png', cleanup=True)