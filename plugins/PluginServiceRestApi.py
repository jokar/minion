'''
Created on 25 Sep 2012

@author: test

Simple wrapper around the PluginService providing, yes, a REST API

'''
from PluginService import PluginService, PluginServiceError
#from bottle import abort, get, put, post, delete, request, run
from bottle import Bottle, run

keys = { 
        "64c4c469ab0743a368d00466e1eb8608",  
        "ca8601b9a687c34703e46328e3dc69eb" 
        } 

app = Bottle()
service = PluginService("Test")

def is_authorized(req):
    key = req.headers.get('Authorization')
    # XX - timing independent check of key strings is required.
    return (key in keys)

@app.get("/info")
def get_info():
    if (not is_authorized(app.request)):
        app.abort(401, "Unauthorized request.")
    return service.get_info()

#@app.put("/session/create/<plugin_name>")
@app.get("/session/create/<plugin_name>")
def create_session(plugin_name):
    if (not is_authorized(app.request)):
        app.abort(401, "Unauthorized request.")
    try:
        return service.create_session(plugin_name);
    except PluginServiceError as e:
        return { "success" : False, "message" : e}

@app.get("/sessions")
def get_sessions():
    if (not is_authorized(app.request)):
        app.abort(401, "Unauthorized request.")
    try:
        return service.get_sessions()
    except PluginServiceError as e:
        return { "success" : False, "message" : e}

@app.delete("/session/<session>")
def terminate_session(session):
    if (not is_authorized(app.request)):
        app.abort(401, "Unauthorized request.")
    try:
        return service.terminate_session(session)
    except PluginServiceError as e:
        return { "success" : False, "message" : e}

@app.get("/session/<session>/status")
def get_session_status(session):
    if (not is_authorized(app.request)):
        app.abort(401, "Unauthorized request.")
    try:
        return service.get_session_status(session)
    except PluginServiceError as e:
        return { "success" : False, "message" : e}

@app.get("/session/<session>/states")
def get_session_states(session):
    if (not is_authorized(app.request)):
        app.abort(401, "Unauthorized request.")
    try:
        return service.get_session_state(session)
    except PluginServiceError as e:
        return { "success" : False, "message" : e}

@app.post("/session/<session>/state/<state>")
def set_session_states(session, state):
    if (not is_authorized(app.request)):
        app.abort(401, "Unauthorized request.")
    try:
        return service.set_session_state(session, state)
    except PluginServiceError as e:
        return { "success" : False, "message" : e}

run(app, host='localhost', port=8090)