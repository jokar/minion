from copy import deepcopy
import sys

def hasKey(collection, key):
    path = key.strip().split('.')
    ptr = collection
    keyCheck = path[-1]
    while (path[0] in ptr):
        if ((path[0] == keyCheck) and (len(path) == 1)):
            return ptr[path[0]]
    ptr = ptr[path[0]]
    path.pop(0) 
    raise Exception("Value not found in collection.")

def setKey(collection, key, value, force=False):
    path = key.strip().split('.')
    ptr = collection
    keyCheck = path[-1]
    if (force):
        if (not path[0] in ptr):
            ptr[path[0]] = {}
    while (path[0] in ptr):
        if ((path[0] == keyCheck) and (len(path) == 1)):
            ptr[path[0]] = value
            return
    ptr = ptr[path[0]]
    path.pop(0)
    if (force):
        if (not path[0] in ptr):
            ptr[path[0]] = {}
    raise Exception("Path not found")

class MinionPluginError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MinionPlugin:
    PLUGIN_TYPE_ABSTRACT = "Abstract"   # Should just used by this class
    PLUGIN_TYPE_WEBAPP = "WebApp"

    TYPE = PLUGIN_TYPE_ABSTRACT
    VERSION = 1
    
    STATUS_PENDING = "PENDING"
    STATUS_WAITING = "WAITING"
    STATUS_RUNNING = "RUNNING"
    STATUS_COMPLETE = "COMPLETE"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_FAILED = "FAILED"
    
    STATE_RESUME = "RESUME"
    STATE_START = "START"
    STATE_SUSPEND = "SUSPEND"
    STATE_TERMINATE = "TERMINATE"
    
    STATUSES = [STATUS_PENDING, STATUS_WAITING, STATUS_RUNNING, STATUS_COMPLETE, STATUS_CANCELLED, STATUS_FAILED]
    STATES = [STATE_RESUME, STATE_START, STATE_SUSPEND, STATE_TERMINATE]

    def create_status(self, success, message, status):
        return { "success" : success, "message" : message, "status" : status} 

    def create_std_status(self, success, status):
        return { "success" : success, "message" : "TBA", "status" : status} 

    def create_status_plus(self, success, message, status, plus):
        s = self.create_status(success, message, status)
        s.update(plus)
        return s

    default = { }
    def __init__(self, default):
        self.template = deepcopy(self.__class__.default)
        #self.configuration = deepcopy(self.__class__.default)
        self.configuration = {}


    def resetConfig(self):
        #self.configuration = deepcopy(self.__class__.default)    
        self.configuration = {}    

    def getTemplate(self):
        return self.template

    def getTemplateForKey(self, key):
        for tkey in self.template["template"]:
            if tkey is key:
                return self.template["template"][key]
        return None

    def getConfig(self):
        return self.configuration

    def setConfig(self, config):
        if (self.status()["status"] != MinionPlugin.STATUS_PENDING):
            raise MinionPluginError("Cannot configure a plugin once execution has started.")
        #XXX - Extension Point - do_validate(config), return True|False
        if (self.validateConfig(config)):
            self.configuration = config
        else:
            raise MinionPluginError("Invalid configuration exception.")

    def validateConfig(self, config):
        ''' first check each value is in the template '''
        for ckey in config:
            self.validateKey(ckey, config[ckey])
        ''' now check for missing 'required' values '''
        for tkey in self.template["template"]:
            if tkey not in config:
                raise MinionPluginError("Missing key %s" % tkey)
            
        return self.do_validate_config(config)
        
    def do_validate_config(self, config):
        ''' first check each value is in the template '''
        for ckey in config:
            self.validateKey(ckey, config[ckey])
        return True

    def validateKey(self, key, value):
        ''' first check each value is in the template '''
        tmp = self.getTemplateForKey(key)
        if tmp is None:
            raise MinionPluginError("Unknown key %s" % key)
        return self.do_validate_key(key, value)

    def getValue(self, key):
        try:
            return hasKey(self.configuration, key)
        except:
            return None

    def setValue(self, key, value):
        if (self.status()["status"] != MinionPlugin.STATUS_PENDING):
            raise MinionPluginError("Cannot configure a plugin once execution has started.")
        if (self.validateKey(key, value)):
            return setKey(self.configuration, key, value, True)


    def status(self):
        try:
            #XXX - Extension Point - do_status(), return create_status()
            result = self.do_status()
            return result
        except:
            return self.create_status(False, "Plugin was unable to report a status: %s" % sys.exc_info()[0], MinionPlugin.STATUS_FAILED)

    def start(self):        
        try:        
            if (self.canEnterState(self.STATE_START)):
                self.validateConfig(self.getConfig())
                #XXX - Extension Point - do_start(), return create_status()
                self.do_start()
                query = self.status()
                return self.create_status(query["success"], "Plugin started: %s" % query["message"], query["status"])
            else:
                return self.create_status(False, "Plugin could not be started: %s" % query["message"], query["status"])
        except:
            return self.create_status(False, "START failed: %s" % sys.exc_info()[0], MinionPlugin.STATUS_FAILED)


    def suspend(self):
        try:            
            if (self.canEnterState(self.STATE_SUSPEND)):
                #XXX - Extension Point - do_suspend(), return create_status()
                self.do_suspend()
                query = self.status()
                return self.create_status(query["success"], "Plugin suspended: %s" % query["message"], query["status"])
            else:
                return self.create_status(False, "Plugin could not be suspended: %s" % query["message"], query["status"])
        except:
            return self.create_status(False, "SUSPEND failed: %s" % sys.exc_info()[0], MinionPlugin.STATUS_FAILED)

    def resume(self):
        try:            
            if (self.canEnterState(self.STATE_RESUME)):
                #XXX - Extension Point - do_resume(), return create_status()
                self.do_resume()
                query = self.status()
                return self.create_status(query["success"], "Plugin resumed: %s" % query["message"], query["status"])
            else:
                return self.create_status(False, "Plugin could not be resumed: %s" % query["message"], query["status"])
        except:
            return self.create_status(False, "RESUME failed: %s" % sys.exc_info()[0], MinionPlugin.STATUS_FAILED)

    def terminate(self):
        try:            
            if (self.canEnterState(self.STATE_TERMINATE)):
                #XXX - Extension Point - do_terminate(), return create_status()
                self.do_terminate()
                query = self.status()
                return self.create_status(query["success"], "Plugin terminated: %s" % query["message"], query["status"])
            else:
                return self.create_status(False, "Plugin could not be terminated: %s" % query["message"], query["status"])
        except:
            return self.create_status(False, "TERMINATE failed: %s" % sys.exc_info()[0], MinionPlugin.STATUS_FAILED)

    def canEnterState(self, state):
        try:
            if not state in self.STATES:
                raise MinionPluginError("Invalid state %s" % state)
            #XXX - Extension Point - do_get_states() : return [] containing available states
            states = self.do_get_states()
            return state in states
        except:
            return False

    def validStates(self):
        return self.do_get_states()
    
    def changeState(self, state):
        if (state is self.STATE_START):
            return self.start()
        elif (state is self.STATE_SUSPEND):
            return self.suspend()
        elif (state is self.STATE_RESUME):
            return self.resume()
        elif (state is self.STATE_TERMINATE):
            return self.terminate()
        else:
            raise MinionPluginError("Invalid state %s" % state)
        
    def getResults(self):
        return self.do_get_results()
        
