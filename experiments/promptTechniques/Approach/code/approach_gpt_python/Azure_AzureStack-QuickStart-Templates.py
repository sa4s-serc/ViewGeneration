from diagrams import Diagram, Cluster, Edge
from diagrams.azure.network import VirtualNetworks, LoadBalancers, VirtualNetworkGateways
from diagrams.azure.compute import VirtualMachines
from diagrams.azure.identity import KeyVault
from diagrams.azure.general import ResourceGroups
from diagrams.azure.devops import Repos
from diagrams.custom import Custom

with Diagram("AzureStack-QuickStart-Templates Architecture", show=False):
    with Cluster("Azure Environment"):
        azure_group = ResourceGroups("Resource Group")
        
        with Cluster("Networking"):
            vnet = VirtualNetworks("Virtual Network")
            lb = LoadBalancers("Load Balancer")
            vpn = VirtualNetworkGateways("VPN Gateway")
        
        with Cluster("Compute Resources"):
            vm1 = VirtualMachines("VM Instance 1")
            vm2 = VirtualMachines("VM Instance 2")
        
        with Cluster("Security"):
            keyvault = KeyVault("Key Vault")
        
        azure_group >> Edge(label="Contains") >> [vnet, lb, vpn, vm1, vm2, keyvault]
        lb >> Edge(label="Distributes Traffic") >> [vm1, vm2]
        vpn >> Edge(label="Secure Connection") >> Custom("ConsortiumBridge", "./icons/consortiumbridge.png")
        keyvault >> Edge(label="Stores Secrets") >> vm1

    with Cluster("Azure Stack Environment"):
        stack_group = ResourceGroups("Resource Group")
        
        with Cluster("Networking"):
            stack_vnet = VirtualNetworks("Virtual Network")
            stack_lb = LoadBalancers("Load Balancer")
        
        with Cluster("Compute Resources"):
            stack_vm1 = VirtualMachines("VM Instance 1")
            stack_vm2 = VirtualMachines("VM Instance 2")
        
        with Cluster("Security"):
            stack_keyvault = KeyVault("Key Vault")
        
        stack_group >> Edge(label="Contains") >> [stack_vnet, stack_lb, stack_vm1, stack_vm2, stack_keyvault]
        stack_lb >> Edge(label="Distributes Traffic") >> [stack_vm1, stack_vm2]
        stack_keyvault >> Edge(label="Stores Secrets") >> stack_vm1

    with Cluster("Repository"):
        repo = Repos("AzureStack-QuickStart-Templates")
    
    repo >> Edge(label="Deploys") >> [azure_group, stack_group]