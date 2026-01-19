import os
import requests
import re

def download_files_from_list():
    """
    Reads URLs from a specified text file and downloads each file.
    """
    # ! SPECIFT PATH
    file_path = "URLS.txt"

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist. Please check the path and try again.")
        return

    # Create a directory to save the downloaded files, if it doesn't exist
    download_dir = "downloaded_files"
    os.makedirs(download_dir, exist_ok=True)
    print(f"Files will be saved in the '{download_dir}' directory.")

    try:
        with open(file_path, 'r') as f:
            urls = f.readlines()

        if not urls:
            print("The provided text file is empty. No URLs to download.")
            return

        print(f"Found {len(urls)} URLs in the file. Starting download...")
        successful_downloads = 0
        failed_downloads = 0

        for url_line in urls:
            url = url_line.strip() # Remove leading/trailing whitespace and newline characters
            if not url: # Skip empty lines
                continue

            # Basic check for a valid URL format (can be expanded if needed)
            if not url.startswith(('http://', 'https://')):
                print(f"Skipping invalid URL (does not start with http/https): {url}")
                failed_downloads += 1
                continue

            try:
                # Extract filename from the URL
                # ! SPECIFT PATTERN
                match = re.search(r'([^/]+?)(?:_list)?\_thumb\.png', url)
                print(f"Extracted filename: {match.group(1) if match else 'unknown'}")
                filename = os.path.join(download_dir, match.group(1) + '.png') if match else os.path.join(download_dir, os.path.basename(url))

                print(f"Attempting to download: {url}")
                response = requests.get(url, stream=True)
                response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

                with open(filename, 'wb') as out_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        out_file.write(chunk)

                print(f"Successfully downloaded: {filename}")
                successful_downloads += 1

            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url}. Error: {e}")
                failed_downloads += 1
            except IOError as e:
                print(f"Failed to save file {filename}. Error: {e}")
                failed_downloads += 1
            except Exception as e:
                print(f"An unexpected error occurred for {url}. Error: {e}")
                failed_downloads += 1

        print("\n--- Download Summary ---")
        print(f"Successful downloads: {successful_downloads}")
        print(f"Failed downloads: {failed_downloads}")

    except FileNotFoundError:
        # This specific error should be caught by the initial os.path.exists check,
        # but included for robustness if file disappears between checks.
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")

# Run the download function when the script is executed
if __name__ == "__main__":
    download_files_from_list()
