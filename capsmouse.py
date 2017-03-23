#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division,print_function,absolute_import,unicode_literals
import sys
import os
os.chdir(sys.path[0])
sys.path.append("LTsv")
#from LTsv_printf import *
from LTsv_file   import *
#from LTsv_time   import *
#from LTsv_calc   import *
#from LTsv_joy    import *
from LTsv_kbd    import *
from LTsv_gui    import *

capsmouse_ltsvname,capsmouse_ltsvtext,capsmouse_config,capsmouse_kbdconfig="capsmouse.tsv","","",""
capsmouse_windowW,capsmouse_windowH=320,240
capsmouse_notifyname="capsmouse_notify.png"
capsmouse_wait=1000
capsmouse_KBD=0
capsmouse_polar,capsmouse_move,capsmouse_accel=0,20,0
capsmouse_NXkbd={}
capsmouse_mouseLCRcount=3
capsmouse_keepLCRaf=[False for mousecount in range(capsmouse_mouseLCRcount+1)]
capsmouse_keepLCRbf=[False for mousecount in range(capsmouse_mouseLCRcount+1)]

capsmouse_getkbdnamesBF,capsmouse_getkbdnamesAF="",""
def capsmousenotify_timeK(callback_void=None,callback_ptr=None):
    global capsmouse_getkbdnamesBF,capsmouse_getkbdnamesAF
    global capsmouse_keepLCRbf,capsmouse_keepLCRaf
    global capsmouse_polar,capsmouse_move,capsmouse_accel
    LTsv_setkbddata(20,10); capsmouse_getkbdnamesAF=LTsv_getkbdnames()
    capsmouse_kbdbuf=""
    if capsmouse_KBD != 0 and capsmouse_getkbdnamesBF != capsmouse_getkbdnamesAF:
        for NXcmd,NXkbd in capsmouse_NXkbd.items():
            for kbd in NXkbd:
                if not kbd in capsmouse_getkbdnamesAF: break;
            else:
                NXcmds=NXcmd.split(' ')
                if NXcmds[0] == "updown":
                    capsmouse_keepLCRaf[int(NXcmds[1])]=True
                elif NXcmds[0] == "polar":
                    capsmouse_polar=int(NXcmds[1])%360
                    LTsv_subprocess("xdotool mousemove_relative --polar {0} {1}".format(capsmouse_polar,NXcmds[-1]))
                elif NXcmds[0] == "capspolar":
                    capsmouse_keepLCRaf[0]=True
                    if capsmouse_keepLCRbf[0] != capsmouse_keepLCRaf[0]:
                        capsmouse_polar=(capsmouse_polar+int(NXcmds[1]))%360
                        capsmouse_move=int(NXcmds[-1])
                        capsmouse_accel=0
                    else:
                        capsmouse_accel+=2
                    LTsv_subprocess("xdotool mousemove_relative --polar {0} {1}".format(capsmouse_polar,capsmouse_move+capsmouse_accel))
                elif NXcmds[0] == "key":
                    LTsv_subprocess("xdotool key {0}".format(NXcmds[1]))
    for mousecount in range(capsmouse_mouseLCRcount+1):
        if capsmouse_keepLCRbf[mousecount] != capsmouse_keepLCRaf[mousecount]:
            capsmouse_keepLCRbf[mousecount]=capsmouse_keepLCRaf[mousecount]
            if mousecount > 0:
                if capsmouse_keepLCRaf[mousecount]:
                     LTsv_subprocess("xdotool mousedown {0}".format(mousecount))
                else:
                     LTsv_subprocess("xdotool mouseup {0}".format(mousecount))
        capsmouse_keepLCRaf[mousecount]=False
    LTsv_widget_settext(capsmouse_window,widget_t="capsmouse:"+capsmouse_kbdbuf)
    LTsv_window_after(capsmouse_window,event_b=capsmousenotify_timeK,event_i="capsmousenotify_timeK",event_w=capsmouse_wait)

