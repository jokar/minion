'''
Created on 25 Sep 2012

@author: test
'''
import unittest
from PluginService import PluginService, PluginServiceError
from MinionPlugin import MinionPlugin


class PluginServiceTestCase(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testBasicSessionManagement(self):
        service = PluginService("Test")
        
        ''' Basic info'''
        result = service.get_info()
        if (result["name"] is not "Test"):
            self.fail("Unexpected name returned %s" % result)
        if (result["version"] is not 1):
            self.fail("Unexpected version returned %s" % result)
        
        ''' Should get a set of empty sessions'''
        result = service.get_sessions()
        if (result is None or "sessions" not in result):
            self.fail("No sessions returned %s" % result)
            
        ''' start a valid session '''
        result = service.create_session("TemplatePlugin")
        if (result is None or "session" not in result):
            self.fail("Failed to start session %s" % result)
        session = result["session"]
            
        ''' start an invalid session (no such plugin)'''
        try:
            service.create_session("BadPlugin")
            self.fail("Successfully started a bad session %s" % result)
        except PluginServiceError:
            pass
            
        ''' Should get a set with one session in'''
        result = service.get_sessions()
        if (result is None or "sessions" not in result):
            self.fail("No sessions returned %s" % result)
        if (len(result["sessions"]) != 1):
            self.fail("Unexpected number of sessions returned %s" % result)
        if (session not in result["sessions"]):
            self.fail("Session %s not returned" % session)
        
        pass

    def testSessionStateManagement(self):
        service = PluginService("Test")

        ''' start a valid session '''
        result = service.create_session("TemplatePlugin")
        if (result is None or "session" not in result):
            self.fail("Failed to start session %s" % result)
        session = result["session"]
        
        ''' check the status '''
        result = service.get_session_status(session)
        if (result["status"] is not MinionPlugin.STATUS_PENDING):
            self.fail("Unexpected session state %s" % result)
            
        ''' Should fail - invalid state '''
        result = service.set_session_states(session, MinionPlugin.STATE_RESUME)
        if ( result["status"] is not MinionPlugin.STATUS_FAILED):
            self.fail("Unexpected result - should have failed %s" % result)

        ''' Should fail - invalid state '''
        result = service.set_session_states(session, MinionPlugin.STATE_SUSPEND)
        if ( result["status"] is not MinionPlugin.STATUS_FAILED):
            self.fail("Unexpected result - should have failed %s" % result)
        
        ''' Should fail - invalid state '''
        result = service.set_session_states(session, MinionPlugin.STATE_TERMINATE)
        if ( result["status"] is not MinionPlugin.STATUS_FAILED):
            self.fail("Unexpected result - should have failed %s" % result)
            
        ''' Should work ok '''
        result = service.set_session_states(session, MinionPlugin.STATE_START)
        if ( result["status"] is not MinionPlugin.STATUS_RUNNING):
            self.fail("Unexpected result - should have worked %s" % result)
        
        ''' Should fail - invalid state '''
        result = service.set_session_states(session, MinionPlugin.STATE_START)
        if ( result["status"] is not MinionPlugin.STATUS_FAILED):
            self.fail("Unexpected result - should have failed %s" % result)
        
        ''' Should fail - invalid state '''
        result = service.set_session_states(session, MinionPlugin.STATE_RESUME)
        if ( result["status"] is not MinionPlugin.STATUS_FAILED):
            self.fail("Unexpected result - should have failed %s" % result)

        ''' Should work ok '''
        result = service.set_session_states(session, MinionPlugin.STATE_SUSPEND)
        if ( result["status"] is not MinionPlugin.STATUS_WAITING):
            self.fail("Unexpected result - should have worked %s" % result)
        
        print "Result from set_session_states:"
        print result
        
        
        ''' start the plugin '''
        #result = service.
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()