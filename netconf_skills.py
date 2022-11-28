from ncclient import manager
import xml.dom.minidom
import routers

#r1 = manager.connect(**routers.router1)
#r2 = manager.connect(**routers.router2)


r1 = manager.connect(
    host="192.168.56.101",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

r2 = manager.connect(
    host="192.168.56.103",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

# import templates
int_off_template = open("interfaces/int_switch_off.j2").read()
int_on_template = open("interfaces/int_switch_on.j2").read()
int_filter = open("interfaces/int_filter.j2").read()
new_loop = open("interfaces/new_loop.j2").read()

#Configures a loopback interface on router one for demo purposes
def conf_loopback(number): 
    loop_config = new_loop.format(num=number[9])
    print(loop_config)
    #Create the interface using the configuration template
    netconf_reply = r1.edit_config(target="running", config=loop_config)
    print(netconf_reply)
    #Use a filter to only show interface name and description
    netconf_reply = r1.get_config(source="running", filter = int_filter.format(full_int_name = ("Loopback" + number[9])))
    return xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml() #Return the reply


### stuff that toggles interfaces ###

'''
Checks weather an interface is up or down.
    interface: template tailored to the target interface
    rTarget: the target router
Returns: 1 if enabled, 0 if disabled
'''
def check_interface(interface,rTarget):
    #get the target interface's configuration 
    netconf_reply = str(rTarget.get_config(source="running", filter = interface))
    #check if the interface is enabled
    if "<enabled>true</enabled>" in netconf_reply:
        return 1 
    else: 
        return 0



# Determines what router and interface should be toggled based on the arguments.
def toggle_handler(message):
    #cut toggle out of the string
    args = message[6:]
    
    #check for a target interface
    if "lo2" in args:
        intName = "Loopback"
        intNum = "2"
    elif "lo3" in args:
        intName = "Loopback"
        intNum = "3"
    elif "gb1" in args:
        intName = "GigabitEthernet"
        intNum = "1"
    elif "gb2" in args:
        intName = "GigabitEthernet"
        intNum = "2"
    else: #default to lo1
        intName = "Loopback"
        intNum = "1"

    #Check for a target router
    if "r2" in args:
        rTarget = r2
    else: #default to r1
        rTarget = r1

    #call toggle_interface and return the result
    return toggle_interface(intName,intNum, rTarget)

'''
Actually toggles the interface.
    intName: The type of interface
    intNum: The interface number
    rTarget: The target router
Returns: The state of the toggled router
'''
def toggle_interface(intName, intNum, rTarget):
    #Put the filter used to check the state of the interface together
    netconf_filter = int_filter.format(full_int_name = (intName+intNum))
    
    #check the state of the interface and then build the payload
    if (check_interface(netconf_filter, rTarget) == 0): #if the interface is down:
        netconf_payload = int_on_template.format(int_name = intName, int_num = intNum)
    else:
        netconf_payload = int_off_template.format(int_name = intName, int_num = intNum)

    #Toggle the router
    rTarget.edit_config(target="running", config=netconf_payload)
    netconf_reply = rTarget.get_config(source="running", filter = netconf_filter)
    
    return xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()
