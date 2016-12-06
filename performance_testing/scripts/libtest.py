import gevent
from gevent.subprocess import Popen, PIPE
import configparser
import uuid
import logging
import logging.handlers

FORMAT = '%(asctime)-15s %(name)s %(levelname)s: %(message)s'


def get_logger(name):
    log = logging.getLogger(name)
    handler = logging.handlers.RotatingFileHandler(filename='/var/log/perftest-%s.log' % name)
    handler.setFormatter(logging.Formatter(FORMAT))
    log.addHandler(handler)

    return log


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
        return out.decode('utf-8')
    else:
        error_output = err.decode('utf-8')
        raise RuntimeError("Failed to execute command.\n\ncommand:\n{}\n\n{}".format(cmd, error_output))


def wait_until_remote_is_listening(address, port, report_failure=False, machine_name='unknown'):
    import socket
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((address, port))
            s.close()
            break
        except (OSError, ConnectionAbortedError, ConnectionRefusedError, TimeoutError):
            if report_failure:
                print("Waiting for machine {} to accept connections on {}:{}".format(machine_name, address, port))
            gevent.sleep(1)
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


def push_results_to_repo(res_dir, location):
    from JumpScale import j
    config = configparser.ConfigParser()
    config.read("locations.cfg")
    if location not in config.options('locations'):
        raise AssertionError('Please update the locations.cfg with your '
                             'location:environment_repo to be able to '
                             'push your results')
    repo = config.get("locations", location)
    repo_dir = '/tmp/' + str(uuid.uuid4()) + '/'
    res_folder_name = res_dir.split('/')[-1]
    j.do.execute('mkdir -p %s' % repo_dir)
    j.do.execute('cd %s; git clone %s' % (repo_dir, repo))
    repo_path = j.do.listDirsInDir(repo_dir)[0]
    repo_result_dir = repo_path + '/testresults/'
    j.do.execute('mkdir -p %s' % repo_result_dir)
    j.do.execute('cp -rf %s %s' % (res_dir, repo_result_dir))
    j.do.chdir(repo_result_dir + res_folder_name)
    j.do.execute('git add *.csv ')
    j.do.execute("git commit -a -m 'Pushing new results' ")
    j.do.execute('git push')
