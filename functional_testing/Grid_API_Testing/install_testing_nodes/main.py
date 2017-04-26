from termcolor import colored
from random import randint
from install_testing_nodes.src.ExecuteRemoteCommands import ExecuteRemoteCommands
from install_testing_nodes.src.install_g8os_on_packet import InstallG8OSOnPacket

JUMPSACLE_BRANCH = "8.2.0"
AYS_TEMPLATE_BRANCH = "1.1.0-alpha"
GRID_API_BRANCH = "1.1.0-alpha"
G8CORE_CLIENT = "1.1.0-alpha"
G8OS_IMAGE = 'https://bootstrap.gig.tech/ipxe/1.1.0-alpha/%s/console=ttyS1,115200n8'
MACHINE_NAME = 'Test-xtremx-0%i' % randint(1, 100)
AUTO_DISCOVERING = True


if __name__ == '__main__':
    install_g8os_on_packet = InstallG8OSOnPacket()
    print(colored(' [*] STEP 1 : Install g8os in packet, image: %s' % G8OS_IMAGE, 'yellow'))
    install_g8os_on_packet.login()
    install_g8os_on_packet.ctreate_new_machine(machine_name=MACHINE_NAME,
                                               image=G8OS_IMAGE)

    executer = ExecuteRemoteCommands()
    print(colored(' [*] STEP 2 : create account', 'yellow'))
    executer.create_account()
    print(colored(' [*] STEP 3 : create cloud space', 'yellow'))
    executer.create_cloudspace()

    if not AUTO_DISCOVERING:
        MACHINE_IP = install_g8os_on_packet.get_packt_machine_ip(machine_name=MACHINE_NAME)
        MACHINE_MAC = install_g8os_on_packet.get_packet_machine_mac(ip=MACHINE_IP)
        executer.update_g8os_valuse(MACHINE_IP, MACHINE_MAC)

    install_g8os_on_packet.driver_quit()
    # # g8os node
    # print(colored(' [*] STEP 3 : create g8os node', 'yellow'))
    # executer.create_virtualmachine()
    # executer.create_port_forward(publicPorts={22: 2200, 6379: 6379})
    # executer.connect_to_virtual_machine(port=2200)
    # executer.update_machine()
    # executer.install_docker()
    # executer.install_g8os()
    # executer.get_virtualmachine_ip()
    # executer.g8os_ip_list.append([executer.virtualmachine['ip'], 'dockerG8os'])

    # AYS server vm
    print(colored(' [*] STEP 4 : create AYS server node', 'yellow'))
    executer.create_virtualmachine()
    executer.create_port_forward(publicPorts={22: 2201, 5000: 5000})
    executer.connect_to_virtual_machine(port=2201)
    executer.update_machine()
    executer.install_zerotire()
    executer.add_node_to_zerotire_nw()
    executer.install_jumpscale(branch=JUMPSACLE_BRANCH)
    executer.install_g8core_python_client(branch=G8CORE_CLIENT)
    executer.start_AYS_server()
    executer.clone_ays_templates(branch=AYS_TEMPLATE_BRANCH)
    executer.discover_g8os_nodes(auto_discovering=True)
    executer.get_virtualmachine_ip()
    ays_server_ip = executer.virtualmachine['ip']

    # grid API node
    print(colored(' [*] STEP 5 : create grid API server', 'yellow'))
    executer.create_virtualmachine()
    executer.create_port_forward(publicPorts={22: 2202, 8080: 8080})
    executer.connect_to_virtual_machine(port=2202)
    executer.update_machine()
    executer.install_zerotire()
    executer.add_node_to_zerotire_nw()
    executer.install_go()
    executer.start_API_server(API_branch=GRID_API_BRANCH,
                              ays_server_ip=ays_server_ip)
    executer.get_virtualmachine_ip()

