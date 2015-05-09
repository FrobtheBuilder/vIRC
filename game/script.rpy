init python:
   
   import time
   import json
   import os, sys
   sys.path.append(os.path.join(config.gamedir, "lib")) #set up path for main to use
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
   call msg(sender, message) from _call_msg

image loop = DynamicDisplayable(event_loop)

label start:
   python:
      
      reactor = main.get_reactor()
      reactor.add_global_handler("pubmsg", on_pubmsg)

   show loop

label base:
   "silence" "..."
   jump base