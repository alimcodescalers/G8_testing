import gevent
from gevent.subprocess import Popen, PIPE


def check_package(package):
    try:
        run_cmd_via_gevent('dpkg -l {}'.format(package))
        return True
    except RuntimeError:
        print("Dependant package {} is not installed".format(package))
        return False


def run_cmd_via_gevent(cmd):
    sub = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
    out, err = sub.communicate()
    if sub.returncode == 0:
        return out.decode('ascii')
    else:
        error_output = err.decode('ascii')
        raise RuntimeError("Failed to execute command.\n\ncommand:\n{}\n\n".format(cmd, error_output))


def wait_until_remote_is_listening(address, port):
    import socket
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((address, port))
            s.close()
            break
        except ConnectionAbortedError:
            gevent.sleep(1)
        except ConnectionRefusedError:
            gevent.sleep(1)
        except TimeoutError:
            gevent.sleep(1)
        s.close()


def check_remote_is_listening(address, port):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((address, port))
    finally:
        s.close()


def safe_get_vm(ovc, concurrency, machine_id):
    while True:
        try:
            if concurrency is None:
                return ovc.api.cloudapi.machines.get(machineId=machine_id)
            with concurrency:
                return ovc.api.cloudapi.machines.get(machineId=machine_id)
        except Exception as e:
            print("Failed to get vm details for machine {}".format(machine_id))
            gevent.sleep(2)
