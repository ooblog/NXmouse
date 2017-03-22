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

NXmouse_ltsvname,NXmouse_ltsvtext,NXmouse_config,NXkbd_config="NXmouse.tsv","","",""
NXmouse_windowW,NXmouse_windowH=320,240
NXmouse_notifyname="NXmouse.png"
NXmouse_wait=1000
NXmouse_KBD=0
NXmouse_capspolar,NXmouse_capsmove=0,20
NXmouse_NXkbd={}
NXmouse_mouseLCRcount=3
NXmouse_keepLCRaf=[False for mousecount in range(NXmouse_mouseLCRcount+1)]
NXmouse_keepLCRbf=[False for mousecount in range(NXmouse_mouseLCRcount+1)]

NXmouse_getkbdnamesBF,NXmouse_getkbdnamesAF="",""
def NXmousenotify_timeK(callback_void=None,callback_ptr=None):
    global NXmouse_getkbdnamesBF,NXmouse_getkbdnamesAF
    global NXmouse_keepLCRbf,NXmouse_keepLCRaf
    global NXmouse_capspolar,NXmouse_capsmove
    LTsv_setkbddata(20,10); NXmouse_getkbdnamesAF=LTsv_getkbdnames()
    NXmouse_kbdbuf=""
    if NXmouse_KBD != 0 and NXmouse_getkbdnamesBF != NXmouse_getkbdnamesAF:
        for NXcmd,NXkbd in NXmouse_NXkbd.items():
            for kbd in NXkbd:
                if not kbd in NXmouse_getkbdnamesAF: break;
            else:
                NXcmds=NXcmd.split(' ')
                if NXcmds[0] == "updown":
                    NXmouse_keepLCRaf[int(NXcmds[1])]=True
                elif NXcmds[0] == "polar":
                    LTsv_subprocess("xdotool mousemove_relative --polar {0} {1}".format(NXcmds[1],NXcmds[-1]))
                elif NXcmds[0] == "capspolar":
                    NXmouse_keepLCRaf[0]=True
                    if NXmouse_keepLCRbf[0] != NXmouse_keepLCRaf[0]:
                        NXmouse_capspolar=(NXmouse_capspolar+int(NXcmds[1]))%360
                        NXmouse_capsmove=int(NXcmds[-1])
                    LTsv_subprocess("xdotool mousemove_relative --polar {0} {1}".format(NXmouse_capspolar,NXmouse_capsmove))
                elif NXcmds[0] == "key":
                    LTsv_subprocess("xdotool key {0}".format(NXcmds[1]))
    for mousecount in range(NXmouse_mouseLCRcount+1):
        if NXmouse_keepLCRbf[mousecount] != NXmouse_keepLCRaf[mousecount]:
            NXmouse_keepLCRbf[mousecount]=NXmouse_keepLCRaf[mousecount]
            if mousecount > 0:
                if NXmouse_keepLCRaf[mousecount]:
                     LTsv_subprocess("xdotool mousedown {0}".format(mousecount))
                else:
                     LTsv_subprocess("xdotool mouseup {0}".format(mousecount))
        NXmouse_keepLCRaf[mousecount]=False
    LTsv_widget_settext(NXmouse_window,widget_t="NXmouse:"+NXmouse_kbdbuf)
    LTsv_window_after(NXmouse_window,event_b=NXmousenotify_timeK,event_i="NXmousenotify_timeK",event_w=NXmouse_wait)

