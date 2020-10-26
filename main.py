import threading

from db.dbHandler import DbHandler
from monitors.processMonitor import ProcessMonitor
from monitors.webMonitor import WebMonitor

if __name__ == '__main__':
    pm = ProcessMonitor()
    wm = WebMonitor()
    db_handler = DbHandler()

    thread_pm = threading.Thread(target=pm.monitor)
    print('Process Monitor started')
    thread_pm.start()

    thread_db = threading.Thread(target=db_handler.launch)
    print('Db handler started')
    thread_db.start()

    thread_wm = threading.Thread(target=wm.monitor)
    print('Web Monitor started')
    thread_wm.start()
