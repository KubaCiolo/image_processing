import argparse
from pathlib import Path
from agh_vqis import process_single_mm_file, VQIs
import json

def extract_parent_dir_name(file_path):
    parent_dir_name = file_path.parent.name
    parent_dir_substring = parent_dir_name.split()[1][:7]
    return parent_dir_substring

def load_processed_files(log_file):
    if log_file.exists():
        with open(log_file, 'r') as f:
            return set(json.load(f))
    return set()

def save_processed_files(log_file, processed_files):
    with open(log_file, 'w') as f:
        json.dump(list(processed_files), f)

def process_files_in_directory(directory, log_file):
    print(f"Initializing VQIs processor")
    vqis_processor = VQIs()  # Initialize the VQIs processor
    directory_path = Path(directory)
    output_dir = Path(r"C:\Users\jakub_lk\OneDrive\.inżynierka\data1")
    
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load the list of processed files
    processed_files = load_processed_files(log_file)
    
    print(f"Processing files in directory: {directory}")
    for file_path in directory_path.glob("*.jpg"):  # Adjust the pattern if needed
        print(f"Checking file: {file_path}")
        if str(file_path) in processed_files:
            print(f"Skipping {file_path}: Already processed")
            continue
        
        try:
            # Extract the parent directory substring
            parent_dir_substring = extract_parent_dir_name(file_path)
            
            # Define the output file path
            output_file = output_dir / f"VQIs_{parent_dir_substring}_for_{file_path.stem}.csv"
            
            # Check if the output file already exists
            if output_file.exists():
                print(f"Skipping {file_path}: Output file already exists")
                processed_files.add(str(file_path))
                save_processed_files(log_file, processed_files)
                continue
            
            # Process the file
            try:
                print(f"Processing file: {file_path}")
                result = process_single_mm_file(file_path, vqis_processor)
            except Exception as e:
                print(f"Skipping {file_path}: Error during processing - {e}")
                processed_files.add(str(file_path))
                save_processed_files(log_file, processed_files)
                continue
            
            # Move the generated CSV file to the specified output directory
            generated_file = Path.cwd() / f"VQIs_for_{file_path.stem}.csv"
            if generated_file.exists():
                generated_file.rename(output_file)
            else:
                print(f"Error: Expected output file {generated_file} not found.")
            
            print(f"Processed {file_path}: {result}")
            print(f"Output saved to {output_file}")
            
            # Mark the file as processed
            processed_files.add(str(file_path))
            save_processed_files(log_file, processed_files)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            processed_files.add(str(file_path))
            save_processed_files(log_file, processed_files)
        
        # Clean up any unexpected directories
        for item in Path.cwd().iterdir():
            if item.is_dir() and len(item.name) == 36 and '-' in item.name:
                print(f"Removing unexpected directory: {item}")
                for sub_item in item.iterdir():
                    sub_item.unlink()
                item.rmdir()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process multimedia files in a specified directory using AGH VQIs.")
    parser.add_argument("path", type=str, help="Path to the directory containing multimedia files to be processed")
    args = parser.parse_args()

    directory = Path(args.path)
    log_file = Path("processed_files_log.json")
    process_files_in_directory(directory, log_file)