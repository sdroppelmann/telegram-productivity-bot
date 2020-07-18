import telepot
from telepot.loop import MessageLoop
import time
import sys


# main bot instance
class Bot:

    def __init__(self, args):
        self.running = True
        self.token, self.user_id = self.parse_args(args)
        self.bot = telepot.Bot(self.token)
        self.send_message('Starting ProductivityBot...')
        MessageLoop(self.bot, self.handle).run_as_thread()
        while self.running:
            time.sleep(2)

    # handle any message that comes in chat
    def handle(self, msg):
        content = telepot.glance(msg)
        if content[0] == 'text':
            if str(content[2]) == self.user_id:
                command = msg['text']
                if str(command).startswith('/'):
                    self.process_command(msg['text'][1:])

    def process_command(self, command):
        self.send_message(command)

    # send a text message in chat
    def send_message(self, message):
        self.bot.sendMessage(self.user_id, message)

    def parse_args(self, args):
        token = None
        user_id = None
        for arg in args:
            arg_str = str(arg)
            if arg_str.startswith('token='):
                token = arg_str.split('=')[1]
            elif arg_str.startswith('userid='):
                user_id = arg_str.split('=')[1]

        if not token or not user_id:
            raise Exception('Bot must have a token and user id to start')
        else:
            return token, user_id


# init bot
Bot(sys.argv)
