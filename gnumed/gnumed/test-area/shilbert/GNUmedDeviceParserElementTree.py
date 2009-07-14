#======================================================================
# GNUmed Device parser
#
# @copyright: author
#======================================================================
__version__ = "$Revision: 1.10 $"
__author__ = "Sebastian Hilbert"
__license__ = 'GPL (details at http://www.gnu.org)'

from lxml import etree
import logging

_log = logging.getLogger('gm.ui')
_log.info(__version__)
#======================================================================
# Devices holds a list of all cardiac devices in the xml
# each list item holds a device context ( generator and one or more leads )
##Devices = []
# DeviceParts is the device context and holds one or more device parts. Each list item
# is a device part such as lead , generator which in turn can consist of 
# device parts such as mainboard or battery
##DeviceParts = []

def extractDevices(DevicesTree=None):
	Devices = []
	# sort device list, first ICD, then pacemaker, then disconnected devices
	for Device in DevicesTree:
		Devices.append(Device)
	return Devices
    
def sortDevicesByTypeAndStatus(Devices=None):
	# todo: sort later, for now return like order gotten from XML 
	return Devices

def extractDeviceParts(Device=None,Type=None):
	DeviceParts = []
	for DevicePart in Device:
		if DevicePart.get("type") == Type:
			DeviceParts.append(DevicePart)
	return DeviceParts
    
def sortLeadsByPosition(Leads=None):
	#skips sorting for now
	return Leads

def extractActions(DevicePart=None,Type=None):
	Actions = []
	# get a list of all procedures for this DevicePart
	for tag in DevicePart.getchildren():
		if tag.get("type") == Type:
			Actions.append(tag)
	return Actions

def extractTagData(start_node=None,SearchTag=None):
	#tag = None
	for tag in start_node.getchildren():
		if tag.tag==SearchTag:
			return tag.text

def extractTagAttribute(start_node=None,SearchTag=None,Attribute=None):
	#tag = None
	for tag in start_node.getchildren():
		if tag.tag==SearchTag:
			return tag.get(Attribute)

#def extractDeviceSubParts(DevicePart=None):
    #DeviceSubParts = []
#    DeviceObject = Device
    #for DevicePart in DeviceObject:
    #    print ('The device has the following parts: %s' %DevicePart)
        # a subpart is like the CPU of a generator and so forth
    #    for KeyAttribute in DevicePart.keys():
    #        if DevicePart.get(KeyAttribute)=='mainboard':
    #            print 'hey we are dealing with a mainboard here:-)'
                #manufacturer
    #            manufacturer=extractTagData(DevicePart,'manufacturer')
                #model
    #            model=extractTagData(DevicePart,'model')
                #return(manufacturer,model)

    #        elif DevicePart.get(KeyAttribute)=='battery':
    #            print 'hey we are dealing with a battery here'

    #        else:
    #            print 'hey we are dealing with an unkown device part here. Please provide the XML file to the GNUmed team.'

