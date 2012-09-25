'''
Created on 24 Sep 2012

@author: test
'''
import unittest
from MinionPlugin import MinionPlugin
from TemplatePlugin import TemplatePlugin


class TemplatePluginTestCase(unittest.TestCase):

    def check_result(self, result, expected):
        if (result.get("status") != expected):
            self.fail("Expected " + expected + " got " + result.get("status") )

    def testStandardRunName(self):
        plugin = TemplatePlugin()
        self.check_result(plugin.status(), MinionPlugin.STATUS_PENDING);
        plugin.start()
        self.check_result(plugin.status(), MinionPlugin.STATUS_RUNNING);
        plugin.suspend()
        self.check_result(plugin.status(), MinionPlugin.STATUS_WAITING);
        plugin.resume()
        self.check_result(plugin.status(), MinionPlugin.STATUS_RUNNING);
        plugin.terminate()
        self.check_result(plugin.status(), MinionPlugin.STATUS_CANCELLED);

    def testFail(self):
        #self.fail("Failed");
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()