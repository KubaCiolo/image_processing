import json

# Function to load headlines data
def load_headlines(file_path):
    headlines = {}
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Debugging statement to check the raw line
            print(f"Raw line: {line.strip()}")
            
            # Replace single quotes with double quotes for JSON compatibility
            line = line.replace("'", '"')
            
            # Debugging statement to check the modified line
            print(f"Modified line: {line.strip()}")
            
            try:
                entry = json.loads(line)
                if 'doc_filename' in entry and 'doc_headline' in entry and 'doc_url' in entry:
                    doc_filename = entry['doc_filename']
                    doc_headline = entry['doc_headline']
                    doc_url = entry['doc_url']
                    headlines[doc_filename] = {
                        'doc_headline': doc_headline,
                        'doc_url': doc_url
                    }
                    print(f"Loaded headline for {doc_filename}: {doc_headline}, {doc_url}")  # Debugging statement
                else:
                    print(f"Missing keys in line: {line.strip()}")  # Debugging statement
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Problematic line: {line.strip()}")  # Debugging statement
                continue
    return headlines

# Example usage
if __name__ == "__main__":
    headlines_file_path = r'C:\Users\jakub_lk\OneDrive\.inżynierka\image_processing\data\headlines(Art2).txt'
    headlines = load_headlines(headlines_file_path)
    print(f"Total headlines loaded: {len(headlines)}")