'''
Created on 26 Sep 2012

@author: psiinon
'''

class TaskEngineError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class TaskEngine(object):
    
    ''' A list of PluginService (local) or PluginServiceClient (remote) - they have the same interface '''
    plugin_services = []
    
    def __init__(self):
        pass
    
    def get_plugin_service(self, service_name):
        for ps in self.plugin_services:
            if (ps.get_info()["name"] == service_name):
                return ps
        raise TaskEngineError("Unknown plugin service %s" % service_name)
    
    def get_plugin_services(self):
        s = []
        for ps in self.plugin_services:
            s.append(ps.get_info())
        return { 'plugin_services' : s }
    
    def add_plugin_service(self, ps):
        self.plugin_services.append(ps)
    
    def remove_plugin_service(self, ps):
        self.plugin_services.remove(ps)

    def get_plugin_service_info(self, service_name):
        return { 'plugin_services' : self.get_plugin_service(service_name).get_info() }
    
    def create_plugin_service_session(self, service_name, plugin_name):
        ps = self.get_plugin_service(service_name)
        result = {"plugin_service" : ps.get_info()}
        result.update(ps.create_session(plugin_name))
        return result

    def get_plugin_service_sessions(self, service_name):
        ps = self.get_plugin_service(service_name)
        result = {"plugin_service" : ps.get_info()}
        result.update(ps.get_sessions())
        return result

    def terminate_plugin_service_session(self, service_name, session):
        ps = self.get_plugin_service(service_name)
        result = {"plugin_service" : ps.get_info()}
        result.update(ps.get_session(session))
        return result

    def get_plugin_service_session_status(self, service_name, session):
        ps = self.get_plugin_service(service_name)
        result = {"plugin_service" : ps.get_info()}
        result.update(ps.get_session_status(session))
        return result

    def get_plugin_service_session_states(self, service_name, session):
        ps = self.get_plugin_service(service_name)
        result = {"plugin_service" : ps.get_info()}
        result.update(ps.get_session_states(session))
        return result

    def set_plugin_service_session_states(self, service_name, session, state):
        ps = self.get_plugin_service(service_name)
        result = {"plugin_service" : ps.get_info()}
        result.update(ps.set_session_state(session, state))
        return result
