from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.generic.virtualization import Qemu, Virtualbox
from diagrams.generic.os import Windows, LinuxGeneral

with Diagram("hAFL2 Hypervisor Fuzzing Architecture", show=False, direction="TB"):
    with Cluster("Linux Host"):
        linux_host = LinuxGeneral("Linux Host")
        with Cluster("QEMU/KVM"):
            qemu = Qemu("QEMU")
            kvm = Virtualbox("KVM with Intel PT")
            
            with Cluster("Root Partition VM (L1)"):
                windows_root = Windows("Windows Root Partition")
                vmswitch = Server("vmswitch.sys")
                crash_monitor = Server("CrashMonitoringDriver.sys")
                
                with Cluster("Child Partition VM (L2)"):
                    windows_child = Windows("Windows Child Partition")
                    cpharness = Server("CPHarness.sys")
                    harness = Server("Fuzzing Harness")
    
    with Cluster("Fuzzing Control"):
        master = Server("Master")
        slave = Server("Slave")
        gui = Server("GUI")
        redqueen = Server("Redqueen")
        
    linux_host >> qemu
    qemu >> kvm
    kvm >> windows_root
    windows_root >> vmswitch
    windows_root >> crash_monitor
    windows_root >> windows_child
    windows_child >> cpharness
    cpharness >> harness
    
    master >> slave
    slave >> qemu
    gui >> master
    redqueen >> slave
    
    harness >> cpharness
    cpharness >> vmswitch
    crash_monitor >> kvm
    slave >> kvm