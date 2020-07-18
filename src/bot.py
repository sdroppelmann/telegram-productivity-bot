import telepot
from telepot.loop import MessageLoop
import time
import sys


# main bot instance
class Bot:

    def __init__(self, args):
        self.running = True
        self.work_mode = False
        self.break_interval_min = 60
        self.time_since_break_min = 0
        self.time_seconds = 0
        self.token, self.user_id = self.parse_args(args)
        self.bot = telepot.Bot(self.token)
        self.send_message('Starting ProductivityBot...')
        MessageLoop(self.bot, self.handle).run_as_thread()

        while self.running:
            time.sleep(1)
            if self.work_mode:
                self.time_seconds += 1

                if self.time_seconds == 60:
                    self.time_since_break_min += 1
                    self.time_seconds = 0

                if self.time_since_break_min == self.break_interval_min:
                    self.time_since_break_min = 0
                    self.send_message("Hey, you have been working for " + str(self.break_interval_min) + " minutes, "
                                                                                                         "it's time "
                                                                                                         "for a break")

                    # handle any message that comes in chat

    def handle(self, msg):
        content = telepot.glance(msg)
        if content[0] == 'text':
            if str(content[2]) == self.user_id:
                command = msg['text']
                if str(command).startswith('/'):
                    self.process_command(msg['text'][1:])

    def process_command(self, command):
        command = str(command).lower()
        if str(command).startswith('workmode'):
            self.reset_time()
            mode = str(command).split(' ')
            if len(mode) > 1:
                if mode[1].lower() == 'on':
                    self.work_mode = True
                elif mode[1].lower() == 'off':
                    self.work_mode = False
            else:
                self.work_mode = not self.work_mode

            if self.work_mode:
                self.send_message('Work mode active, break interval is ' + str(self.break_interval_min) + ' minutes')
            else:
                self.send_message('Work mode is now inactive')

        if str(command).startswith('setbreakinterval'):
            try:
                interval = int(str(command).split(' ')[1])
                if interval < 1 or interval > 300:
                    self.send_message('Break interval must be an integer between 1 and 300')
                else:
                    self.break_interval_min = interval
                    self.reset_time()
                    self.send_message('Set break interval to ' + str(interval) + ' minutes')

            except ValueError:
                self.send_message('Break interval must be an integer between 1 and 300')

        if command == 'shutdown':
            self.running = False
            self.send_message('Shutting down ProductivityBot...')

    # send a text message in chat
    def send_message(self, message):
        self.bot.sendMessage(self.user_id, message)

    def reset_time(self):
        self.time_since_break_min = 0
        self.time_seconds = 0

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
