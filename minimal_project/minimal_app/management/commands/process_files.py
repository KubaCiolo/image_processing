# minimal_app/management/commands/process_files.py

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Process PDF and image files'

    def handle(self, *args, **options):
        print("Command process_files is being executed")
        main_dir = 'C:\\Users\\jakub_lk\\OneDrive\\.inżynierka\\Es_pdfs(Art2)'
        print(f"Main directory: {main_dir}")
        self.stdout.write(self.style.SUCCESS('Successfully processed files'))