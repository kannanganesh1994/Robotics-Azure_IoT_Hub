# import requests
# import json
# import logging
# import os
# import asyncio
# import ast



# class APIHandler:
#     def __init__(self, configs):
#         """
#         Initialize the API Handler with configuration settings
        
#         Args:
#             configs (dict): Configuration settings for API interactions
#         """
#         self.configs = configs
#         self.update_headers()
    
#     def update_headers(self):
#         """Update headers with the current token from configs"""
#         self.update_headers()
    
#     def update_headers(self):
#         """Update headers with the current token from configs"""
#         self.headers = {
#             "Authorization": f"Bearer {self.configs.get('msft_token')}",
#             "Content-Type": "application/json"
#         }
#         logging.info("API headers updated with current token")
        

#     def get_document_details(self):
#         """
#         Get document details from the API
        
#         Returns:
#             dict: Document details response from API
#         """
        
#         # Fix: Access JobId and DocumentId directly from configs, not from a non-existent 'message' key
#         api_url = f"{self.configs.get('api_base_url')}/ml/jobs/{self.configs.get('JobId')}/documents/{self.configs.get('DocumentId')}/ocrDocumentDetails"
#         # Fix: Access JobId and DocumentId directly from configs, not from a non-existent 'message' key
#         api_url = f"{self.configs.get('api_base_url')}/ml/jobs/{self.configs.get('JobId')}/documents/{self.configs.get('DocumentId')}/ocrDocumentDetails"
        
#         try:
#             logging.info(f"Getting document details from: {api_url}")
#             # Ensure headers are up to date
#             self.update_headers()
            
#             logging.info(f"Getting document details from: {api_url}")
#             # Ensure headers are up to date
#             self.update_headers()
            
#             response = requests.get(api_url, headers=self.headers)
#             response.raise_for_status()
            
#             response_data = response.json()
#             return response_data
#         except requests.exceptions.HTTPError as e:
#             self._handle_unauthorized_error(e, api_url)
#             logging.error(f"HTTP error getting document details: {str(e)}")
#             return None
#         except requests.exceptions.HTTPError as e:
#             self._handle_unauthorized_error(e, api_url)
#             logging.error(f"HTTP error getting document details: {str(e)}")
#             return None
#         except Exception as e:
#             logging.error(f"Error getting document details: {str(e)}")
#             return None


# import requests
# import json
# import logging
# import os
# import asyncio
# import ast


# class APIHandler:
#     def __init__(self, configs):
#         """
#         Initialize the API Handler with configuration settings
        
#         Args:
#             configs (dict): Configuration settings for API interactions
#         """
#         self.configs = configs
    


#     def send_extracted_image(self, image_path, mission_id, zone):
#         """
#         Send an extracted image and metadata to an open API endpoint.

#         Args:
#             image_path (str): Path to the image file (e.g., 'pressure_guage.jpg')
#             mission_id (str or int): Mission ID to send
#             zone (str): Zone identifier (e.g., 'Z2-MDL-STAND')

#         Returns:
#             dict or None: JSON response from API or None if failed
#         """
#         api_base_url = self.configs.get("api_base_url")
#         if not api_base_url:
#             logging.error("API base URL is missing in configs.")
#             return None

#         if not os.path.exists(image_path):
#             logging.error(f"Image file not found: {image_path}")
#             return None

#         # Open endpoint → no Authorization header required
#         api_url = f"{api_base_url}/stream/upload"
#         files = {
#             "frame": (os.path.basename(image_path), open(image_path, "rb"), "image/jpeg")
#         }

#         data = {
#             "missionId": str(mission_id),
#             "zone": zone
#         }

#         try:
#             logging.info(f"Sending extracted image to {api_url}")
#             response = requests.post(api_url, files=files, data=data)
#             response.raise_for_status()
#             logging.info("Image upload successful.")
#             return response.json()
#         except requests.exceptions.HTTPError as e:
#             logging.error(f"HTTP error while sending image: {str(e)}")
#             return None
#         except Exception as e:
#             logging.error(f"Unexpected error while sending image: {str(e)}")
#             return None
#         finally:
#             files["frame"][1].close()  # Ensure file handle is closed


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     # Example usage
#     configs = {
#         "api_base_url": "https://usedpaiwap01.azurewebsites.net"
#     }

#     api_handler = APIHandler(configs)
#     response = api_handler.send_extracted_image(
#         image_path="pressure_guage.jpg",
#         mission_id="6900d9c42e1f53db9a1cac6d",
#         zone="Z2-MDL-STAND"
#     )

#     print(response)


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


    def update_mission_status(self, mission_id, status):
        """
        Update the mission status via PATCH request to the mission status API.

        Args:
            mission_id (str): Mission ID to update.
            status (str): New status to set (e.g., 'Created', 'InProgress', 'Completed').

        Returns:
            dict or None: JSON response from API or None if failed.
        """
        api_base_url = self.configs.get("api_base_url")
        if not api_base_url:
            logging.error("API base URL is missing in configs.")
            return None

        api_url = f"{api_base_url}/mission/{mission_id}/update-status"
        headers = {
            "accept": "*/*",
            "Content-Type": "application/json"
        }
        payload = {"status": status}

        try:
            logging.info(f"Updating mission status to '{status}' at {api_url}")
            response = requests.patch(api_url, headers=headers, json=payload)
            response.raise_for_status()
            logging.info("Mission status updated successfully.")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error while updating mission status: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error while updating mission status: {str(e)}")
            return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example usage
    configs = {
        "api_base_url": "https://usedpaiwap01.azurewebsites.net"
    }

    api_handler = APIHandler(configs)

    # Example: Send extracted image
    response = api_handler.send_extracted_image(
        image_path="pressure_guage.jpg",
        mission_id="6900d9c42e1f53db9a1cac6d",
        zone="Z2-MDL-STAND"
    )
    print("Image upload response:", response)

    # Example: Update mission status
    status_response = api_handler.update_mission_status(
        mission_id="69003548661346a029a2d107",
        status="Created"
    )
    print("Status update response:", status_response)

