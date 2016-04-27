import os
import subprocess
import requests
import time

from config import config


class Server(object):
    """
    Simple helper to start/stop and interact with a tests server
    TODO: add method to check what request has been send last by browser
    might need this for connect-src testing. To make sure nothing is send
    over network
    """
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.logfile_name = config['server_log_filename']
        self.log = None
        self.log_pointer = 0

    def start(self):
        """
        Starts test server with stdout and stderr output to /dev/null
        """
        FNULL = open(os.devnull, 'w')
        command_line = ['python', 'server/server.py']
        self.process = subprocess.Popen(command_line, shell=False,
                                        stdout=FNULL, stderr=FNULL)
        self.wait_for_server_to_start()
        self.clean_server_log()

    def stop(self):
        """
        Shutdown test server child process
        """
        self.process.terminate()

    def wait_for_server_to_start(self, timeout=5):
        """
        Waits for server process to start
        Raises Exception if server didn't start
        TODO: create exceptions class and raise smth like ServerError
        """
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.server_is_running():
                return True
            else:
                print('Waiting for start...')
                time.sleep(1)

        raise Exception('Cannot start server')

    def server_is_running(self):
        """
        Checks if server is running
        """
        target_url = 'http://{}:{}/ping'.format(self.address, self.port)
        try:
            response = requests.get(target_url, timeout=1)
        except Exception:
            return False
        if response.status_code == 200 and response.content == 'pong':
            return True
        else:
            print('Got unexpected response form server:')
            print('Status: {}\n Content: {}').format(response.status,
                                                     response.content)
            return False

    def clean_server_log(self):
        with open(self.logfile_name, 'w') as f:
            f.write('')
            f.close()

    def get_log_messages(self):
        """
        Method to get log messages from server log
        """
        with open(self.logfile_name, 'r') as f:
            f.seek(self.log_pointer)
            messages = f.readlines()
            self.log_pointer = f.tell()
        return messages

    def update_log_pointer(self):
        """
        Method to update log read position in case you want to get latest
        logs. e.g. call it before your test to get server log's for test
        """
        with open(self.logfile_name, 'r') as f:
            f.seek(0, 2)
            self.log_pointer = f.tell()
