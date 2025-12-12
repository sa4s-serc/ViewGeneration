import graphviz

dot = graphviz.Digraph(comment='TypeScript Flag Upgrade Tool Architecture')
dot.attr(rankdir='TB', size='8,10')

with dot.subgraph(name='cluster_runner') as c:
    c.attr(label='Runner (Orchestrator)', style='filled', color='lightgrey')
    c.node('runner', 'Runner', shape='ellipse', style='filled', fillcolor='white')

with dot.subgraph(name='cluster_core') as c:
    c.attr(label='Core Components', style='filled', color='lightblue')
    c.node('index', 'index.ts\nCLI Entry Point')
    c.node('runner_file', 'runner.ts\nOrchestrator')
    c.node('parser', 'parser.ts\nProject Parser')
    c.node('types', 'types.ts\nShared Types')

with dot.subgraph(name='cluster_manipulators') as c:
    c.attr(label='Manipulators (Strategy Pattern)', style='filled', color='lightgreen')
    c.node('no_implicit_returns', 'no_implicit_returns_manipulator.ts')
    c.node('strict_null_checks', 'strict_null_checks_manipulator.ts')
    c.node('strict_property_init', 'strict_property_initialization_manipulator.ts')
    c.node('no_implicit_any', 'no_implicit_any_manipulator.ts')

with dot.subgraph(name='cluster_error_detectors') as c:
    c.attr(label='Error Detectors', style='filled', color='orange')
    c.node('error_detector_base', 'error_detector.ts\nBase Class')
    c.node('prod_error_detector', 'prod_error_detector.ts\nProduction Detector')

with dot.subgraph(name='cluster_emitters') as c:
    c.attr(label='Emitters', style='filled', color='yellow')
    c.node('in_place_emitter', 'in_place_emitter.ts')
    c.node('out_of_place_emitter', 'out_of_place_emitter.ts')

with dot.subgraph(name='cluster_loggers') as c:
    c.attr(label='Loggers', style='filled', color='pink')
    c.node('console_logger', 'console_logger.ts')
    c.node('stub_logger', 'stub_logger.ts')

with dot.subgraph(name='cluster_utils') as c:
    c.attr(label='Utilities', style='filled', color='lightcyan')
    c.node('util', 'util/\nUtility Functions')

with dot.subgraph(name='cluster_tests') as c:
    c.attr(label='Tests', style='filled', color='lavender')
    c.node('tests', 'test/**/*_test.ts')

dot.edge('index', 'runner_file')
dot.edge('runner_file', 'parser')
dot.edge('runner_file', 'error_detector_base')
dot.edge('runner_file', 'in_place_emitter')
dot.edge('runner_file', 'console_logger')
dot.edge('runner_file', 'util')

dot.edge('error_detector_base', 'prod_error_detector')
dot.edge('prod_error_detector', 'no_implicit_returns')
dot.edge('prod_error_detector', 'strict_null_checks')
dot.edge('prod_error_detector', 'strict_property_init')
dot.edge('prod_error_detector', 'no_implicit_any')

dot.edge('no_implicit_returns', 'in_place_emitter')
dot.edge('strict_null_checks', 'in_place_emitter')
dot.edge('strict_property_init', 'in_place_emitter')
dot.edge('no_implicit_any', 'in_place_emitter')

dot.edge('in_place_emitter', 'console_logger')
dot.edge('out_of_place_emitter', 'console_logger')

dot.edge('tests', 'runner_file', style='dashed')
dot.edge('tests', 'parser', style='dashed')
dot.edge('tests', 'no_implicit_returns', style='dashed')
dot.edge('tests', 'strict_null_checks', style='dashed')
dot.edge('tests', 'prod_error_detector', style='dashed')

dot.render('typescript_flag_upgrade_architecture', format='png', cleanup=True)