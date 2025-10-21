# save this file as inspect_diagrams.py
import diagrams
import pkgutil
import inspect
import importlib

def generate_diagrams_import_map():
    """
    Inspects the `diagrams` package to find all public classes
    and their correct import paths.
    """
    package = diagrams
    class_map = {}

    # Recursively walk through all modules in the diagrams package
    for _, name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        try:
            # Dynamically import the module
            module = importlib.import_module(name)

            # Inspect the module for its members
            for member_name, member_obj in inspect.getmembers(module):
                # We want to find classes that are defined in this specific module
                # (not imported from another) and are public (don't start with '_').
                if (inspect.isclass(member_obj) and
                        member_obj.__module__ == name and
                        not member_name.startswith('_')):
                    
                    # Store the class name and its full module path
                    if member_name not in class_map:
                        class_map[member_name] = name
        except Exception:
            # Skip any modules that might fail to import
            pass
            
    return class_map

if __name__ == "__main__":
    print("🔍 Generating a reference of all available classes in the 'diagrams' package...")
    
    import_map = generate_diagrams_import_map()
    with open("diagrams_import_reference.txt", "w") as f:
        for class_name, module_path in sorted(import_map.items()):
            f.write(f"from {module_path} import {class_name}\n")
    print("\n# ========== Diagrams Import Reference (copy this into your prompt) ==========")
    # Sort the items for a clean, alphabetical list
    for class_name, module_path in sorted(import_map.items()):
        print(f"from {module_path} import {class_name}")
    print("# ==========================================================================\n")

    print(f"✅ Found {len(import_map)} classes. You can now provide this list to the LLM for context.")