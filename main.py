import sys
from auth import MiBand3
from cursesmenu import *
from cursesmenu.items import *
from constants import ALERT_TYPES
import time
import os
def call_immediate():
    print('Sending Call Alert')
    time.sleep(1)
    band.send_alert(ALERT_TYPES.PHONE)
def msg_immediate():
    print('Sending Message Alert')
    time.sleep(1)
    band.send_alert(ALERT_TYPES.MESSAGE)
def detail_info():
    print('MiBand')
    print('Soft revision:',band.get_revision())
    print('Hardware revision:',band.get_hrdw_revision())
    print('Serial:',band.get_serial())
    print('Battery:', band.get_battery_info())
    print('Time:', band.get_current_time())
    print('Steps:', band.get_steps())
    input('Press Enter to continue')
def custom_message():
    band.send_custom_alert(5)

def custom_call():
    # custom_call
    band.send_custom_alert(3)

def custom_missed_call():
    band.send_custom_alert(4)
def l(x):
    print('Realtime heart BPM:', x)

def heart_beat():
    band.start_raw_data_realtime(heart_measure_callback=l)
    input('Press Enter to continue')

def change_date():
    band.change_date()
MAC_ADDR = sys.argv[1]
print('Attempting to connect to ', MAC_ADDR)

def updateFirmware():
    fileName = input('Enter the file Name with Extension\n')
    band.dfuUpdate(fileName)

band = MiBand3(MAC_ADDR, debug=True)
band.setSecurityLevel(level = "medium")

# Authenticate the MiBand
if len(sys.argv) > 2:
    if band.initialize():
        print("Initialized...")
    band.disconnect()
    sys.exit(0)
else:
    band.authenticate()

# detail_info()

menu = CursesMenu("MiBand MAC: " + MAC_ADDR, "Select an option")
detail_menu = FunctionItem("View Band Detail info", detail_info)
call_notif = FunctionItem("Send a High Prority Call Notification", call_immediate)
msg_notif = FunctionItem("Send a Medium Prority Message Notification", msg_immediate)
msg_alert = FunctionItem("Send a Message Notification", custom_message)
call_alert = FunctionItem("Send a Call Notification", custom_call)
miss_call_alert = FunctionItem("Send a Missed Call Notification", custom_missed_call)
change_date_time = FunctionItem("Change Date and Time", change_date)
heart_beat_menu = FunctionItem("Get Heart BPM", heart_beat)
dfu_update_menu = FunctionItem("DFU Update", updateFirmware)

menu.append_item(detail_menu)
menu.append_item(call_notif)
menu.append_item(msg_notif)
menu.append_item(msg_alert)
menu.append_item(call_alert)
menu.append_item(change_date_time)
menu.append_item(miss_call_alert)
menu.append_item(heart_beat_menu)
menu.append_item(dfu_update_menu)
menu.show()
