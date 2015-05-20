from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

#TODO: Add method to change community data string to support different versions of SNMP.
#TODO: Add support to set/get multiple outlets.

class APCUnit:
	"""  A class that represents an APC power management unit. """
	
	# OID for the outlet Control 
	outletCtlOID = (1,3,6,1,4,1,318,1,1,4,4,2,1,3)
	
	# states that can be set.
	on = 1
	off = 2
	reboot = 3 
	rd = 7 # Reboot with Delay.
	
	def __init__(self, host, port=161 ):
		""" Set up object with a host and port. """
		self.host = host
		self.port = port
		self.community = cmdgen.CommunityData('my-agent', 'private', 0)
		self.target = cmdgen.UdpTransportTarget((host, port))
	
	def getOutletCtl(self, outlet):
		""" Get the current state of an outlet. """
		oid = self.outletCtlOID + (outlet,)
		errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(self.community, self.target, oid)
		print varBinds
		
	def setOutletCtl(self, outlet, state):
		""" Set an outlet. """
		oid = self.outletCtlOID + (outlet,)
		setting = rfc1902.Integer32(state)
		
		errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(self.community, self.target, (oid, setting))
		
		#print errorIndication
		print varBinds
		

if __name__ == "__main__":
	""" We're being run as a script. """
	a = APCUnit("10.1.2.27")
	print a.on
	a.getOutletCtl(1)
	a.setOutletCtl(1, a.reboot)