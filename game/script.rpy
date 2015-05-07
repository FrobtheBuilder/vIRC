init python:
   import irc.client
   import time
   #import socks
   import json
   import os

   for fname in os.listdir(config.gamedir + '/img'):
      if fname.endswith(('.jpg', '.png')):
         tag = fname[:-4]
         fname =  'img/' + fname
   renpy.image(tag, fname)

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

# The game starts here.
label start:
   python:
      #socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, 'localhost', 666)
      #socks.wrapmodule(irc.client)
      reactor = irc.client.Reactor()
      c = reactor.server().connect(
            server,
            port,
            nick,
            password=passwd,
            connect_factory=irc.connection.Factory(),
         )
      kkk = renpy.get_widget("main_menu", "innn")

      reactor.add_global_handler("pubmsg", on_pubmsg)

   show loop

label base:
   "silence" "..."
   jump base