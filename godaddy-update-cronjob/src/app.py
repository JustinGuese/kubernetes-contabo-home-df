import smtplib
import socket
from datetime import datetime
from email.mime.text import MIMEText
from os import environ
from pathlib import Path

from godaddypy import Account, Client
from requests import get

my_acct = Account(api_key=environ["GODADDY_PUBLIC_KEY"], api_secret=environ["GODADDY_SECRET"])
client = Client(my_acct)

SUBDOMAINS = environ["GODADDY_SUBDOMAINS"].split(",")
MAINDOMAIN = environ["GODADDY_MAINDOMAIN"]
TESTDOMAIN = SUBDOMAINS[0] + "." + MAINDOMAIN

if len(SUBDOMAINS) == 0:
    raise Exception("No domains submitted in env variable GODADDY_DOMAINS")
else:
    print("checking for domains: " + str(SUBDOMAINS))

def getCurrentGodaddyIP():
    entries = client.get_records(MAINDOMAIN)
    for entry in entries:
        if entry["name"] in SUBDOMAINS:
            return entry["data"]
    # else
    return None

def getCurrentDNSIP():
    return socket.getaddrinfo(TESTDOMAIN, 443)[0][4][0]

def getCurrentServerIP():
    return get('https://api.ipify.org').text

def saveLastIP(ip):
    with open("persistent/lastip.txt", "w") as f:
        f.write(ip)
        
def updateIP(ip):
    for domain in SUBDOMAINS:
        # domain += "." + MAINDOMAIN
        print("updating domain: " + domain)
        client.update_record_ip(ip, MAINDOMAIN, domain, "A")
        # client.add_record(MAINDOMAIN, {'data' : ip, 'name' : domain, 'type' : 'A', 'ttl' : 604800})
    print("success! all domains updated to: " + ip)
    saveLastIP(ip)

# storage for current ip
my_file = Path("persistent/lastip.txt")
if my_file.is_file():
    with open("persistent/lastip.txt", "r") as f:
        LAST_IP = f.read()
else:
    LAST_IP = getCurrentGodaddyIP()
    saveLastIP(LAST_IP)
    
# CLOUDFLARE_ZONES = environ["CLOUDFLARE_ZONES"].split(",")
# def cloudflareupdate(zoneid):
#     params = {'match':'all', 'type':"A"}
#     cf = CloudFlare.CloudFlare(email = environ["CLOUDFLARE_EMAIL"], token = environ["CLOUDFLARE_TOKEN"])
    
#     try:
#         dns_records = cf.zones.dns_records.get(zoneid, params=params)
#     except CloudFlare.exceptions.CloudFlareAPIError as e:
#         exit('/zones/dns_records %s - %d %s - api call failed' % (zoneid, e, e))
        
#     print("dns_records: " + str(dns_records))

# if 
def send_alert_email():
    my_file = Path("persistent/lastmail.txt")
    if my_file.is_file():
        with open("persistent/lastmail.txt", "r") as f:
            LAST_MAIL = f.read()
            LAST_MAIL = datetime.strptime(LAST_MAIL, "%d/%m/%Y")
        # i only want to send once per day
        if LAST_MAIL.date() != datetime.today().date():
            print("going to send mail bc we didnt do fuck", LAST_MAIL.date(), datetime.today().date())
            msg = MIMEText("your domain ip changed, but i cant update cloudflare. currently myopiagraph u fuck.", "plain")
            msg['Subject']=       "Domain IP Change!"
            msg['From']   = "info@datafortress.cloud" # some SMTP servers will do this automatically, not all
            s = smtplib.SMTP_SSL("smtppro.zoho.eu", 465)
            s.login(environ["EMAIL_USERNAME"], environ["EMAIL_PASSWORD"])
            try:
                s.sendmail("info@datafortress.cloud", ["info@datafortress.cloud"], msg.as_string())
            finally:
                s.close()
        else:
            print("wont send bc last mail was today", LAST_MAIL)
    with open("persistent/lastmail.txt", "w+") as f:
        f.write(datetime.today().strftime("%d/%m/%Y"))
# get current server IP and check if is the same
server_ip = getCurrentServerIP()
if server_ip != LAST_IP:
    print("GODADDY")
    print("Server IP has changed for {}".format(TESTDOMAIN))
    print("Current server IP: {}".format(server_ip))
    print("Current godaddy IP: {}".format(LAST_IP))
    # updateIP(server_ip)
    
    # print("\n\CLOUDFLARE")
    # cf = CloudFlare.CloudFlare(email = environ["CLOUDFLARE_EMAIL"], token = environ["CLOUDFLARE_TOKEN"])
    # zones = cf.zones.get()
    # for zone in zones:
    #     zone_id = zone['id']
    #     zone_name = zone['name']
    #     print("zone_id=%s zone_name=%s" % (zone_id, zone_name))
    # # for cf_zone in CLOUDFLARE_ZONES:
    # #     cloudflareupdate(cf_zone)
    send_alert_email()
    
else:
    print("all good")
