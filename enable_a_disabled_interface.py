import requests
import json
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from jinja2 import Template
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError

url = 'https://notify-api.line.me/api/notify'
token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def getDeviceDetail(device_id):
    header = {"Content-Type":"application/json" ,"Accept" : "application/json" }
    parameter = { "working": True }
    #r=requests.get("https://xxx.xxx.xxx.xxx:8080/api/v2/config/device/"+device_id,params=parameter, headers=header,verify=False) # call from external
    r=requests.get("http://config-server:9000/api/v2/config/device/"+device_id,params=parameter, headers=header,verify=False) # call with internal
    print(r.url)
    return r.json()

def sendMessage(interface,host_ip,status):
    msg = 'At device ip: '+host_ip+" ,interfaces "+interface+" "+status
    r = requests.post(url, headers=headers, data = {'message':msg})


def getJunos_v2(interface, **kwargs):
    junos_details = getDeviceDetail(kwargs.get('device_id'))
    junos_host = junos_details['host']
    junos_user = 'root'
    junos_password = 'Juniper!1'
    device=Device(host=junos_host, user=junos_user, password=junos_password)
    device.open()
    cfg=Config(device)
    my_template = Template('delete interfaces {{ interface }} disable')
    cfg.load(my_template.render(interface=interface), format='set')
    cfg.commit()
    device.close()
    sendMessage(interface,junos_details['host'],"enable")