def NXmouse_configload():
    global NXmouse_ltsvname,NXmouse_ltsvtext,NXmouse_config
    global NXmouse_notifyname,NXmouse_wait,NXmouse_KBD
    global NXkbd_config,NXmouse_NXkbd
    NXmouse_ltsvtext=LTsv_loadfile(NXmouse_ltsvname)
    NXmouse_config=LTsv_getpage(NXmouse_ltsvtext,"NXmouse")
    NXmouse_wait=min(max(LTsv_intstr0x(LTsv_readlinerest(NXmouse_config,"wait",str(NXmouse_wait))),10),1000)
    NXmouse_notifyname=LTsv_readlinerest(NXmouse_config,"notify",NXmouse_notifyname)
    NXmouse_KBD=min(max(LTsv_intstr0x(LTsv_readlinerest(NXmouse_config,"KBD",str(NXmouse_KBD))),0),1)
    NXmouse_capsturn=min(max(LTsv_intstr0x(LTsv_readlinerest(NXmouse_config,"KBD",str(NXmouse_KBD))),0),360)
    NXkbd_config=LTsv_getpage(NXmouse_ltsvtext,"NXkbd")
    for NXkbd_configline in NXkbd_config.split('\n'):
        if len(NXkbd_configline) == 0 or not '\t' in NXkbd_configline: continue;
        if not ' ' in NXkbd_configline.split('\t')[0]: continue;
        NXmouse_NXkbd[NXkbd_configline.split('\t')[0]]=NXkbd_configline.split('\t')[1:]

def NXmouse_menu():
    yield ("exit NXmouse",NXmouse_exit_cbk)
    yield ("",None)
    yield ("on",NXmouse_on_cbk)
    yield ("off",NXmouse_off_cbk)


def NXmouse_view(KBD=None):
    global NXmouse_KBD
    global NXmouse_keepLCRbf,NXmouse_keepLCRaf
    if KBD != None:
        NXmouse_KBD=min(max(KBD,0),1)
        for mousecount in range(NXmouse_mouseLCRcount):
            NXmouse_keepLCRbf[mousecount],NXmouse_keepLCRaf[mousecount]=False,False
            LTsv_subprocess("xdotool mouseup {0}".format(mousecount+1))
    LTsv_widget_seturi(NXmouse_notifyicon,widget_u="{0}[{1}]".format(NXmouse_notifyname,NXmouse_KBD))
    LTsv_widget_settext(NXmouse_notifyicon,widget_t="NXmouse")

def NXmouse_switch(window_objvoid=None,window_objptr=None):
    if NXmouse_KBD:
        NXmouse_off()
    else:
        NXmouse_on()
NXmouse_switch_cbk=LTsv_CALLBACLTYPE(NXmouse_switch)

def NXmouse_off(window_objvoid=None,window_objptr=None):
    NXmouse_view(0)
NXmouse_off_cbk=LTsv_CALLBACLTYPE(NXmouse_off)

def NXmouse_on(window_objvoid=None,window_objptr=None):
    NXmouse_view(1)
NXmouse_on_cbk=LTsv_CALLBACLTYPE(NXmouse_on)

def NXmouse_exit(window_objvoid=None,window_objptr=None):
    LTsv_window_exit()
NXmouse_exit_cbk=LTsv_CALLBACLTYPE(NXmouse_exit)

LTsv_GUI=LTsv_guiinit()
if len(LTsv_GUI) > 0:
    LTsv_kbdinit("LTsv/LTsv_kbd.tsv",LTsv_initmouse=True)
    LTsv_hideondelete=LTsv_hideondelete_shell()
    if LTsv_global_Notify() == LTsv_GUI_GTK2:
        NXmouse_iconnameAF="NXmouse"
        NXmouse_window=LTsv_window_new(event_b=LTsv_hideondelete,widget_t=NXmouse_iconnameAF,widget_w=NXmouse_windowW,widget_h=NXmouse_windowH)
        NXmouse_configload()
        LTsv_label_new(NXmouse_window,widget_t=NXkbd_config,widget_x=0,widget_y=0,widget_w=NXmouse_windowW,widget_h=NXmouse_windowH)
        LTsv_draw_picture_load(NXmouse_notifyname); LTsv_draw_picture_celldiv(NXmouse_notifyname,2,1)
        NXmouse_notifyicon=LTsv_notifyicon_new(NXmouse_window,widget_t=NXmouse_iconnameAF,widget_u="{0}[{1}]".format(NXmouse_notifyname,NXmouse_KBD),menu_b=NXmouse_menu(),menu_c=NXmouse_switch_cbk)
#        LTsv_widget_showhide(NXmouse_window,True)
        NXmousenotify_timeK()
        LTsv_window_main(NXmouse_window)


# Copyright (c) 2017 ooblog
# License: MIT
# https://github.com/ooblog/NXmouse/blob/master/LICENSE
