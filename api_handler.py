import requests
import json
import logging
import os
import asyncio
import ast


class APIHandler:
    def __init__(self, configs):
        """
        Initialize the API Handler with configuration settings
        
        Args:
            configs (dict): Configuration settings for API interactions
        """
        self.configs = configs
    


    def send_extracted_image(self, image_path, mission_id, zone):
        """
        Send an extracted image and metadata to an open API endpoint.

        Args:
            image_path (str): Path to the image file (e.g., 'pressure_guage.jpg')
            mission_id (str or int): Mission ID to send
            zone (str): Zone identifier (e.g., 'Z2-MDL-STAND')

        Returns:
            dict or None: JSON response from API or None if failed
        """
        api_base_url = self.configs.get("api_base_url")
        if not api_base_url:
            logging.error("API base URL is missing in configs.")
            return None

        if not os.path.exists(image_path):
            logging.error(f"Image file not found: {image_path}")
            return None

        # Open endpoint → no Authorization header required
        api_url = f"{api_base_url}/stream/upload"
        files = {
            "frame": (os.path.basename(image_path), open(image_path, "rb"), "image/jpeg")
        }

        data = {
            "missionId": str(mission_id),
            "zone": zone
        }

        try:
            logging.info(f"Sending extracted image to {api_url}")
            response = requests.post(api_url, files=files, data=data)
            response.raise_for_status()
            logging.info("Image upload successful.")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error while sending image: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error while sending image: {str(e)}")
            return None
        finally:
            files["frame"][1].close()  # Ensure file handle is closed


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Example usage
    configs = {
        "api_base_url": "https://usedpaiwap01.azurewebsites.net"
    }

    api_handler = APIHandler(configs)
    response = api_handler.send_extracted_image(
        image_path="pressure_guage.jpg",
        mission_id="6900d9c42e1f53db9a1cac6d",
        zone="Z2-MDL-STAND"
    )

    print(response)
