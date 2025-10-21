from diagrams import Diagram, Cluster
from diagrams.generic.blank import Blank

with Diagram("Linux Command Tutorial Architecture", show=False):
    with Cluster("Documentation-as-Code"):
        readme = Blank("README.md")
        config = Blank("_config.yml")

        with Cluster("Linux Command Tutorials"):
            basic_commands = Blank("Basic-commands.md")
            filter_commands = Blank("filtercommands.md")
            file_permissions = Blank("filepermissions.md")
            signals_in_linux = Blank("signalsinlinux.md")
            top_command = Blank("topcommand.md")
            user_admin = Blank("useradmin.md")
            group_admin = Blank("groupadmin.md")
            ls_command = Blank("ls.md")
            grep_command = Blank("grep.md")
            find_command = Blank("findcommand.md")
            links_command = Blank("links.md")
            managing_process = Blank("managingprocess.md")
            vi_editor = Blank("vi.md")
            changing_ownership = Blank("changing-ownership-and-group.md")

        readme >> basic_commands
        readme >> filter_commands
        readme >> file_permissions
        readme >> signals_in_linux
        readme >> top_command
        readme >> user_admin
        readme >> group_admin
        readme >> ls_command
        readme >> grep_command
        readme >> find_command
        readme >> links_command
        readme >> managing_process
        readme >> vi_editor
        readme >> changing_ownership

    readme >> config