from MinionPlugin import MinionPlugin

class GarmrPlugin(MinionPlugin):


	default = {
		"template" : {
			"target" : { "type" : "url", "is_list" : True, "required" : True}
		},
		"safechecks" : { "type" : "bool", "value" : True}
	}

	def __init__(self):
		MinionPlugin.__init__(self, GarmrPlugin.default)

		self.state = "PENDING"
		self.messages = {
        	"PENDING" : "Plugin is pending execution.",
        	"WAITING" : "Execution is suspending, waiting for RESUME.",
        	"RUNNING" : "Execution is in progress.",
        	"COMPLETE" : "Execution is finished.",
        	"CANCELLED" : "Execution was cancelled.",
        	"FAILED" : "Execution failed."
		}
		self.allow_states = {
        	"PENDING" : ["START"],
        	"WAITING" : ["RESUME", "TERMINATE"],
        	"RUNNING" : ["SUSPEND", "TERMINATE"],
        	"COMPLETE" : [],
        	"CANCELLED" : [],
        	"FAILED" : []
        }


	def do_validate(self, config):
		return True

	def do_validate_key(self, key, value):
		return True

	def do_status(self):
		return self.create_status(True, self.messages["PENDING"], "PENDING")

	def do_start(self):
		return self.create_status(True, self.messages["RUNNING"], "RUNNING")

	def do_suspend(self):
		return self.create_status(True, self.messages["WAITING"], "WAITING")

	def do_terminate(self):
		return self.create_status(True, self.messages["CANCELLED"], "CANCELLED")

	def do_get_states(self):
		return self.allow_states[self.state]



