import os
from django.core.management.base import BaseCommand
from image_processing_app.utils import process_images

class Command(BaseCommand):
    help = 'Process images from specified directories'

    def handle(self, *args, **kwargs):
        directories = [
            r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-01-01 to 2023-01-31_3724PDFs_pictures",
            r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-02-01 to 2023-02-28_3063PDFs_pictures",
            r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-03-01 to 2023-03-31_1992PDFs_pictures",
            r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-04-01 to 2023-04-30_5507PDFs_pictures",
            r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-05-01 to 2023-05-31_1971PDFs_pictures",
            r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-06-01 to 2023-06-30_2198PDFs_pictures",
            r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-09-01 to 2023-09-15_329PDFs_pictures",
            r"C:\Users\jakub_lk\OneDrive\.inżynierka\Es_pdfs(Art2)\From 2023-09-16 to 2023-09-30_8750PDFs_pictures"
        ]

        for directory in directories:
            if not os.path.isdir(directory):
                self.stderr.write(self.style.ERROR(f'Directory {directory} does not exist'))
                continue

        process_images(directories)