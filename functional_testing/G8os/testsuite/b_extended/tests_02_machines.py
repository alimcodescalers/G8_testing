# from utils.utils import BaseTest
# import time
# import unittest
# import uuid

# class Machinetests(BaseTest):
#
#     def setUp(self):
#         super(Machinetests, self).setUp()
#         self.check_g8os_connection(Machinetests)
#
#     def test001_create_KVM_with_nbd_server(self):
#         """ g8os-008
#
#         *Test case for testing creating, listing and destroying VMs*
#
#         **Test Scenario:**
#
#         #. Check that system support hardware virtualization
#         #. Connect to nbd_server and check that image exist
#         #. Create virtual machine (VM1) with nbd_server, should succeed
#
#     def test002_check_vm_after_creation(self):
#         """ g8os-008
#
#         *Test case for testing main specs for vm after creation *
#
#         **Test Scenario:**
#
#         #. Check that system support hardware virtualization
#         #. Create virtual machine (VM1) , should succeed
#         #. ssh created vm ,should succeed
#         #. check vm image
#         #. check that can do basic comments through it
