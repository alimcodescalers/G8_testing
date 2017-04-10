from termcolor import colored
from src.ExecuteRemoteCommands import ExecuteRemoteCommands

if __name__ == '__main__':
    executer = ExecuteRemoteCommands()
    # import ipdb; ipdb.set_trace()
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
    g8os_ip = executer.virtualmachine['ip']

    # AYS server vm
    print(colored(' [*] STEP 4 : create AYS server node', 'yellow'))
    executer.create_virtualmachine()
    executer.create_port_forward(publicPorts={22: 2201, 5000: 5000})
    executer.connect_to_virtual_machine(port=2201)
    executer.update_machine()
    executer.install_jumpscale(branch='8.2.0')
    executer.install_g8core_python_client(branch='0.12.0')
    executer.start_AYS_server()
    executer.clone_ays_templates(branch='0.2.0')
    executer.discover_g8os_nodes(g8os_ip=g8os_ip)
    executer.get_virtualmachine_ip()
    ays_server_ip = executer.virtualmachine['ip']

    # grid API node
    print(colored(' [*] STEP 5 : create grid API server', 'yellow'))
    executer.create_virtualmachine()
    executer.create_port_forward(publicPorts={22: 2202, 8080: 8080})
    executer.connect_to_virtual_machine(port=2202)
    executer.update_machine()
    executer.install_go()
    executer.start_API_server(API_branch='nodes-api',
                               ays_server_ip=ays_server_ip)
    executer.get_virtualmachine_ip()

