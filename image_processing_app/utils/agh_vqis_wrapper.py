# image_processing_app/utils/agh_vqis_wrapper.py
import logging
from pathlib import Path
from agh_vqis.__main__ import process_single_mm_file

logger = logging.getLogger(__name__)

def process_image_without_cli(image_path: Path, options=None):
    """
    Wrapper function to process an image without invoking the CLI argument parser.
    
    :param image_path: Path to the image file to process
    :param options: Options for the executable file
    :return: Status, 0 if successful, 1 otherwise
    """
    logger.info(f"Processing image: {image_path}")
    if options is None:
        options = {}

    # Call the process_single_mm_file function directly with the necessary arguments
    try:
        status = process_single_mm_file(image_path, cli=False, options=options)
        logger.info(f"process_single_mm_file returned status {status}")
    except Exception as e:
        logger.error(f"Exception in process_single_mm_file: {e}")
        raise

    return status