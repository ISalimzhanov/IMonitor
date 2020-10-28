import threading
import argparse
from db.dbHandler import DbHandler
from monitors.mitm import MITM
from monitors.processMonitor import ProcessMonitor
from monitors.webMonitor import WebMonitor

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-victim_ip', help='victim ip', type=str)
    parser.add_argument('-router_ip', help="router's ip", type=str)
    args = parser.parse_args()

    mitm = MITM(victim_ip=args.victim_ip, router_ip=args.router_ip)
    pm = ProcessMonitor()
    wm = WebMonitor()
    db_handler = DbHandler()

    thread_mitm = threading.Thread(target=mitm.launch)
    print('MITM started')
    thread_mitm.start()

    thread_pm = threading.Thread(target=pm.monitor)
    print('Process Monitor started')
    thread_pm.start()

    thread_db = threading.Thread(target=db_handler.launch)
    print('Db handler started')
    thread_db.start()

    thread_wm = threading.Thread(target=wm.monitor)
    print('Web Monitor started')
    thread_wm.start()
