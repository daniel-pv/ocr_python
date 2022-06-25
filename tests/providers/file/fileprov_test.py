import sys
from unittest.mock import MagicMock, mock_open, patch
sys.path.insert(1, 'c:\\Users\\daniel.pacheco\\Documents\\katas_python\\src')
from src.providers.file.fileprov import FileProvider
from providers.providerAdapter import ProviderAdapter
import os
import unittest
import builtins


class TestFileProvider():
    file_path = os.path.dirname(__file__)
    file_provider = FileProvider(file_path)

    def test_read_file_linebyline(self):
        file_name = 'data/test_data_read.txt'
        content = ['Lorem ipsum dolor sit amet, consectetuer adipiscing elit.']
        read_content = self.file_provider.read(file_name)
        assert read_content == content

    def test_write_file_content(self):
        file_name = 'data/test_data_write.txt'
        content = [
            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.",
            "Aliquam tincidunt mauris eu risus.",
            "Vestibulum auctor dapibus neque."]
        self.file_provider.write(content, file_name)
        read_content = self.file_provider.read(file_name)
        assert read_content == content

    def test_read_file_readline(self):
        file_path = os.path.dirname(__file__)
        file_name = 'data/test_data_read.txt'
        with patch('builtins.open', unittest.mock.mock_open()) as mock:
            data_reader = FileProvider(folder_path=file_path)
            data_reader.read(file_name=file_name)

        assert os.path.exists(file_path)
        mock.assert_called_once_with('{}/{}'.format(file_path, file_name), 'r')
        handle = mock()
        handle.readline.assert_called()

    def test_write_file_writelines(self):
        file_path = os.path.dirname(__file__)
        file_name = 'data/test_data_write.txt'
        lines = [
            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.",
            "Aliquam tincidunt mauris eu risus.",
            "Vestibulum auctor dapibus neque."]
        with patch('builtins.open', unittest.mock.mock_open()) as mock:
            data_reader = FileProvider(folder_path=file_path)
            data_reader.write(
                lines=lines,
                file_name=file_name)

        assert os.path.exists(file_path)
        mock.assert_called_once_with('{}/{}'.format(file_path, file_name), 'w')
        handle = mock()
        handle.writelines.assert_called()
