# A simple Template plugin

from MinionPlugin import MinionPlugin

class TemplatePlugin(MinionPlugin):


	default = {
		"template" : {
			"target" : { "type" : "url", "is_list" : True, "required" : True}
		},
		"safechecks" : { "type" : "bool", "value" : True}
	}

	def __init__(self):
		MinionPlugin.__init__(self, TemplatePlugin.default)
		#super().__init__(TemplatePlugin.default)

		self.state = MinionPlugin.STATUS_PENDING

		self.messages = {
        	"PENDING" : "Plugin is pending execution.",
        	"WAITING" : "Execution is suspending, waiting for RESUME.",
        	"RUNNING" : "Execution is in progress.",
        	"COMPLETE" : "Execution is finished.",
        	"CANCELLED" : "Execution was cancelled.",
        	"FAILED" : "Execution failed."
		}
		self.allow_states = {
        	MinionPlugin.STATUS_PENDING : [MinionPlugin.STATE_START],
        	MinionPlugin.STATUS_WAITING : [MinionPlugin.STATE_RESUME, MinionPlugin.STATE_TERMINATE],
        	MinionPlugin.STATUS_RUNNING : [MinionPlugin.STATE_SUSPEND, MinionPlugin.STATE_TERMINATE],
        	MinionPlugin.STATUS_COMPLETE : [],
        	MinionPlugin.STATUS_CANCELLED : [],
        	MinionPlugin.STATUS_FAILED : []
        }


	def do_validate(self, config):
		return True

	def do_validate_key(self, key, value):
		return True

	def do_status(self):
		return self.create_status(True, self.messages[self.state], self.state)

	def do_start(self):
		self.state = MinionPlugin.STATUS_RUNNING
		#return self.create_status(True, self.messages[self.state], self.state)
		return self.create_std_status(True, self.state)

	def do_suspend(self):
		self.state = MinionPlugin.STATUS_WAITING
		return self.create_status(True, self.messages[self.state], self.state)

	def do_resume(self):
		self.state = MinionPlugin.STATUS_RUNNING
		return self.create_status(True, self.messages[self.state], self.state)

	def do_terminate(self):
		self.state = MinionPlugin.STATUS_CANCELLED
		return self.create_status(True, self.messages[self.state], self.state)

	def do_get_states(self):
		return self.allow_states[self.state]


