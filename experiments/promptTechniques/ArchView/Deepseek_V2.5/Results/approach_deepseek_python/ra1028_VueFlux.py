from diagrams import Diagram
from diagrams.programming.flowchart import Action, Display, Document, InputOutput, StartEnd
from diagrams.generic.blank import Blank

with Diagram("VueFlux Architecture", show=False, direction="LR"):
    ui = Display("UI Components")
    actions = Action("Actions")
    mutations = Action("Mutations")
    state = Document("State")
    computed = Document("Computed")
    store = StartEnd("Store")
    variable = InputOutput("Variable")
    constant = InputOutput("Constant")
    signal = InputOutput("Signal")
    binder = InputOutput("Binder")
    executor = InputOutput("Executor")
    reactive = Blank("VueFluxReactive")
    core = Blank("VueFlux")

    core >> store
    reactive >> variable
    reactive >> constant
    reactive >> signal
    reactive >> binder
    store >> state
    store >> mutations
    store >> actions
    store >> computed
    actions >> mutations
    mutations >> state
    state >> computed
    computed >> ui
    signal >> binder
    binder >> ui
    executor >> actions