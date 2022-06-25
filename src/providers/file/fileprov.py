import os.path
import logging
from providers.providerAdapter import ProviderAdapter
from xmlrpc.client import boolean
script_dir = os.path.dirname(__file__)


class FileProvider(ProviderAdapter):
    def __init__(self, folder_path=''):
        if folder_path == '':
            folder_path = script_dir
        self.folder_path = folder_path

    def read(self, file_name: str) -> list:
        lines = []
        file_path = '{}/{}'.format(self.folder_path, file_name)
        exist_file = os.path.exists(file_path)

        if exist_file:
            with open(file_path, 'r') as file:
                line = ' '
                while line:
                    line = file.readline()
                    if line == '':
                        break
                    lines.append(line.rstrip())
        else:
            logging.error('File was not found in directory!')
            lines = None

        return lines

    def write(self, lines, file_name: str) -> boolean:
        written = False
        file_path = '{}/{}'.format(self.folder_path, file_name)
        exist_file = os.path.exists(file_path)

        if exist_file:
            with open(file_path, 'w') as file:
                file.writelines(line + '\n' for line in lines)
                written = True
        else:
            logging.error('File was not found in directory!')

        return written
