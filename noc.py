from noc.inv.models.interface import *
from noc.sa.models import *
from noc.ip.models import *
from math import asin
from noc.lib.text import split_alnum

router_gw=""
i = Interface.objects.filter(managed_object=context["object"].id, type="physical")
for interface in sorted(i, key=lambda x: split_alnum(x.name)):
    if "switch" in str(interface.description):
        router_gw = interface.name 
        break

region=""
ip=str(context["object"].address)
temp_ip=ip.split('.')
region=str(temp_ip[1])

context["cmd"]="configure terminal\n"

context["cmd"]+="ip vrf " + context["vrf"] + "\n"
context["cmd"]+="description --" + context["vrf"] + "--\n"
context["cmd"]+="rd 65000:" + context["vrf_num"] + "\n"
context["cmd"]+="route-target export 65000:" + context["vrf_num"] + "\n"
context["cmd"]+="route-target import 65000:" + context["vrf_num"] + "\n"
context["cmd"]+="exit\n"

context["cmd"]+="router bgp 65000\n"
context["cmd"]+="address-family ipv4 vrf " + context["vrf"] + "\n"
context["cmd"]+="redistribute connected\n"
context["cmd"]+="exit\n exit\n"

context["cmd"] += "interface " + router_gw + "." + context["vrf_num"] + "\n"
context["cmd"]+="description --" + context["vrf"] + "_gw--\n"
context["cmd"]+="encapsulation dot1Q " + context["vrf_num"] + "\n"
context["cmd"]+="ip vrf forwarding " + context["vrf"] + "\n"
context["cmd"]+="ip address 10." + context["vrf_num"] + "." + region + ".1 255.255.255.0\n"
context["cmd"]+="no ip redirects\n"
context["cmd"]+="no ip unreachables\n"
context["cmd"]+="no ip proxy-arp\n"
context["cmd"]+="ip flow ingress\n"
context["cmd"]+="ip flow egress\n"
context["cmd"]+="ip virtual-reassembly in\n"
context["cmd"]+="no cdp enable\n"
context["cmd"]+="end\n"