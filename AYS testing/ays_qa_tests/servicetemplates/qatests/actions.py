
from JumpScale import j

class Actions(ActionsBaseMgmt):
    def install(self, service):

        print("Hello I'm running performance Tests...")
        host = service.hrd.getStr('host')
        cmd = service.hrd.getStr('testcmd')

        executer = j.tools.executor.getSSHViaProxy(host)
        connection=executer.cuisine

        a = connection.core.run("cd; ls")[1].find('org_quality')
        if a < 0:
            connection.core.run("cd; git clone https://js-awesomo:jsR00t3r@github.com/gig-projects/org_quality.git")

        connection.core.run(cmd)



