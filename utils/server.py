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

    def start(self):
        """
        Starts test server with stdout and stderr output to /dev/null
        """
        # FNULL = open(os.devnull, 'w')
        FNULL = open('server.out', 'w')
        command_line = ['python', 'server/server.py']
        self.process = subprocess.Popen(command_line, shell=False,
                                        stdout=FNULL, stderr=FNULL)
        self.wait_for_server_to_start()

    def stop(self):
        """
        Shutdown test server child process
        """
        self.process.terminate()

    def wait_for_server_to_start(self, timeout=5):
        """
        Waits for server process to start
        Raises Exception if server didn't start
        TODO: create exceptions class and rais smth like ServerError
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
