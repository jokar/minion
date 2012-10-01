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
    
    def __init__(self):
        ''' A list of PluginService (local) or PluginServiceClient (remote) - they have the same interface '''
        self.plugin_services = []
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
    
    def get_all_plugins(self):
        ''' Returns a list of all of the plugins available '''
        plist = []
        for ps in self.plugin_services:
            plugins = ps.get_plugins()
            for p in plugins["plugins"]:
                if p not in plist:
                    plist.append(p)
        return { 'plugins' : plist }
    
    def add_plugin_service(self, ps):
        self.plugin_services.append(ps)
    
    def remove_plugin_service(self, ps):
        self.plugin_services.remove(ps)

    ''' Probably should only use this internally for now '''
    def get_services_with_plugin(self, plugin, version):
        s = []
        for ps in self.plugin_services:
            plugins = ps.get_plugins()
            for p in plugins["plugins"]:
                if p["plugin"] is plugin and p["version"] is version:
                    ''' It shouldnt matter which one we choose, if they have the same name and version they should be identical '''
                    s.append(ps)
        return s

    def get_plugin_template(self, plugin, version):
        s = self.get_services_with_plugin(plugin, version)
        if len(s) is 0:
            raise TaskEngineError("Plugin not found %s" % plugin)
        return s[0].get_plugin_template(plugin)

    def get_plugin_service_info(self, service_name):
        return { 'plugin_services' : self.get_plugin_service(service_name).get_info() }
    
    def create_plugin_session(self, plugin, version):
        s = self.get_services_with_plugin(plugin, version)
        if len(s) is 0:
            raise TaskEngineError("Plugin not found %s" % plugin)
        ''' For now just select the first one;) '''
        result = {"plugin_service" : s[0].get_info()}
        result.update(s[0].create_session(plugin))
        return result

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

    def set_plugin_service_session_state(self, service_name, session, state):
        ps = self.get_plugin_service(service_name)
        result = {"plugin_service" : ps.get_info()}
        result.update(ps.set_session_state(session, state))
        return result

    def set_plugin_service_session_config(self, service_name, session, config):
        ps = self.get_plugin_service(service_name)
        ps.set_plugin_config(session, config)

    def get_plugin_service_session_results(self, service_name, session):
        ps = self.get_plugin_service(service_name)
        result = {"plugin_service" : ps.get_info()}
        result.update(ps.get_session_results(session))
        return result

