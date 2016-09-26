class test2(object):
    def fun_2(self):
        print(4)

class test(object):
    var = test2()

    def fun_1(self):
        print(3)

    def fun_3(self):
        self.fun_1()




test.var.fun_2()
a = test
a.var.fun_2()
o = test()
o.var.fun_2()

