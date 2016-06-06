# encoding:utf-8
import PyV8

class Test():
    def js(self):
        ctxt = PyV8.JSContext()
        ctxt.enter()
        f_query1 = open("test.js", "r")
        html_cont = f_query1.read();
        print html_cont
        func = ctxt.eval(html_cont)
        print func()


if __name__ == '__main__':
    crawler = Test()
    crawler.js()
