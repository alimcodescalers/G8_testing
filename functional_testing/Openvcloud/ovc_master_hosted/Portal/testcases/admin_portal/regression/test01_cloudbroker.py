from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework

class AccountsTests(Framework):
    def setUp(self):
        super(AccountsTests, self).setUp()
        self.Login.Login()
        self.lg('Create new username, user:%s password:%s' % (self.username, self.password))
        self.Users.create_new_user(self.username, self.password, self.email, self.group)

    def test01_add_account_with_decimal_limitations(self):
        """ PRTL-026
        *Test case to make sure that creating account with decimal limitations working as expected*

        **Test Scenario:**
        #. create account with decimal limitations.
        #. search for it and verify it should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('create new account %s with decimal limitations' % self.account)
        max_memory = '3.5'
        self.Accounts.create_new_account(self.account, self.username, max_memory=max_memory)
        self.Accounts.open_account_page(self.account)
        account_maxmemory = self.get_text("account_page_maxmemory")
        self.assertTrue(account_maxmemory.startswith(max_memory), "Account max memory is [%s]"
                        " and expected is [%s]" % (account_maxmemory, max_memory))
        self.lg('%s ENDED' % self._testID)

