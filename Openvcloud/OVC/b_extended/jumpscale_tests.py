from JumpScale import j
from Openvcloud.utils.utils import BaseTest


class JumpscaleTests(BaseTest):

    def test001_jumpscale_debug(self):
        # if we want to change debug value:
        # hrd = j.core.hrd.get('/opt/jumpscale7/hrd/system/system.hrd'); hrd.set('debug','0')

        j.application.start('jsshell')
        self.assertEqual(j.application.debug, False)
