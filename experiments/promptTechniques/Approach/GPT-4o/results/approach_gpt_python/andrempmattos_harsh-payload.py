from diagrams import Diagram, Cluster, Node
from diagrams.generic.os import Windows
from diagrams.generic.device import Tablet

with Diagram("HARSH Payload Architecture", show=False):
    with Cluster("FPGA-Based System-on-Chip"):
        microsemi_fpga = Node("Microsemi SmartFusion2 FPGA")

        with Cluster("Software/Firmware Components"):
            freertos = Node("FreeRTOS")
            drivers = Node("Peripheral Drivers")
            system_services = Node("System Services Driver")
            experiment_algorithms = Node("Experiment Algorithms")
            obc_communication = Node("OBC Communication (FSP)")
            raspberry_pi_wrapper = Node("Raspberry Pi Software Wrapper")

            freertos >> drivers
            drivers >> system_services
            system_services >> experiment_algorithms
            experiment_algorithms >> obc_communication
            raspberry_pi_wrapper >> drivers

        with Cluster("Hardware Components and Architecture"):
            fpga_fabric = Node("FPGA Fabric")
            axi_ahb_interconnect = Node("AXI/AHB Interconnect")
            memory_subsystem = Node("Memory Subsystem")
            clocking_reset = Node("Clocking and Reset")
            peripheral_interfaces = Node("Peripheral Interfaces")
            power_management = Node("Power Management")

            fpga_fabric >> axi_ahb_interconnect
            axi_ahb_interconnect >> memory_subsystem
            memory_subsystem >> clocking_reset
            clocking_reset >> peripheral_interfaces
            peripheral_interfaces >> power_management

    microsemi_fpga >> [freertos, drivers, system_services, experiment_algorithms, obc_communication, raspberry_pi_wrapper]
    microsemi_fpga >> [fpga_fabric, axi_ahb_interconnect, memory_subsystem, clocking_reset, peripheral_interfaces, power_management]

    with Cluster("Design Patterns"):
        hierarchical_design = Node("Hierarchical Design")
        bus_based_architecture = Node("Bus-Based Architecture")
        data_driven_design = Node("Data-Driven Design")
        component_based_design = Node("Component-Based Design")
        configuration_driven_design = Node("Configuration-Driven Design")
        constraint_driven_design = Node("Constraint-Driven Design")
        hardware_abstraction_layer = Node("Hardware Abstraction Layer")
        gated_logic = Node("Gated Logic")

        hierarchical_design >> bus_based_architecture
        bus_based_architecture >> data_driven_design
        data_driven_design >> component_based_design
        component_based_design >> configuration_driven_design
        configuration_driven_design >> constraint_driven_design
        constraint_driven_design >> hardware_abstraction_layer
        hardware_abstraction_layer >> gated_logic

    with Cluster("Synthesis and Implementation"):
        logic_synthesis = Node("Logic Synthesis")
        bfm_simulation = Node("BFM Driven Simulation")
        resource_utilization = Node("Resource Utilization")
        timing_constraints = Node("Timing Constraints")

        logic_synthesis >> bfm_simulation
        bfm_simulation >> resource_utilization
        resource_utilization >> timing_constraints

    with Cluster("Key Concerns and Potential Issues"):
        unused_signals = Node("Unused Signals")
        timing_violations = Node("Timing Violations")
        simulation_mismatches = Node("Simulation Mismatches")

        unused_signals >> timing_violations
        timing_violations >> simulation_mismatches