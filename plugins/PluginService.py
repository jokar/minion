'''
Created on 25 Sep 2012

@author: test

This class should present the same interface as PluginServiceClient so the caller doesnt need to
know whether they are talking to a local or remote service.

'''
import os
from TemplatePlugin import TemplatePlugin

''' Version allows us to identify and support different versions of the PluginService '''
VERSION = 1

class PluginServiceError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PluginService(object):
    '''
    classdocs
    '''
    ''' Probbly the server name, but can be anything that identifies this service '''
    name = ''
    sessions = {}
    ''' TODO: how to load plugins dynamically? '''
    plugins = { "TemplatePlugin" : TemplatePlugin }

    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        
    def gen_session_key(self):
        return ''.join('%02x' % ord(x) for x in os.urandom(16))

    def create_session(self, plugin_name):
        if (plugin_name not in self.plugins):
            raise PluginServiceError("Unknown plugin %s" % plugin_name)
        plugin = self.plugins[plugin_name]
        session = self.gen_session_key();
        while (session in self.sessions):
            session = self.gen_session_key()
        self.sessions[session] = { "plugin_name" : plugin_name, "configuration" : "", "plugin" : plugin() }
        return { 
                "session" : session, 
                "message" : "Created new session for plugin '%s'" % plugin_name }
    
    def get_info(self):
        return {"name" : self.name, "version" : VERSION}
    
    def get_sessions(self):
        '''GET - get a list of all active sessions'''
        s = {}
        for session in self.sessions:
            s[session] = { 
                          "plugin_name" : self.sessions[session]["plugin_name"],
                          "status" : self.sessions[session]["plugin"].status(),
                          }
        return { 'sessions' : s }

    def terminate_session(self, session):
        if (session not in self.sessions):
            raise PluginServiceError("Unknown session %s" % session)
        sess = self.sessions[session]
        sess["plugin"].terminate()
        return { 
                "session" : session, 
                "message" : "Session terminated"}

    def get_session_status(self, session):
        if (session not in self.sessions):
            raise PluginServiceError("Unknown session %s" % session)
        sess = self.sessions[session]
        return sess["plugin"].status()

    def get_session_states(self, session):
        if (session not in self.sessions):
            raise PluginServiceError("Unknown session %s" % session)
        sess = self.sessions[session]
        return sess["plugin"].validStates()

    def set_session_state(self, session, state):
        if (session not in self.sessions):
            raise PluginServiceError("Unknown session %s" % session)
        sess = self.sessions[session]
        return sess["plugin"].changeState(state)
