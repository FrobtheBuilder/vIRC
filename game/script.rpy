﻿init python:
   import irc.client
   import irc.connection
   import time
   #import socks
   import json
   import os
   import main

   main.initialize(renpy, config)

   def on_pubmsg(connection, event):
         renpy.call("msg", str(event.source), event.arguments[0])

   def event_loop(st, at):
         reactor.process_once(0.2)
         return Null(), 0.5
         
#image anon = im.Scale("anon.png", 250, 400)

label msg(sender="", message=""):
   show anon
   "[sender]" "[message]"
   call msg(sender, message)

image loop = DynamicDisplayable(event_loop)

label start:
   python:
      #socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, 'localhost', 666)
      #socks.wrapmodule(irc.client)
      reactor = irc.client.Reactor()
      c = reactor.server().connect(
            ircconf['server'],
            ircconf['port'],
            ircconf['nick'],
            password=ircconf['passwd'],
            connect_factory=irc.connection.Factory()
         )
      
      reactor.add_global_handler("pubmsg", on_pubmsg)

   show loop

label base:
   "silence" "..."
   jump base