from JumpScale import j


class Actions(ActionsBaseMgmt):
    def install(self, service):
        print("Hello I'm running JS8 TESTS...")
        # ex =  service.executor
        # c  =  ex.cuisine
        host = service.hrd.getStr('host')
        mail_service = service.getProducers('mailclient')[0]
        email_sender = mail_service.actions.getSender(mail_service)
        executor = j.tools.executor.getSSHViaProxy(host)
        cuisine = executor.cuisine
        rc, out, err = cuisine.core.run(service.hrd.getStr('testcmd'))
        email_sender.send(service.hrd.getStr('sendto'),
                          mail_service.hrd.getStr("smtp.sender"),
                          "asdadad",
                          "OUT: %s, ERR: %s"%(out, err),
                          'html',
                          )


        #executor("cd /root/org_quality/Environment_testing/performance\ testing/ && jspython Testsuite/1_Network_config_test/1_Network_conf_test.py ")
