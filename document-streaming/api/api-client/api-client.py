import json
import requests
from typing import Generator, Dict, Any
import time


def read_lines_as_json(file_path: str) -> Generator[Dict[str, Any], None, None]:
    """
    Generator that reads a file line by line and yields JSON objects.
    
    Args:
        file_path: Path to the text file to read
        
    Yields:
        Dictionary containing the parsed JSON data or error information
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, start=1):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            try:
                # Parse the line as JSON
                json_data = json.loads(line)
                yield json_data
            except json.JSONDecodeError as e:
                print(f"Warning: Line {line_num} is not valid JSON: {e}")
                # Optionally yield the raw line wrapped in a JSON object
                yield {"error": "invalid_json", "line_number": line_num, "raw_data": line}


def post_json_to_endpoint(
    file_path: str,
    endpoint_url: str,
    delay_seconds: float = 0.1,
) -> None:
    """
    Reads a file line by line, converts each line to JSON, and posts to an endpoint.
    
    Args:
        file_path: Path to the text file to read
        endpoint_url: The API endpoint URL to post data to
        delay_seconds: Delay between requests (default: 0.1 seconds)
    """

    success_count = 0
    error_count = 0
    
    print(f"Starting to process file: {file_path}")
    print(f"Posting to endpoint: {endpoint_url}\n")
    
    # Use the generator to process the file
    for json_data in read_lines_as_json(file_path):
        try:
            # Post the JSON data to the endpoint
            response = requests.post(
                endpoint_url,
                json=json_data,
                timeout=10
            )
            
            # Check if the request was successful
            if response.status_code in [200, 201, 202]:
                success_count += 1
                print(f"✓ Successfully posted record {success_count} (Status: {response.status_code})")
            else:
                error_count += 1
                print(f"✗ Failed to post record (Status: {response.status_code}): {response.text}")
            
            # Add delay to avoid overwhelming the endpoint
            time.sleep(delay_seconds)
            
        except requests.exceptions.RequestException as e:
            error_count += 1
            print(f"✗ Request error: {e}")
        except Exception as e:
            error_count += 1
            print(f"✗ Unexpected error: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"Successful posts: {success_count}")
    print(f"Failed posts: {error_count}")
    print(f"Total processed: {success_count + error_count}")
    print(f"{'='*50}")


if __name__ == "__main__":
    # Configuration

    FILE_PATH = '../../data/ncr_ride_bookings.txt'  # Path to your text file
    ENDPOINT_URL = 'http://localhost:80/ride-booking'  # Update with your actual endpoint

    

    # Run the script
    try:
        post_json_to_endpoint(
            file_path=FILE_PATH,
            endpoint_url=ENDPOINT_URL,
            delay_seconds=0.1,  # Adjust delay as needed
        )
    except FileNotFoundError:
        print(f"Error: File '{FILE_PATH}' not found!")
    except Exception as e:
        print(f"Error: {e}")