def capsmouse_configload():
    global capsmouse_ltsvname,capsmouse_ltsvtext,capsmouse_config
    global capsmouse_notifyname,capsmouse_wait,capsmouse_KBD
    global capsmouse_kbdconfig,capsmouse_NXkbd
    capsmouse_ltsvtext=LTsv_loadfile(capsmouse_ltsvname)
    capsmouse_config=LTsv_getpage(capsmouse_ltsvtext,"capsmouse")
    capsmouse_wait=min(max(LTsv_intstr0x(LTsv_readlinerest(capsmouse_config,"wait",str(capsmouse_wait))),10),1000)
    capsmouse_notifyname=LTsv_readlinerest(capsmouse_config,"notify",capsmouse_notifyname)
    capsmouse_KBD=min(max(LTsv_intstr0x(LTsv_readlinerest(capsmouse_config,"KBD",str(capsmouse_KBD))),0),1)
    capsmouse_capsturn=min(max(LTsv_intstr0x(LTsv_readlinerest(capsmouse_config,"KBD",str(capsmouse_KBD))),0),360)
    capsmouse_kbdconfig=LTsv_getpage(capsmouse_ltsvtext,"capskbd")
    for capsmouse_kbdconfigline in capsmouse_kbdconfig.split('\n'):
        if len(capsmouse_kbdconfigline) == 0 or not '\t' in capsmouse_kbdconfigline: continue;
        if not ' ' in capsmouse_kbdconfigline.split('\t')[0]: continue;
        capsmouse_NXkbd[capsmouse_kbdconfigline.split('\t')[0]]=capsmouse_kbdconfigline.split('\t')[1:]

def capsmouse_menu():
    yield ("exit capsmouse",capsmouse_exit_cbk)
    yield ("",None)
    yield ("on",capsmouse_on_cbk)
    yield ("off",capsmouse_off_cbk)


def capsmouse_view(KBD=None):
    global capsmouse_KBD
    global capsmouse_keepLCRbf,capsmouse_keepLCRaf
    if KBD != None:
        capsmouse_KBD=min(max(KBD,0),1)
        for mousecount in range(capsmouse_mouseLCRcount):
            capsmouse_keepLCRbf[mousecount],capsmouse_keepLCRaf[mousecount]=False,False
            LTsv_subprocess("xdotool mouseup {0}".format(mousecount+1))
    LTsv_widget_seturi(capsmouse_notifyicon,widget_u="{0}[{1}]".format(capsmouse_notifyname,capsmouse_KBD))
    LTsv_widget_settext(capsmouse_notifyicon,widget_t="capsmouse")

def capsmouse_switch(window_objvoid=None,window_objptr=None):
    if capsmouse_KBD:
        capsmouse_off()
    else:
        capsmouse_on()
capsmouse_switch_cbk=LTsv_CALLBACLTYPE(capsmouse_switch)

def capsmouse_off(window_objvoid=None,window_objptr=None):
    capsmouse_view(0)
capsmouse_off_cbk=LTsv_CALLBACLTYPE(capsmouse_off)

def capsmouse_on(window_objvoid=None,window_objptr=None):
    capsmouse_view(1)
capsmouse_on_cbk=LTsv_CALLBACLTYPE(capsmouse_on)

def capsmouse_exit(window_objvoid=None,window_objptr=None):
    LTsv_window_exit()
capsmouse_exit_cbk=LTsv_CALLBACLTYPE(capsmouse_exit)

LTsv_GUI=LTsv_guiinit()
if len(LTsv_GUI) > 0:
    LTsv_kbdinit("LTsv/LTsv_kbd.tsv",LTsv_initmouse=True)
    LTsv_hideondelete=LTsv_hideondelete_shell()
    if LTsv_global_Notify() == LTsv_GUI_GTK2:
        capsmouse_iconnameAF="capsmouse"
        capsmouse_window=LTsv_window_new(event_b=LTsv_hideondelete,widget_t=capsmouse_iconnameAF,widget_w=capsmouse_windowW,widget_h=capsmouse_windowH)
        capsmouse_configload()
        LTsv_label_new(capsmouse_window,widget_t=capsmouse_kbdconfig,widget_x=0,widget_y=0,widget_w=capsmouse_windowW,widget_h=capsmouse_windowH)
        LTsv_draw_picture_load(capsmouse_notifyname); LTsv_draw_picture_celldiv(capsmouse_notifyname,2,1)
        capsmouse_notifyicon=LTsv_notifyicon_new(capsmouse_window,widget_t=capsmouse_iconnameAF,widget_u="{0}[{1}]".format(capsmouse_notifyname,capsmouse_KBD),menu_b=capsmouse_menu(),menu_c=capsmouse_switch_cbk)
#        LTsv_widget_showhide(capsmouse_window,True)
        capsmousenotify_timeK()
        LTsv_window_main(capsmouse_window)


# Copyright (c) 2017 ooblog
# License: MIT
# https://github.com/ooblog/capsmouse/blob/master/LICENSE
