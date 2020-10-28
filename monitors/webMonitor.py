from scapy.all import *
from scapy.layers.http import HTTPRequest

from db.dbHandler import DbHandler


class WebMonitor:
    def __new__(cls, *args, **kwargs):
        if not hasattr(WebMonitor, '__instance'):
            setattr(WebMonitor, '__instance', super(WebMonitor, cls).__new__(cls))
        return getattr(WebMonitor, '__instance')

    @staticmethod
    def _sniff_packets():
        sniff(filter="port 443", prn=WebMonitor._process_packet, store=False)

    @staticmethod
    def _process_packet(pck):
        db_handler = DbHandler()
        if pck.haslayer(HTTPRequest):
            dns_name = pck[HTTPRequest].Host.decode()  # DNS host's name
            print(dns_name)
            db_handler.inc_web_duration(dns_name, 1)

    def monitor(self):
        WebMonitor._sniff_packets()

    # toDo Sniffing HTTPS requests
