import threading

from db.dbHandler import DbHandler
from monitors.processMonitor import ProcessMonitor

if __name__ == '__main__':
    pm = ProcessMonitor()
    db_handler = DbHandler()
    thread_pm = threading.Thread(target=pm.monitor())
    thread_db = threading.Thread(target=db_handler.launch())
