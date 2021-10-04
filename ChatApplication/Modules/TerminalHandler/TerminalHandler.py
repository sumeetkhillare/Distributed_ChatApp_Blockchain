import urwid
import threading

def terminalHandlerMain(interactDeployObj,chatroomName, username):
    my_term = RoomTerminal(interactDeployObj,chatroomName,username)
    mainloop = urwid.MainLoop(my_term)
    my_term.loop=mainloop
    listenMsgThread = threading.Thread(target=my_term.getMsg)
    listenMsgThread.start()
    mainloop.run()



class RoomTerminal(urwid.WidgetWrap):
    def __init__(self, interactDeployObj, chatroomName, username):
        self.interactDeployObj = interactDeployObj
        loop=None
        self.chatRoomName = chatroomName
        self.username = username
        self.msgSize = 0
        self.screen_text = urwid.Text(self.chatRoomName + ' : ' + self.username)
        self.prompt_text = urwid.Edit(self.username + ': ', '')
        self._w = urwid.Frame(header=urwid.Pile([urwid.Text(self.chatRoomName),
                                                 urwid.Divider()]),
                              body=urwid.ListBox([self.screen_text]),
                              footer=self.prompt_text,
                              focus_part='footer')

    def getMsg(self):
        self.msgSize = len(self.interactDeployObj.callGetMessagesFromChatRoomByName(self.interactDeployObj.chatRoomName))
        while True:
            curr_msg = self.interactDeployObj.callGetMessagesFromChatRoomByName(self.interactDeployObj.chatRoomName)
            if self.msgSize < len(curr_msg):
                for i in range(self.msgSize, len(curr_msg)):
                    msg = curr_msg[i]
                    self.screen_text.set_text(self.screen_text.text +
                                              '\n' +
                                              msg[0] + ':' + msg[1])
                    self.loop.draw_screen()
                self.msgSize = len(curr_msg)

    def keypress(self, size, key):
        if key == 'esc':
            raise urwid.ExitMainLoop()
        if key == 'enter':
            query = self.prompt_text.edit_text
            msg = query
            sendMsg = threading.Thread(target=self.interactDeployObj.transactAddMessage, args=(self.chatRoomName, self.username, msg))
            sendMsg.start()
            self.prompt_text.edit_text = ''
            return
        super(RoomTerminal, self).keypress(size, key)
