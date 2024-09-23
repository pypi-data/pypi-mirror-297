"""Create a room and list all rooms"""
import asyncio
import os

from dotenv import load_dotenv
from livekit import api

# Load environment variables
load_dotenv()

ROOM_NAME = os.environ.get("LIVEKIT_ROOM_NAME", "anam")
LIVEKIT_URL = os.environ.get("LIVEKIT_URL", "http://localhost:7880")
LIVEKIT_KEY = os.environ.get("LIVEKIT_API_KEY", "livekitkey")
LIVEKIT_SECRET = os.environ.get("LIVEKIT_API_SECRET", "livekitsecret")

def get_token(identity: str):
    """Use the LIVEKIT_API_KEY and LIVEKIT_API_SECRET env vars"""
    return (
        api.AccessToken()
        .with_identity(identity)
        .with_name(identity)
        .with_grants(api.VideoGrants(
            room_join=True,
            room=ROOM_NAME,
        )).to_jwt()
    )

async def main():
    
    pub_token = get_token("publisher")
    sub_token = get_token("subscriber")

    print("Publisher Token: \n\n", pub_token, "\n\n")
    print("Sub Token: \n\n", sub_token, "\n\n")
    # lk_api = api.LiveKitAPI(
    #     url=LIVEKIT_URL,
    #     api_key=LIVEKIT_KEY,
    #     api_secret=LIVEKIT_SECRET,
    # )

    # print(f"Creating room {ROOM_NAME}")
    # room_info = await lk_api.room.create_room(
    #     api.CreateRoomRequest(name=ROOM_NAME),
    # )
    # print(f"Room {ROOM_NAME} created. \n", room_info)
    # results = await lk_api.room.list_rooms(
    #     api.ListRoomsRequest()
    # )
    # await lk_api.aclose()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        main()
    )