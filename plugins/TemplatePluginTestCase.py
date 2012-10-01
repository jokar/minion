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

    def testBasicStateChanges(self):
        plugin = TemplatePlugin()
        self.check_result(plugin.status(), MinionPlugin.STATUS_PENDING);
        plugin.setConfig({"target" : "http://localhost"})
        plugin.start()
        self.check_result(plugin.status(), MinionPlugin.STATUS_RUNNING);
        plugin.suspend()
        self.check_result(plugin.status(), MinionPlugin.STATUS_WAITING);
        plugin.resume()
        self.check_result(plugin.status(), MinionPlugin.STATUS_RUNNING);
        plugin.terminate()
        self.check_result(plugin.status(), MinionPlugin.STATUS_CANCELLED);

    def testConfigs(self):
        print TemplatePlugin.default
        plugin = TemplatePlugin()
        plugin.setValue("target", "http://localhost")
        if plugin.getValue("target") is not "http://localhost":
            self.fail("Unexpected value %s" % plugin.getValue("target"))
        try:
            plugin.setValue("badkey", "whatever")
            self.fail("Expected key to fail")
        except:
            pass
        try:
            plugin.setConfig({})
            self.fail("Expected key to fail")
        except:
            pass
        try:
            plugin.setConfig({"badkey" : "whatever"})
            self.fail("Expected key to fail")
        except:
            pass
        
        plugin.setConfig({"target" : "http://localhost"})
        plugin.resetConfig()
        try:
            plugin.validateConfig({})
            self.fail("Expected to fail")
        except:
            pass
        
    def testFakeResults(self):
        plugin = TemplatePlugin()
        self.check_result(plugin.status(), MinionPlugin.STATUS_PENDING);
        plugin.setConfig({"target" : "http://localhost"})
        plugin.start()
        results = plugin.getResults()
        print results

        print plugin.status()
        print plugin.status()
        results = plugin.getResults()
        print results

        print plugin.status()
        print plugin.status()
        results = plugin.getResults()
        print results

        print plugin.status()
        print plugin.status()
        results = plugin.getResults()
        print results


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()