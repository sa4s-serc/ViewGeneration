from graphviz import Digraph

dot = Digraph(comment='CodeMirror and ComPar Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='filled', fillcolor='lightblue')

# Core Components
dot.node('core', 'Core Editor\n- Text editing\n- Syntax highlighting\n- Indentation\n- Code folding')

# Language Modes
dot.node('modes', 'Language Modes\n- JavaScript\n- HTML/CSS\n- Python\n- SQL\n- XML')

# Keymaps
dot.node('keymaps', 'Keymaps\n- Vim\n- Emacs\n- Sublime')

# Addons
dot.node('addons', 'Addons\n- Auto-completion\n- Linting\n- Search\n- Merge')

# ComPar Components
dot.node('compar_gui', 'ComPar GUI\n- HTML/CSS\n- Jinja2\n- CodeMirror integration')

dot.node('compiler', 'Compiler Abstraction\n- GCC\n- ICC\n- Cetus\n- Autopar')

dot.node('parallel', 'Parallelization\n- OpenMP\n- Parameter combinations\n- Code instrumentation')

dot.node('execution', 'Execution\n- Slurm integration\n- Runtime analysis\n- Output validation')

# Relationships
dot.edge('core', 'modes')
dot.edge('core', 'keymaps')
dot.edge('core', 'addons')
dot.edge('compar_gui', 'core')
dot.edge('compar_gui', 'compiler')
dot.edge('compiler', 'parallel')
dot.edge('parallel', 'execution')

print(dot.source)
dot.render('architecture_diagram', view=True, format='png')