'''
Created on 25 Sep 2012

@author: test
'''
import unittest
from TaskEngine import TaskEngine, TaskEngineError
from PluginService import PluginService, PluginServiceError
from MinionPlugin import MinionPlugin

class TaskEngineTestCase(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testPluginServiceManagement(self):
        te = TaskEngine()
        
        ''' Check no services to start with '''
        result = te.get_plugin_services()
        if (len(result["plugin_services"]) is not 0):
            self.fail("Unexpected number of plugin services returned %s" % result)
            
        service_name = "TestService1"
            
        ''' Add a services to start with '''
        te.add_plugin_service(PluginService(service_name))
        result = te.get_plugin_services()
        if (len(result) is not 1):
            self.fail("Unexpected number of plugin services returned %s" % result)
        if (result["plugin_services"][0]["name"] is not service_name):
            self.fail("Unexpected name returned %s" % result)
        if (result["plugin_services"][0]["version"] is not 1):
            self.fail("Unexpected version returned %s" % result)
        
        ''' Should get a set of empty sessions'''
        result = te.get_plugin_service_sessions(service_name)
        if (result is None or "sessions" not in result):
            self.fail("No sessions returned %s" % result)
        if (len(result["sessions"]) != 0):
            self.fail("Unexpected number of sessions returned %s" % result)
            
        ''' start a valid session '''
        result = te.create_plugin_service_session(service_name, "TemplatePlugin")
        if (result is None or "session" not in result):
            self.fail("Failed to start session %s" % result)
        session = result["session"]
            
        ''' start an invalid session (no such plugin)'''
        try:
            te.create_plugin_service_session(service_name, "BadPlugin")
            self.fail("Successfully started a bad session %s" % result)
        except PluginServiceError:
            pass
            
        ''' Should get a set with one session in'''
        result = te.get_plugin_service_sessions(service_name)
        if (result is None or "sessions" not in result):
            self.fail("No sessions returned %s" % result)
        if (len(result["sessions"]) != 1):
            self.fail("Unexpected number of sessions returned %s" % result)
        if (session not in result["sessions"]):
            self.fail("Session %s not returned" % session)
        
        pass

    def testSessionStateManagement(self):
        te = TaskEngine()

        service_name = "TestService1"
            
        ''' Add a services to start with '''
        te.add_plugin_service(PluginService(service_name))

        ''' start a valid session '''
        result = te.create_plugin_service_session(service_name, "TemplatePlugin")
        if (result is None or "session" not in result):
            self.fail("Failed to start session %s" % result)
        session = result["session"]

        ''' check the status '''
        result = te.get_plugin_service_session_status(service_name, session)
        if (result["status"] is not MinionPlugin.STATUS_PENDING):
            self.fail("Unexpected session state %s" % result)
            
        ''' Should fail - invalid state '''
        result = te.set_plugin_service_session_states(service_name, session, MinionPlugin.STATE_RESUME)
        if ( result["status"] is not MinionPlugin.STATUS_FAILED):
            self.fail("Unexpected result - should have failed %s" % result)

        ''' Should fail - invalid state '''
        result = te.set_plugin_service_session_states(service_name, session, MinionPlugin.STATE_SUSPEND)
        if ( result["status"] is not MinionPlugin.STATUS_FAILED):
            self.fail("Unexpected result - should have failed %s" % result)
        
        ''' Should fail - invalid state '''
        result = te.set_plugin_service_session_states(service_name, session, MinionPlugin.STATE_TERMINATE)
        if ( result["status"] is not MinionPlugin.STATUS_FAILED):
            self.fail("Unexpected result - should have failed %s" % result)
            
        ''' Should work ok '''
        result = te.set_plugin_service_session_states(service_name, session, MinionPlugin.STATE_START)
        if ( result["status"] is not MinionPlugin.STATUS_RUNNING):
            self.fail("Unexpected result - should have worked %s" % result)
        
        ''' Should fail - invalid state '''
        result = te.set_plugin_service_session_states(service_name, session, MinionPlugin.STATE_START)
        if ( result["status"] is not MinionPlugin.STATUS_FAILED):
            self.fail("Unexpected result - should have failed %s" % result)
        
        ''' Should fail - invalid state '''
        result = te.set_plugin_service_session_states(service_name, session, MinionPlugin.STATE_RESUME)
        if ( result["status"] is not MinionPlugin.STATUS_FAILED):
            self.fail("Unexpected result - should have failed %s" % result)

        ''' Should work ok '''
        result = te.set_plugin_service_session_states(service_name, session, MinionPlugin.STATE_SUSPEND)
        if ( result["status"] is not MinionPlugin.STATUS_WAITING):
            self.fail("Unexpected result - should have worked %s" % result)
        
        #print "Result from set_session_states:"#
        #print result
        
        
        ''' start the plugin '''
        #result = service.
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()