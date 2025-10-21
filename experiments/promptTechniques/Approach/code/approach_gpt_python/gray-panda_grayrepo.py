from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client
from diagrams.onprem.network import Internet
from diagrams.generic.os import Windows, Android
from diagrams.generic.firewall import Firewall
from diagrams.generic.compute import Rack as ELK

with Diagram("Flare-On CTF Architecture", show=False, direction="TB"):
    client = Client("User")

    with Cluster("Malware Analysis"):
        induct = Server("Induct (ELF Binary)")
        udp_script = Server("udpp.py")
        decrypt_script = Server("01_decrypt.py")

        induct - Edge(label="UDP/IRC") - udp_script
        induct >> decrypt_script

    with Cluster("SSHD Exploitation"):
        sshd = Server("sshd")
        liblzma = Server("liblzma")
        custom_vm = Server("Custom VM")
        server_script = Server("server.py")

        sshd - Edge(label="Exploit") - liblzma
        liblzma >> custom_vm
        server_script >> sshd

    with Cluster("Mobile Application Reverse Engineering"):
        android_app = Android("Android App")
        windows_app = Windows("Windows Mobile App")

        android_app - Edge(label="Gesture Handling") - windows_app

    with Cluster("Network"):
        internet = Internet("C2 Server")
        firewall = Firewall("Firewall")

        induct - Edge(label="C2 Communication") - internet
        internet >> firewall

    client >> induct
    client >> sshd
    client >> android_app
    client >> windows_app

    with Cluster("Cryptography"):
        elk = ELK("ECC & ChaCha20")

        elk << decrypt_script
        elk << server_script