# A simple Template plugin

from MinionPlugin import MinionPlugin
import threading
import time
from zap import ZAP

# TODO: This is work in progress!

class ZapScanThread(threading.Thread):
	
	zap = None
	target = None
		
	def setZap(self, zap):
		self.zap = zap

	def setTarget(self, target):
		self.target = target
				
	def run(self):
		self.zap.urlopen(self.target)
		
		# Give the sites tree a chance to get updated
		time.sleep(2)
		
		print 'Spidering target %s' % self.target
		self.zap.start_spider(self.target)
		# Give the Spider a chance to start
		time.sleep(2)
		while (int(self.zap.spider_status[0]) < 100):
			print 'Spider progress %: ' + self.zap.spider_status[0]
			time.sleep(5)
		
		print 'Spider completed'
		# Give the passive scanner a chance to finish
		time.sleep(5)
		
		print 'Scanning target %s' % self.target
		self.zap.start_scan(self.target)
		''' Nasty HACK '''
		#self.zap.start_scan("http://localhost:8080/")	
		time.sleep(5)
		while (int(self.zap.scan_status[0]) < 100):
			print 'Scan progress %: ' + self.zap.scan_status[0]
			time.sleep(5)

		print 'Scan completed? %s' % self.zap.scan_status[0]

class ZapPlugin(MinionPlugin):

	zap = ZAP(proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

	default = {
		"template" : {
			"target" : { "type" : "url", "is_list" : True, "required" : True}
		},
		"safechecks" : { "type" : "bool", "value" : True}
	}

	def __init__(self):
		MinionPlugin.__init__(self, ZapPlugin.default)

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
		target = "http://localhost:8080/bodgeit/"
		print "ZapPlugin pre start"
		try:
			zct = ZapScanThread()
			zct.setZap(self.zap)
			zct.setTarget(target)
			zct.start()
			
		except Exception as e:
			print "ZapPlugin failed %s" % e
		print "ZapPlugin post start"
		
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