def device_status_as_text(tree=None):
	DevicesDict = {}
	DevicePartSpecsDict = {}
	DevicesDisplayed = []
	""" In this area GNUmed will place the status of all cardiac devices and device parts. 
	There can be more than one device at a time\n\n
	It potentially looks like this\n
	----------------------------------------------------------------------------------------------------------------\n
	Device: SJM Atlas DR (active)     Battery: 2.4V (MOL)      Implanted:  Feb 09 2008\n\n
	RA: Medtronic Sprint fidelis (active, flaky, replacement)             Implanted: Feb 09 2008\n
	Sensing: 2 (1.5) mV    Threshold: 0.7/0.5 (1/0.4) V/ms       Impedance: 800 (900) Ohm\n\n
	RV: Medtronic Sprint fidelis (active, flaky, replacement)             Implanted: Feb 09 2008\n
	Sensing: 7 (15) mV    Threshold: 0.7/0.5 (1/0.4) V/ms       Impedance: 800 (900) Ohm\n\n
	LV: Medtronic Sprint fidelis (active, flaky, Y-connector)             Implanted: Feb 09 2008\n
	Sensing: 7 ( ?) mV    Threshold: 1/1.5 (1/1) V/ms       Impedance: 800 (900) Ohm\n
	----------------------------------------------------------------------------------------------------------------\n
	Device: Medtronic Relia SR (inactive)     Battery 2.1V (EOL)   Implanted: Jan 23 2000\n\n
	Device: Medtronic Kappa SR (explanted)     Battery 2.1V (EOL)   Explanted: Jan 23 2000 (Jan 23 1995)\n
	-----------------------------------------------------------------------------------------------------------------\n
	RA Lead: Medtronic ? (inactive, capped)             Implanted: Jan 23 2000\n
	RV Lead: Medtronic ? (explanted)                        Explanted: Feb 09 2008
	"""
	"""
	first search for devices, produce a list, 
	sort in active devices first, ICD befor pacemaker before disconnted devices
	per convention a single generator or lead which is not connected is a self contained device
	there are virtual devices such as 'ICD' or 'pacemaker' which consist of parts such as leads and generator
	there are true devices such as inactive leads or non-explanted generators
	class will be 'lead' instead of type 'lead' for DeviceParts
	"""
	DevicesTree = tree.getroot() 
	Devices = extractDevices(DevicesTree)
	DevicesSorted = sortDevicesByTypeAndStatus(Devices)
	#print 'Number of devices: %s' %len(Devices)
    
	for Device in DevicesSorted:
		DevicesDisplayed.append('-------------------------------------------------------------\n')
		# check for class
		DeviceClass=Device.get("class")
		if DeviceClass == 'ICD':
			# get generator xml node
			Generator = extractDeviceParts(Device=Device,Type='generator')[0]
			# get generator vendor, model, devicestate
			vendor = extractTagData(start_node=Generator,SearchTag='vendor')
			model = extractTagData(start_node=Generator,SearchTag='model')
			devicestate = extractTagData(start_node=Generator,SearchTag='devicestate')
			# get subpart battery
			battery = extractDeviceParts(Device=Generator,Type='battery')[0]
			action = extractActions(DevicePart=battery,Type='interrogation')[0]
			battery_voltage = extractTagData(start_node=action,SearchTag='voltage')
			battery_voltage_unit = extractTagAttribute(start_node=action,SearchTag='voltage',Attribute='unit')
			battery_status = extractTagData(start_node=action,SearchTag='status')
			implantation_date= extractTagData(start_node=Generator,SearchTag='doi')
			line = _('Device(%s):') %DeviceClass + ' ' + vendor + ' ' + model + ' ' + '('+ devicestate + ')'+'   '+_('Battery:')+' '+battery_voltage+' '+battery_voltage_unit+'('+battery_status+')'+'  '+_('Implanted:')+' '+implantation_date+'\n\n'
			# append each line to a list, later produce display string by parsing list
			DevicesDisplayed.append(line)
			#DevicesDisplayed.append('\n')
			# now get the leads, RA then RV and last LV if they exist
			# todo: think about four leads : pace/sense but on another thought they both simply show up as RV leads
			Leads = extractDeviceParts(Device=Device,Type='lead')
			LeadsSorted = sortLeadsByPosition(Leads)
			for Lead in LeadsSorted:
				leadposition = extractTagData(start_node=Lead,SearchTag='leadposition')
				leadslot = extractTagData(start_node=Lead,SearchTag='leadslot')
				vendor = extractTagData(start_node=Lead,SearchTag='manufacturer')
				model = extractTagData(start_node=Lead,SearchTag='model')
				devicestate = extractTagData(start_node=Lead,SearchTag='devicestate')
				comment = extractTagData(start_node=Lead,SearchTag='comment')
				implantation_date = extractTagData(start_node=Lead,SearchTag='doi')
				line = '%s-lead in %s-position:' %(leadposition,leadslot) + ' ' + vendor + ' ' + model + ' ' + '(' + devicestate + ',' + comment + ')' + ' ' + 'Implanted:' + ' ' + implantation_date +'\n'
				DevicesDisplayed.append(line)
				#now get the newest interrogation
				action = extractActions(DevicePart=Lead,Type='interrogation')[0]
				action_date = extractTagData(start_node=action,SearchTag='dop')
				sensing = extractTagData(start_node=action,SearchTag='sensing')
				sensingunit = extractTagAttribute(start_node=action,SearchTag='sensing',Attribute='unit')
				threshold = extractTagData(start_node=action,SearchTag='thresholdvoltage')
				thresholdunit = extractTagAttribute(start_node=action,SearchTag='thresholdvoltage',Attribute='unit')
				impedance = extractTagData(start_node=action,SearchTag='impedance')
				impedanceunit = extractTagAttribute(start_node=action,SearchTag='impedance',Attribute='unit')
				line = _('last check:')+' '+action_date+' '+_('Sensing:')+' '+sensing+sensingunit+' '+_('Threshold')+' '+threshold+thresholdunit+' '+_('Impedance:')+' '+impedance+' '+impedanceunit+'\n\n' 
				DevicesDisplayed.append(line)
	return DevicesDisplayed

if __name__ == '__main__':
	from Gnumed.pycommon import gmI18N
	gmI18N.activate_locale()
	gmI18N.install_domain()

	# for now assume that the xml file provide the cardiac device context.
	# that pretty much means logical connection of leads and generator is provided in the xml
	tree = etree.parse('GNUmed6.xml')
	DevicesDisplayed = device_status_as_text(tree)
	for line in DevicesDisplayed:
		print line