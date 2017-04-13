from termcolor import colored
from install_testing_nodes.src.ExecuteRemoteCommands import ExecuteRemoteCommands

JUMPSACLE_BRANCH = "8.2.0"
GRID_API_BRANCH = "1.1.0-alpha"
AYS_TEMPLATE_BRANCH = "1.1.0-alpha"

if __name__ == '__main__':
    executer = ExecuteRemoteCommands()
    print(colored(' [*] STEP 1 : create account', 'yellow'))
    executer.create_account()
    print(colored(' [*] STEP 2 : create cloud space', 'yellow'))
    executer.create_cloudspace()

    # g8os node
    print(colored(' [*] STEP 3 : create g8os node', 'yellow'))
    executer.create_virtualmachine()
    executer.create_port_forward(publicPorts={22: 2200, 6379: 6379})
    executer.connect_to_virtual_machine(port=2200)
    executer.update_machine()
    executer.install_docker()
    executer.install_g8os()
    executer.get_virtualmachine_ip()
    executer.g8os_ip_list.append([executer.virtualmachine['ip'], 'dockerG8os'])

    # AYS server vm
    print(colored(' [*] STEP 4 : create AYS server node', 'yellow'))
    executer.create_virtualmachine()
    executer.create_port_forward(publicPorts={22: 2201, 5000: 5000})
    executer.connect_to_virtual_machine(port=2201)
    executer.update_machine()
    import ipdb; ipdb.set_trace()
    executer.install_jumpscale(branch=JUMPSACLE_BRANCH)
    executer.install_g8core_python_client()
    executer.start_AYS_server()
    executer.clone_ays_templates(branch=AYS_TEMPLATE_BRANCH)
    executer.discover_g8os_nodes()
    executer.get_virtualmachine_ip()
    ays_server_ip = executer.virtualmachine['ip']

    # grid API node
    print(colored(' [*] STEP 5 : create grid API server', 'yellow'))
    executer.create_virtualmachine()
    executer.create_port_forward(publicPorts={22: 2202, 8080: 8080})
    executer.connect_to_virtual_machine(port=2202)
    executer.update_machine()
    executer.install_go()
    executer.start_API_server(API_branch=GRID_API_BRANCH,
                               ays_server_ip=ays_server_ip)
    executer.get_virtualmachine_ip()

