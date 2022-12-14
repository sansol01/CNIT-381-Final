### teams Bot ###
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
### Utilities Libraries
import routers
import netconf_skills as netskills
import netmiko_skills as bu
import monitor_skill as monitoring

# Router Info 
device_address = routers.ncHQ['host']
device_username = routers.ncHQ['username']
device_password = routers.ncHQ['password']

# RESTCONF Setup
port = '443'
url_base = "https://{h}/restconf".format(h=device_address)
headers = {'Content-Type': 'application/yang-data+json',
           'Accept': 'application/yang-data+json'}

# Bot Details
bot_email = 'broski@webex.bot'
teams_token = 'Y2ZhZjFjOTAtMTZmYS00ZWM2LWIzOTItOTA4ZDBkMjk2ODNhNGNkY2MxNWItYTk0_P0A1_b34062fa-24f1-480f-a815-05d10d8cf4f2'
bot_url = "https://fc02-144-13-254-102.ngrok.io"
bot_app_name = 'Broski'

# Create a Bot Object
#   Note: debug mode prints out more details about processing to terminal
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},],
)

# Create a function to respond to messages that lack any specific command
# The greeting will be friendly and suggest how folks can get started.
def greeting(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hello {}, I'm a friendly CSR1100v assistant .  ".format(
        sender.firstName
    )
    response.markdown += "\n\nSee what I can do by asking for **/help**."
    return response


def new_loop(incoming_msg):
    response = Response()
    #resp = netskills.conf_loopback1()
    resp = netskills.conf_loopback(incoming_msg.text)
    response.markdown = str(resp)

    return response


def toggle_int(incoming_msg):
    response = Response()
    resp = netskills.toggle_handler(incoming_msg.text)
    response.markdown = resp

    return response

def backup(incoming_msg):
    response = Response()
    resp = bu.backup(incoming_msg.text)
    response.markdown = resp

    return response

def ping_test(incoming_msg):
    response = Response()
    resp = monitoring.ping()
    response.markdown = resp

    return response

def updatevpn(incoming_msg):
    response = Response()
    resp = monitoring.monitor()
    response.markdown = resp

    return response

# Set the bot greeting.
bot.set_greeting(greeting)

# Add Bot's Commmands
bot.add_command("toggle", "Ex: toggle [router] [interface] | toggle r2 lo2", toggle_int)
bot.add_command("new loop", "Ex: new loop 2", new_loop)
bot.add_command("backup", "Ex: backup [router|all] | backup Branch | backup all", backup)
bot.add_command("vpn test", "Ex: tests the vpn config", ping_test)
bot.add_command("update vpn", "Ex: updates the vpn configuration", updatevpn)
# Every bot includes a default "/echo" command.  You can remove it, or any
bot.remove_command("/echo")

if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5000)
