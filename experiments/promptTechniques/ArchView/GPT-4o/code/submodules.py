import pkgutil
import diagrams

for mod in pkgutil.iter_modules(diagrams.__path__):
    print(mod.name)
