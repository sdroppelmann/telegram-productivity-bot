import telepot
from telepot.loop import MessageLoop
import time
import sys


class Bot:

    def __init__(self, args):

        self.commands = {
            'workmode':         self.process_work_mode,
            'setbreakinterval': self.process_break_interval,
            'shutdown':         self.process_shutdown,
            'status':           self.process_status,
            'continue':         self.process_continue
        }

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
            self.next_second()

        self.send_message('Shutting down ProductivityBot...')

    # parse token and user id
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

    def next_second(self):
        if self.work_mode:
            self.time_seconds += 1

            if self.time_seconds == 60:
                self.time_since_break_min += 1
                self.time_seconds = 0

            if self.time_since_break_min == self.break_interval_min:
                self.time_since_break_min = 0
                self.work_mode = False
                message = "Hey, you have been working for " + str(self.break_interval_min)
                message += " minutes, it's time for a break."
                message += ' If you want to continue, hit me up with a /continue'
                self.send_message(message)

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
        command_args = command.split(' ')
        command_name = command_args[0]
        if command_name in self.commands.keys():
            self.commands[command_name](command)
        else:
            self.send_message('Unknown command: ' + command)

    def process_status(self, command):
        message = 'Work mode ' + ('active' if self.work_mode else 'inactive') + ', break interval is '
        message += str(self.break_interval_min) + ' minutes, ' + str(self.time_since_break_min)
        message += ' minutes and ' + str(self.time_seconds) + ' seconds, since last break'
        self.send_message(message)

    def process_shutdown(self, command):
        self.running = False

    def process_break_interval(self, command):
        try:
            args = str(command).split(' ')
            if len(args) != 2:
                self.send_break_interval_usage()

            interval = int(args[1])
            if interval < 1 or interval > 300:
                self.send_break_interval_usage()
            else:
                self.break_interval_min = interval
                self.reset_time()
                self.send_message('Set break interval to ' + str(interval) + ' minutes')
                if self.work_mode:
                    self.send_message('Work mode was active, restarting timer')

        except ValueError:
            self.send_break_interval_usage()

    def process_work_mode(self, command):
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

    def process_continue(self, command):
        self.process_work_mode('workmode on')

    def send_break_interval_usage(self):
        self.send_message('Break interval must be an integer between 1 and 300')

    # send a text message in chat
    def send_message(self, message):
        self.bot.sendMessage(self.user_id, message)

    def reset_time(self):
        self.time_since_break_min = 0
        self.time_seconds = 0


# init bot
Bot(sys.argv)
