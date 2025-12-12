from diagrams import Diagram
from diagrams.generic.blank import Blank
from diagrams.programming.language import Go
from diagrams.onprem.network import Apache
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git

with Diagram("Software Architecture View", show=False, direction="TB"):
    with Diagram("Text Processing Layer"):
        text_processing = Go("golang.org/x/text")
        unicode_norm = Go("Unicode\nNormalization")
        collation = Go("Collation")
        bidi = Go("BiDi Text\nHandling")
        idna = Go("IDNA")
        case_conv = Go("Case\nConversion")
        encoding = Go("Character\nEncoding")
        
        text_processing >> unicode_norm
        text_processing >> collation
        text_processing >> bidi
        text_processing >> idna
        text_processing >> case_conv
        text_processing >> encoding

    with Diagram("System Interaction Layer"):
        system_interaction = Go("golang.org/x/sys")
        os_abstraction = Go("OS\nAbstraction")
        syscalls = Go("System\nCalls")
        windows_api = Go("Windows\nAPI")
        linux_api = Go("Linux\nAPI")
        
        system_interaction >> os_abstraction
        system_interaction >> syscalls
        system_interaction >> windows_api
        system_interaction >> linux_api

    with Diagram("CLI Layer"):
        cli_framework = Go("github.com/spf13/cobra")
        hierarchical_cmds = Go("Hierarchical\nCommands")
        args_flags = Go("Arguments &\nFlags")
        cli_generator = Go("CLI\nGenerator")
        
        cli_framework >> hierarchical_cmds
        cli_framework >> args_flags
        cli_framework >> cli_generator

    with Diagram("Core Components"):
        ebpf = Go("eBPF\nInteraction")
        yaml = Go("YAML\nProcessing")
        caching = Go("Caching\n(LRU)")
        fs_watch = Go("File System\nWatching")
        text_funcs = Go("Text\nProcessing")
        cmd_interaction = Go("Command Line\nInteraction")
        
    # Cross-layer relationships
    text_processing >> cli_framework
    system_interaction >> cli_framework
    text_processing >> ebpf
    system_interaction >> ebpf
    
    # Infrastructure components
    with Diagram("Infrastructure"):
        monitoring = Grafana("Monitoring")
        metrics = Prometheus("Metrics")
        ci_cd = Jenkins("CI/CD")
        container = Docker("Container\nRuntime")
        vcs = Git("Version\nControl")
        
        monitoring << metrics
        ci_cd >> container
        vcs >> ci_cd