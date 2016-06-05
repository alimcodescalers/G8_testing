#!/usr/local/bin/jspython

from JumpScale import j
import ConfigParser
import time
from optparse import OptionParser
import re
import sys

parser = OptionParser()
parser.add_option('--clean', help='clean environment', dest='clean', default=False, action='store_true')
(options, args) = parser.parse_args()

ccl = j.clients.osis.getNamespace('cloudbroker')
pcl = j.clients.portal.getByInstance('main')
scl = j.clients.osis.getNamespace('system')


def delete_accounts(accounts):
    for account in accounts:
        if account['name'] not in ['test_storage', 'gig'] :
            print('   |--Deleting account: %s' % account['name'])
            pcl.actors.cloudbroker.account.delete(account['id'], reason='testing')
            for _ in xrange(600):
                if account['status'] == 'DESTROYED':
                    break
                account = ccl.account.search({'name': '%s' % account['name'], 'id': account['id']})[1]
                time.sleep(1)
users_list=[]
if options.clean:
    # if accounts with no users have been found make sure to delete them
    Nouser_accounts = ccl.account.search({'status': 'CONFIRMED', 'acl.userGroupId': ''})[1:]
    if Nouser_accounts:
        delete_accounts(Nouser_accounts)
    hanging_accounts = ccl.account.search({'status': 'DESTROYING'})[1:]
    if hanging_accounts:
        delete_accounts(hanging_accounts)
    if Nouser_accounts:
        delete_accounts(Nouser_accounts)
    list = scl.user.list()
    for user in list:
        match = re.search('_([\S]+)', user)
        users_list.append(match.group(1))
elif len(sys.argv) == 2 and sys.argv[1]!= '--clean':
    USERNAME = sys.argv[1]
    users_list.append(USERNAME)
else:
    config = ConfigParser.ConfigParser()
    config.read("Perf_parameters.cfg")
    USERNAME = config.get("perf_parameters", "username")
    users_list.append(USERNAME)
print('Start tearing Down...')

for user in users_list:
    user_accounts = ccl.account.search({'status': 'CONFIRMED', 'acl.userGroupId': user})[1:]
    if user_accounts:
        print('  Deleting accounts for user: %s' %user)
        delete_accounts(user_accounts)
    if user not in ['gig','admin']:
        print('  Deleting user: %s' %user)
        scl.user.delete(user)

print('Tearing Down is done')







