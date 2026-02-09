from diagrams import Diagram
from diagrams.programming.language import TypeScript
from diagrams.generic.blank import Blank
from diagrams.custom import Custom

with Diagram("Visual Programming Environment Architecture", show=False, direction="TB"):
    syntax_representation = TypeScript("Syntax Representation")
    
    element_api = Custom("Element API", "./custom/element.png")
    specification = Custom("Specification", "./custom/specification.png")
    warehouse = Custom("Warehouse", "./custom/warehouse.png")
    syntax_tree = Custom("Syntax Tree", "./custom/tree.png")
    
    execution_engine = TypeScript("Execution Engine")
    
    symbol_table = Custom("Symbol Table", "./custom/table.png")
    parser = Custom("Parser", "./custom/parser.png")
    interpreter = Custom("Interpreter", "./custom/interpreter.png")
    scheduler = Custom("Scheduler", "./custom/scheduler.png")
    
    library = TypeScript("Library")
    
    values = Custom("Values", "./custom/values.png")
    boxes = Custom("Boxes", "./custom/box.png")
    math_ops = Custom("Math Operators", "./custom/math.png")
    conditionals = Custom("Conditionals", "./custom/conditional.png")
    loops = Custom("Loops", "./custom/loop.png")
    program_structures = Custom("Program Structures", "./custom/program.png")
    miscellaneous = Custom("Miscellaneous", "./custom/misc.png")
    
    syntax_representation >> [element_api, specification, warehouse, syntax_tree]
    execution_engine >> [symbol_table, parser, interpreter, scheduler]
    library >> [values, boxes, math_ops, conditionals, loops, program_structures, miscellaneous]
    
    syntax_tree >> parser
    parser >> interpreter
    symbol_table >> interpreter
    interpreter >> scheduler