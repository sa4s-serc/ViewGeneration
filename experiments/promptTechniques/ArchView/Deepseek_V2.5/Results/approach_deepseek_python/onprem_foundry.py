import graphviz

dot = graphviz.Digraph(comment='Foundry Architecture')
dot.attr(rankdir='TB', size='8,8')

with dot.subgraph(name='cluster_foundry') as foundry:
    foundry.attr(label='Foundry System', style='filled', color='lightgrey')
    
    with foundry.subgraph(name='cluster_furnace') as furnace:
        furnace.attr(label='Furnace', style='filled', color='white')
        
        furnace.node('grpc', 'gRPC Interface', shape='ellipse', style='filled', color='lightblue')
        furnace.node('pkg_map', 'Package Map\n(pkgMap)', shape='box', style='filled', color='lightyellow')
        furnace.node('build_queue', 'Build Queue', shape='box', style='filled', color='lightyellow')
        furnace.node('scheduler', 'Scheduler', shape='box', style='filled', color='lightyellow')
        furnace.node('worker_pool', 'Worker Pool', shape='box', style='filled', color='lightyellow')
        
        furnace.node('builder_interface', 'Builder Interface', shape='ellipse', style='filled', color='lightblue')
        furnace.node('makepkg_builder', 'MakepkgBuilder', shape='box', style='filled', color='lightgreen')
        furnace.node('builder_metrics', 'BuilderWithMetrics', shape='box', style='filled', color='lightgreen')
        furnace.node('noop_builder', 'NoOpBuilder', shape='box', style='filled', color='lightgreen')
        
        furnace.node('metrics', 'Metrics (Prometheus)', shape='box', style='filled', color='orange')
        furnace.node('health', 'Health Checks', shape='box', style='filled', color='orange')
        furnace.node('profiling', 'Profiling (pprof)', shape='box', style='filled', color='orange')

dot.node('aur', 'Arch User Repository (AUR)', shape='cylinder', style='filled', color='pink')
dot.node('object_storage', 'Object Storage', shape='cylinder', style='filled', color='pink')
dot.node('clients', 'gRPC Clients', shape='box', style='filled', color='lightblue')

dot.edge('clients', 'grpc', label='Build Requests\nQueue Status', style='dashed')
dot.edge('grpc', 'pkg_map', label='Package State\nManagement')
dot.edge('grpc', 'build_queue', label='Queue Builds')
dot.edge('build_queue', 'scheduler', label='Asynchronous\nProcessing')
dot.edge('scheduler', 'worker_pool', label='Parallel\nExecution')
dot.edge('worker_pool', 'builder_interface', label='Build Strategy')
dot.edge('builder_interface', 'makepkg_builder', label='Implementation')
dot.edge('builder_interface', 'noop_builder', label='Implementation')
dot.edge('makepkg_builder', 'builder_metrics', label='Decorated')
dot.edge('worker_pool', 'aur', label='Retrieve\nPackage Info')
dot.edge('worker_pool', 'object_storage', label='Upload\nBuilt Packages')
dot.edge('builder_interface', 'metrics', label='Instrumentation')
dot.edge('furnace', 'health', label='Internal\nMonitoring')
dot.edge('furnace', 'profiling', label='Performance\nAnalysis')

dot.attr(label='Foundry: Arch Linux Package Building System\nMicroservices Architecture with gRPC and Asynchronous Processing')
dot.attr(fontsize='20')

dot.render('foundry_architecture', format='png', cleanup=True)