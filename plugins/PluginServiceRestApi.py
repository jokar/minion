'''
Created on 25 Sep 2012

@author: test

Wrapper around the PluginService providing, yes, a REST API
'''
from PluginService import PluginService
#from bottle import abort, get, put, post, delete, request, run
import bottle
#import json

class PluginServiceRestApi(object):
    '''
    classdocs
    '''
    ''' Probbly the server name, but can be anything that identifies this service '''
    service = None

    def __init__(self):
        '''
        Constructor
        '''
        self.service = PluginService()
        
    @bottle.put("/session/create/<plugin_name>")
    def create_session(self, plugin_name):
        return self.create_session(plugin_name);
    
    @bottle.get("/info")
    def get_info(self):
        return self.service.get_info()
    
    @bottle.get("/sessions")
    def get_sessions(self):
        return self.service.get_sessions()

    @bottle.delete("/session/<session>")
    def terminate_session(self, session):
        ''' Why doesnt this work??'''
        return self.service.terminate_session(session)

    def get_session_status(self, session):
        return self.get_session_status(session)

    def get_session_states(self, session):
        return self.get_session_state(session)

    def set_session_states(self, session, state):
        return self.set_session_state(session, state)
