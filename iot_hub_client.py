# import asyncio
# from azure.iot.device.aio import IoTHubDeviceClient
# from azure.iot.device import MethodResponse

# CONNECTION_STRING = "connection_string_here"


# # --- Example async functions ---
# async def initiate():
#     print("[initiate] started")
#     await asyncio.sleep(3)
#     print("[initiate] done")
#     return {"status": "initiated"}


# async def start_streaming():
#     print("[startStreaming] started")
#     await asyncio.sleep(5)
#     print("[startStreaming] done")
#     return {"status": "streaming_started"}


# async def stop_streaming():
#     print("[stopStreaming] started")
#     await asyncio.sleep(2)
#     print("[stopStreaming] done")
#     return {"status": "streaming_stopped"}


# # --- Handle each method request in its own task ---
# async def handle_method(device_client, method_request):
#     method_name = method_request.name
#     print(f"\n[IoT Hub] Received: {method_name}")

#     try:
#         if method_name == "navigate":
#             payload = await initiate()
#         elif method_name == "startStreaming":
#             payload = await start_streaming()
#         elif method_name == "stopStreaming":
#             payload = await stop_streaming()
#         else:
#             payload = {"error": f"Unknown method {method_name}"}

#         status = 200
#     except Exception as e:
#         payload, status = {"error": str(e)}, 500

#     response = MethodResponse.create_from_method_request(method_request, status, payload)
#     await device_client.send_method_response(response)
#     print(f"[IoT Hub] Responded to {method_name}: {payload}")


# # --- Listener loop ---
# async def method_listener(device_client):
#     print("✅ Listening for IoT Hub direct methods...")

#     while True:
#         # Wait for a new direct method
#         method_request = await device_client.receive_method_request()

#         # Each request handled concurrently in its own task
#         asyncio.create_task(handle_method(device_client, method_request))


# # --- Main entrypoint ---
# async def main():
#     device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING,
#                                                                      websockets=True)
#     await device_client.connect()
#     print("Connected to IoT Hub.")
#     await method_listener(device_client)


# if __name__ == "__main__":
#     asyncio.run(main())
 


import json
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
from azure.iot.device import MethodResponse

from settings import Settings


# import ssl
# import certifi
# import paho.mqtt.client as mqtt

# # Patch the default SSL context used by paho-mqtt
# def patched_ssl_context():
#     context = ssl.create_default_context()
#     context.load_verify_locations(cafile=certifi.where())
#     return context

# mqtt.ssl_context = patched_ssl_context()

CONNECTION_STRING = Settings.IOTH_DEVICE_CONN_STRING


# --- Example async functions ---
async def initiate(device_client):
    print("[initiate] started")
    message_payload = {
        "executionId": "exec0001",
        "deviceId": "d01",
        "messageRoute": "ai_inference",
        "messageType": "Inference"
    }
    
    # Send the message
    message = Message(json.dumps(message_payload))
    message.content_type = "application/JSON"
    message.content_encoding = "UTF-8"
    await device_client.send_message(message)

    await asyncio.sleep(3)
    print("[initiate] done")
    return {"status": "initiated"}


async def start_streaming(device_client):
    print("[startStreaming] started")
    await asyncio.sleep(5)
    print("[startStreaming] done")
    return {"status": "streaming_started"}


async def stop_streaming(device_client):
    print("[stopStreaming] started")
    await asyncio.sleep(2)
    print("[stopStreaming] done")
    return {"status": "streaming_stopped"}


# --- Handle each method request in its own task ---
async def handle_method(device_client, method_request):
    method_name = method_request.name
    print(f"\n[IoT Hub] Received: {method_name}")

    try:
        if method_name == "navigate":
            payload = await initiate(device_client)
        elif method_name == "startStreaming":
            payload = await start_streaming(device_client)
        elif method_name == "stopStreaming":
            payload = await stop_streaming(device_client)
        else:
            payload = {"error": f"Unknown method {method_name}"}

        status = 200
    except Exception as e:
        payload, status = {"error": str(e)}, 500

    response = MethodResponse.create_from_method_request(method_request, status, payload)
    await device_client.send_method_response(response)
    print(f"[IoT Hub] Responded to {method_name}: {payload}")


# --- Listener loop ---
async def method_listener(device_client):
    print("✅ Listening for IoT Hub direct methods...")

    while True:
        # Wait for a new direct method
        method_request = await device_client.receive_method_request()

        # Each request handled concurrently in its own task
        asyncio.create_task(handle_method(device_client, method_request))


# --- Main entrypoint ---
async def main():
    device_client = IoTHubDeviceClient.create_from_connection_string(Settings.IOTH_DEVICE_CONN_STRING
                                                                     , websockets=True)
    print(Settings.IOTH_DEVICE_CONN_STRING)
    await device_client.connect()
    print("Connected to IoT Hub.")
    await method_listener(device_client)


if __name__ == "__main__":
    asyncio.run(main())
 

