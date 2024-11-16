import logging
from pathlib import Path
from django.conf import settings
from agh_vqis.__main__ import process_single_mm_file
import argparse
import shutil
import glob

logger = logging.getLogger(__name__)

def process_image(image_path: Path, options=None):
    """
    Process an image using agh_vqis without invoking the CLI argument parser.
    
    :param image_path: Path to the image file to process
    :param options: Options for the executable file
    :return: Path to the output CSV file
    """
    logger.info(f"Processing image: {image_path}")
    if options is None:
        options = {}

    # Manually set up the arguments to avoid parsing command-line arguments
    args = argparse.Namespace(
        path=image_path,
        colourfulness=False,  # Explicitly disable colourfulness
        blur_amount=False,    # Explicitly disable blur amount
        ugc=False,            # Explicitly disable UGC
        exec=None,
        vqis=None             # Explicitly disable VQIs
    )

    # Call the process_single_mm_file function directly with the necessary arguments
    try:
        status = process_single_mm_file(args.path, cli=False, options=options, args=args)
        logger.info(f"process_single_mm_file returned status {status}")
    except Exception as e:
        logger.error(f"Exception in process_single_mm_file: {e}")
        raise

    if status != 0:
        logger.error(f"Error processing image: status {status}")
        raise Exception("Error processing image")

    logger.info(f"VQIS result file generated for {image_path}")

    # Find the generated CSV file
    generated_csv_files = glob.glob("VQIs_for_*.csv")
    if not generated_csv_files:
        logger.error("No CSV file generated")
        raise Exception("No CSV file generated")
    
    generated_csv_path = Path(generated_csv_files[0])

    # Define the path to save the output CSV file
    results_dir = Path(settings.MEDIA_ROOT) / 'results'
    results_dir.mkdir(parents=True, exist_ok=True)
    output_csv_path = results_dir / f"{image_path.stem}_results.csv"

    # Move the generated CSV file to the results directory
    try:
        shutil.move(str(generated_csv_path), str(output_csv_path))
    except Exception as e:
        logger.error(f"Error moving CSV file: {e}")
        raise

    return output_csv_path