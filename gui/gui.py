import os
import subprocess
import tkinter
from datetime import datetime
from tkinter import filedialog

BUTTON_WIDTH = 20
BUTTON_HEIGHT = 2

font_size = 14

dir_path = os.path.dirname(os.path.realpath(__file__))
log_cat_file_path = dir_path + "/" + str(datetime.now().microsecond) + ".txt"
ip = "0.0.0.0:5555"
package = "test"
log = ""
push_location = "/sdcard/amazon.sdktester.json"

top = tkinter.Tk()


def disconnect_call_back():
    console_log = subprocess.run(['adb', 'disconnect'], stdout=subprocess.PIPE)
    convert_to_str(console_log)


def devices_call_back():
    console_log = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
    convert_to_str(console_log)


def connect_call_back():
    global ip
    ip = entry.get()
    ip_value['text'] = ip + ":5555"
    console_log = subprocess.run(['adb', 'connect', ip], stdout=subprocess.PIPE)
    convert_to_str(console_log)


def reboot_call_back():
    subprocess.run(['adb', 'reboot'], stdout=subprocess.PIPE)


def pick_apk_callback():
    if is_device_connected():
        filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        global package
        package = subprocess.run(
            ['aapt', 'dump', 'badging', filename],
            stdout=subprocess.PIPE
        )
        std_out = str(package.stdout)
        if std_out:
            package = std_out.split("versionCode")[0]
            package = package.split("'")[1]
            package_value['text'] = package
            subprocess.run(
                ['adb', 'install', filename],
                stdout=subprocess.PIPE)

        else:
            print("failed")
    else:
        log_value['text'] = "No devices found"


def push_file_callback():
    if is_device_connected():
        filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        subprocess.run(
            ['adb', 'push', filename, push_location],
            stdout=subprocess.PIPE)
    else:
        log_value['text'] = "No devices found"


def uninstall_call_back():
    if is_device_connected():
        if package != "test":
            console_log = subprocess.run(['adb', 'uninstall', package], stdout=subprocess.PIPE)
            convert_to_str(console_log)
        elif entry_package.get():
            console_log = subprocess.run(['adb', 'uninstall', entry_package.get()], stdout=subprocess.PIPE)
            convert_to_str(console_log)
        else:
            log_value['text'] = "Incorrect package name test"
    else:
        log_value['text'] = "No devices found"


def log_cat_to_file_callback():
    if is_device_connected():
        global log_cat_file_path
        log_cat_file_path = dir_path + "/" + str(datetime.now().microsecond) + ".txt"
        with open(log_cat_file_path, "wb", 0) as out:
            log_cat_stop['state'] = 'normal'
            global proc
            proc = subprocess.Popen('adb logcat', stdout=out, shell=True)
            log_value['text'] = "Logging to" + log_cat_file_path
    else:
        log_value['text'] = "No devices found"


def log_cat_stop_to_file_callback():
    global proc
    proc.terminate()
    global log_cat_file_path
    log_value['text'] = "Logging stopped " + log_cat_file_path
    log_cat_stop['state'] = 'disabled'


def clear_call_back():
    console_log = subprocess.run(['adb', 'shell', 'pm', 'clear', package], stdout=subprocess.PIPE)
    convert_to_str(console_log)


def convert_to_str(input_val):
    log_value['text'] = str(input_val.stdout)


def is_device_connected():
    console_log = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
    val = str(console_log.stdout)
    return val.__len__() > 35  # hacky to fix


# UI for label and  button
font_style = ('Helvetica', font_size, 'bold')
label = tkinter.Label(top, text=" Enter TV IP:: ", font=font_style)
label.grid(row=0, column=0)

entry = tkinter.Entry(top)
entry.grid(row=0, column=1)

connect = tkinter.Button(top, text="ADB connect", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=connect_call_back)
connect.grid(row=0, column=2)
pick = tkinter.Button(top, bg="#000000", text=" ADB install ", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      command=pick_apk_callback)
pick.grid(row=2, column=0)

disconnect = tkinter.Button(top, bg="#000000", text=" ADB disconnect ", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                            command=disconnect_call_back)
disconnect.grid(row=2, column=2)

reboot = tkinter.Button(top, bg="#000000", text=" ADB reboot ", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                        command=reboot_call_back)
reboot.grid(row=4, column=0)
clear = tkinter.Button(top, bg="#000000", text=" ADB clear ", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                       command=clear_call_back)
clear.grid(row=4, column=1)

push = tkinter.Button(top, bg="#000000", text=" ADB push ", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                       command=push_file_callback)
push.grid(row=4, column=2)

devices = tkinter.Button(top, bg="#000000", text=" ADB devices ", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                         command=devices_call_back)
devices.grid(row=2, column=1)
uninstall = tkinter.Button(top, bg="#000000", text=" ADB uninstall ", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                           command=uninstall_call_back)

log_cat = tkinter.Button(top, bg="#000000", text=" ADB logcat ", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                         command=log_cat_to_file_callback)
log_cat.grid(row=6, column=0)
log_cat_stop = tkinter.Button(top, bg="#000000", text=" ADB logcat stop ", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                              state="disabled",
                              command=log_cat_stop_to_file_callback)
log_cat_stop.grid(row=6, column=1)

uninstall.grid(row=7, column=0)
entry_package = tkinter.Entry(top)
entry_package.grid(row=7, column=1)
ip_label = tkinter.Label(top, text=" IP::", font=font_style)
ip_label.grid(row=8, column=0)
ip_value = tkinter.Label(top, text=ip)
ip_value.grid(row=8, column=1)
package_label = tkinter.Label(top, text=" Package Name::", font=font_style)
package_label.grid(row=9, column=0)
package_value = tkinter.Label(top, text=package)
package_value.grid(row=9, column=1)
numberOfScreenUnits = 100
log_label = tkinter.Label(top, text=" Log::", font=font_style, wraplength=numberOfScreenUnits)
log_label.grid(row=10, column=0)
log_value = tkinter.Label(top, text=log)
log_value.grid(row=10, column=1)

top.mainloop()
