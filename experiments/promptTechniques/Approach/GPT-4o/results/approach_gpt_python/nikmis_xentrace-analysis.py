from graphviz import Digraph

dot = Digraph(comment='Xen Performance Analysis Tool', format='png')

# Components
dot.node('Xentrace', 'Xentrace\nData Capture')
dot.node('Reader', 'Reader\nEvent Parsing')
dot.node('EventHandler', 'EventHandler\nEvent Handling')
dot.node('AnalysisTools', 'Analysis Tools\nAnalysis')
dot.node('CPUUtil', 'CPU Utilization\n(cpu_time_sharing)')
dot.node('SchedLatency', 'CPU Scheduling Latency\n(cpu_wait)')
dot.node('HypervisorTime', 'Time in Hypervisor\n(xen_dom_time_sharing)')
dot.node('DiskIO', 'Disk I/O\n(blk_io_queues)')
dot.node('XenStats', 'Xen Event Statistics\n(xen_stats)')
dot.node('TrapCount', 'Trap Counting\n(trap)')

# Connectors
dot.edge('Xentrace', 'Reader', label='Trace Data')
dot.edge('Reader', 'EventHandler', label='Parsed Events')
dot.edge('EventHandler', 'AnalysisTools', label='Invoke Handlers')
dot.edge('AnalysisTools', 'CPUUtil', label='Analysis')
dot.edge('AnalysisTools', 'SchedLatency', label='Analysis')
dot.edge('AnalysisTools', 'HypervisorTime', label='Analysis')
dot.edge('AnalysisTools', 'DiskIO', label='Analysis')
dot.edge('AnalysisTools', 'XenStats', label='Analysis')
dot.edge('AnalysisTools', 'TrapCount', label='Analysis')

# Render the diagram
dot.render('xen_performance_analysis_tool_diagram')