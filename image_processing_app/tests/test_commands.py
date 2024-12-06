from django.test import TestCase
from django.core.management import call_command
from image_processing_app.management.commands.process_files import process_files_in_directory
from pathlib import Path
import json

class ProcessFilesCommandTest(TestCase):
    def test_process_files_in_directory(self):
        directory = Path('/path/to/test/directory')
        log_file = Path('/path/to/test/log_file.json')
        process_files_in_directory(directory, log_file)
        # Add assertions to verify the expected behavior

    def test_insert_data_command(self):
        call_command('insert_data')
        # Add assertions to verify the expected behavior

    def test_load_vqis_command(self):
        call_command('load_vqis')
        # Add assertions to verify the expected behavior