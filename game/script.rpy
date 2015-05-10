init python:
   import os, sys
   sys.path.append(os.path.join(config.gamedir, "lib")) #set up path for main to use
   import main
   main.initialize(renpy)

label msg(sender="", message=""):
   python:
      renpy.show("anon")
      if "!" in sender:
         sendernick = sender.split("!")[0]
   "[sendernick]" "[message]"
   call msg(sender, message) from _call_msg

label start:
   $ main.start()

label base:
   "silence" "..."
   jump base