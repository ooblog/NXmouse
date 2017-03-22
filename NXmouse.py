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

NXmouse_ltsvname,NXmouse_ltsvtext,NXmouse_config="NXmouse.tsv","",""
NXmouse_windowW,NXmouse_windowH=320,120
NXmouse_notifyname="NXmouse.png"
NXmouse_wait=1000
NXmouse_KBD=0
NXmouse_kbdLCR=["NFER","None","XFER"]
NXmouse_nameLCR=["kbdL","kbdC","kbdR"]
NXmouse_downLCR=["xdotool mousedown 1","xdotool mousedown 2","xdotool mousedown 3"]
NXmouse_upLCR=["xdotool mouseup 1","xdotool mouseup 2","xdotool mouseup 3"]
NXmouse_keepLCRbf=list(tuple(NXmouse_downLCR[:]))
NXmouse_keepLCRaf=list(tuple(NXmouse_downLCR[:]))
NXmouse_iconnameBF,NXmouse_iconnameAF="",""

def NXmousenotify_timeK(callback_void=None,callback_ptr=None):
    global NXmouse_iconnameBF,NXmouse_iconnameAF
    LTsv_setkbddata(20,10); glyphtype_getkbdnames=LTsv_getkbdnames()
    NXmouse_iconnameAF=glyphtype_getkbdnames
    if NXmouse_KBD != 0 and NXmouse_iconnameBF != NXmouse_iconnameAF:
        for kbdcount,kbdLCR in enumerate(NXmouse_kbdLCR):
            if kbdLCR in NXmouse_iconnameAF:
                NXmouse_keepLCRaf[kbdcount]=NXmouse_downLCR[kbdcount]
            else:
                NXmouse_keepLCRaf[kbdcount]=NXmouse_upLCR[kbdcount]
            if NXmouse_keepLCRbf[kbdcount] != NXmouse_keepLCRaf[kbdcount]:
                LTsv_subprocess(NXmouse_keepLCRaf[kbdcount])
                NXmouse_keepLCRbf[kbdcount] = NXmouse_keepLCRaf[kbdcount]
        LTsv_widget_settext(NXmouse_window,widget_t="NXmouse:"+NXmouse_iconnameAF)
        NXmouse_iconnameBF=NXmouse_iconnameAF
    LTsv_window_after(NXmouse_window,event_b=NXmousenotify_timeK,event_i="NXmousenotify_timeK",event_w=NXmouse_wait)

def NXmouse_configload():
    global NXmouse_ltsvname,NXmouse_ltsvtext,NXmouse_config
    global NXmouse_notifyname,NXmouse_wait,NXmouse_KBD
    global NXmouse_kbdLCR
    NXmouse_ltsvtext=LTsv_loadfile(NXmouse_ltsvname)
    NXmouse_config=LTsv_getpage(NXmouse_ltsvtext,"NXmouse")
    NXmouse_notifyname=LTsv_readlinerest(NXmouse_config,"notify",NXmouse_notifyname)
    NXmouse_wait=min(max(LTsv_intstr0x(LTsv_readlinerest(NXmouse_config,"wait",str(NXmouse_wait))),20),1000)
    NXmouse_KBD=min(max(LTsv_intstr0x(LTsv_readlinerest(NXmouse_config,"KBD",str(NXmouse_KBD))),0),1)
    for namecount,nameLCR in enumerate(NXmouse_nameLCR):
        NXmouse_kbdLCR[namecount]=LTsv_readlinerest(NXmouse_config,nameLCR,NXmouse_kbdLCR[namecount])

def NXmouse_menu():
    yield ("「NXmouse」の終了",NXmouse_exit_cbk)
    yield ("",None)
    yield ("「NXmouse」の停止",NXmouse_off_cbk)
    yield ("「NXmouse」の再開",NXmouse_on_cbk)


def NXmouse_view(KBD=None):
    global NXmouse_KBD
    if KBD != None:
        NXmouse_KBD=min(max(KBD,0),1)
        for kbdcount,kbdLCR in enumerate(NXmouse_kbdLCR):
            NXmouse_keepLCRaf[kbdcount]=NXmouse_upLCR[kbdcount]
            LTsv_subprocess(NXmouse_keepLCRaf[kbdcount])
            NXmouse_keepLCRbf[kbdcount] = NXmouse_keepLCRaf[kbdcount]
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
        LTsv_draw_picture_load(NXmouse_notifyname); LTsv_draw_picture_celldiv(NXmouse_notifyname,2,1)
        NXmouse_notifyicon=LTsv_notifyicon_new(NXmouse_window,widget_t=NXmouse_iconnameAF,widget_u="{0}[{1}]".format(NXmouse_notifyname,NXmouse_KBD),menu_b=NXmouse_menu(),menu_c=NXmouse_switch_cbk)
#        LTsv_widget_showhide(NXmouse_window,True)
        NXmousenotify_timeK()
        LTsv_window_main(NXmouse_window)


# Copyright (c) 2017 ooblog
# License: MIT
# https://github.com/ooblog/NXmouse/blob/master/LICENSE
