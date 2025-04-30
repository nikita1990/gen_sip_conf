from sys import argv
import argparse



# Author: Nikita Konyshev
# Email: nikitakonishev@hotmail.com
# Initialize argument parser with a description
parser = argparse.ArgumentParser(description="Generate SIP trunk configuration based on input parameters")

# Define command-line arguments
parser.add_argument("-n", "--name", type=str, help="Trunk name", required=True)
parser.add_argument("-d", "--domain", type=str, help="Domain of the SIP server", required=True)
parser.add_argument("-u", "--username", type=str, help="SIP username", required=True)
parser.add_argument("-ps", "--password", type=str, help="SIP password", required=True)
parser.add_argument("-pn", "--phonenumber", type=str, help="Phone number associated with the trunk", required=True)
parser.add_argument("-id", "--client_id", type=int, help="Client identifier", required=True)  # Changed from 'lk' to 'client_id'
parser.add_argument("-prefix", "--prefix", type=int, help="Prefix for outgoing calls", required=True)
parser.add_argument("-op", "--outboundproxy", type=str, help="Outbound proxy (optional)", required=False, default="None")
parser.add_argument("-exp", "--exception_domain_name", type=str, help="Domain name to add to the exception list (optional)", required=False, default="None")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output mode")

# Parse command-line arguments
args = parser.parse_args()

# Assign arguments to variables
trunk_name = args.name
username = args.username
password = args.password
domain = args.domain
phone_number = args.phonenumber
exception = args.exception_domain_name
client_id = args.client_id  # Updated variable name
prefix = args.prefix
digits = len(str(prefix))
outboundproxy = args.outboundproxy

# Define braces for dynamic string formatting
brace1 = "{"
brace2 = "}"
first = "1"

# Add outbound proxy configuration if provided
sip_outbound = f"\noutboundproxy={outboundproxy}"

# Generate SIP register string
sip_register = f""" register => {username}:{password}@{domain}/{phone_number} """

# Initialize exception list with default values
exceptions_list = ["mango", "beeline", "mtt", "rt"]

# Add custom exception domain if provided
if exception != "None":
    exceptions_list.append(exception)

# Generate SIP peer configuration
sip_peer = f"""[{trunk_name}]
host={domain}
username={username}
secret={password}
fromdomain={domain}
type=peer
context=default
insecure=invite,port
disallow=all
allow= alaw
allow= g729
directmedia=no 
canreinvite=no
qualify= yes
port= 5060
dtmfmode=rfc2833  """

# Append outbound proxy configuration if provided
if outboundproxy != "None":
    sip_peer = sip_peer + sip_outbound

# Generate SIP dialplan for outgoing calls
sip_dialplan = f""" exten => _{prefix}X.,{first},Dial(SIP/{trunk_name}/${brace1}EXTEN:{digits}{brace2},600)"""

# Generate SIP dialplan for exceptions
sip_dialplan_exception = f""" exten => _{prefix}X.,1,Set(CALLERID(num)={username})
 exten => _{prefix}X.,n,Set(CALLERID(name)={username})
 exten => _{prefix}X.,n,Dial(SIP/{trunk_name}/${brace1}EXTEN:{digits}{brace2},600)
                          """

# Generate SIP dialplan for incoming calls
sip_dialplan_incoming = f""" exten => _{phone_number},{first},Dial(SIP/to_twintime/${brace1}EXTEN{brace2},600)"""

# Print generated configurations
print('\n' + '-' * 50)
print(sip_register)
print('\n' + '-' * 50)
print(sip_peer)
print('\n' + '-' * 50)

# Check if the domain matches any exceptions and adjust the dialplan
for e in exceptions_list:
    if domain.find(e) != -1:
        sip_dialplan = sip_dialplan_exception
        break

# Print client ID and domain
print(f"; {client_id}  {domain}")

# Print the dialplan for outgoing calls
print(sip_dialplan)
print('\n' + '-' * 50)

# Print the dialplan for incoming calls
print(sip_dialplan_incoming)
print('\n' + '-' * 50)