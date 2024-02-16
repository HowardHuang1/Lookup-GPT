import os


def append_files_together(source_dir, output_file):
    """
    Recursively goes through every file in source_dir and appends them into one massive .txt file.

    Parameters:
    - source_dir: The directory to search files in.
    - output_file: The file where all the contents will be appended.
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(str(file_path).upper() + '\n' + infile.read() + '\n')
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")


# Example usage:
if __name__ == '__main__':
    source_directory = '/path/to/your/directory'  # Replace with the path to your directory
    output_text_file = '/path/to/output.txt'  # Replace with your desired output file path
    append_files_together(source_directory, output_text_file)
