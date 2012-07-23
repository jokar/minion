Basic Requirements

Authentication
* use BrowserID Authentication

Access Controls
* group membership
* group membership assignment via email address (e.g. mozilla.com, mozilla.org)
* permissions are assigned to groups
* base permissions
** run scan
** view my results
** view my group results
** view all results
** system admin (configure server, add groups)
** group admin (configure groups, add user to group)

Task Manager
* Query plugin list to identify tasks available
* Provide a list of available tasks
* Allow user to configure a task to run:
** once
** periodically
** with defined start and end times (time/date) or duration (hours/days)
* provide a list of currently running tasks the user has visibility into
* for tasks the user has control of, options to stop, suspend, query, and resume tasks (default view should query running tasks for status)

Task Engine
* provide restful service to manage the status of tasks
* maintains references to configured plugins to provide configurations and access factories to spawn instances
* provide a mechanism for running tasks to raise alerts

Plugins
* Singleton that is a factory for plugin instances
* support a configuration method to get for a JSON[or xml :(] blob that describes configuration settings and options
* support for a spawn method that accepts a configuration and target specifier to create a new task
* support for an analyze method that can accept a result object and discover artefacts

Plugin Instance
* support querying for status
* support querying for state options (canSuspend, canResume)
* support for terminating the task
* finished tasks can be queried for a result set (includes result messages, a blob containing the tools native report format, and a list of identified artefacts)



== Basic Specs {needs work} ==

Artefacts
* objects discovered during the scan
* can represent vulnerabilities, new hosts, new targets, etc

Result Format
'''
  result
   {
    messages :
    {
      { TIMESTAMP, TYPE, LEVEL, CLASS, MESSSAGE},
      ...
    }
    results :
    { 
      BASE64_BLOB
    }
    artefacts : 
    {
      { ARTEFACTS }, 
      ... 
    }
   }
'''


--------------


Core Plugins
* Skipfish
* Garmr
* ZAP Proxy
