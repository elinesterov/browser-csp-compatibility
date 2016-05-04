import os
import subprocess
import requests
import time

from urlparse import urlparse

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
        target_url = 'http://{0}:{1}/ping'.format(self.address, self.port)
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

    def is_request_received(self, method, url, ignore_query=False):
        """
        Method checks if request to specific url has been received by
        server.
        if path_only set to True, then only query string will be ignored during
        comparison.
        Returns True if yes otherwise returns False
        """
        logs = self.get_new_log_messages()
        parsed_logs = self._parse_logs(logs)
        result = False
        for message in parsed_logs:
            if ignore_query:
                msg_url = urlparse(message['url'].lower()).path
            else:
                msg_url = message['url'].lower()

            if (method.lower() == message['method'].lower() and
               url.lower() == msg_url):
                result = True
        return result

    def update_log_pointer(self):
        """
        Method to update log read position in case you want to get latest
        logs. e.g. call it before your test to get server log's for test
        """
        with open(self.logfile_name, 'r') as f:
            f.seek(0, 2)
            self.log_pointer = f.tell()

    def get_new_log_messages(self):
        """
        Method to get new log messages from server log
        'new' means since last call for update_log_pointer
        """
        with open(self.logfile_name, 'r') as f:
            f.seek(self.log_pointer)
            messages = f.readlines()
            self.log_pointer = f.tell()
        return messages

    def _parse_logs(self, logs):
        """
        Method to parse log messages
        Returns array of dict for each log message, parsed by
        _parse_log_message method
        """
        parsed_logs = []
        for log_message in logs:
            parsed_logs.append(self._parse_log_message(log_message))
        return parsed_logs

    @staticmethod
    def _parse_log_message(log_message):
        """
        Method to parse log message from server log
        returns dict {'method': 'method_from_log_message',
                      'url': 'url_from_log_message'}
        """
        url = log_message.split(' ')[6]
        method = log_message.split(' ')[5][1:]
        return {'method': method,
                'url': url}
