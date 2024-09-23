"""Subscribe to a room and receive video frames"""
import os
from dotenv import load_dotenv
from livekit import rtc

import asyncio
import logging


load_dotenv()

URL = os.environ.get("LIVEKIT_URL")
TOKEN = os.environ.get("LIVEKIT_TOKEN")
ROOM_NAME = os.environ.get("LIVEKIT_ROOM_NAME")
SECRET = os.environ.get("LIVEKIT_SECRET")

async def main():
    room = rtc.Room()

    @room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        logging.info(
            "participant connected: %s %s", participant.sid, participant.identity)

    async def receive_frames(stream: rtc.VideoStream):
        async for frame in video_stream:
            # received a video frame from the track, process it here
            pass

    # track_subscribed is emitted whenever the local participant is subscribed to a new track
    @room.on("track_subscribed")
    def on_track_subscribed(
        track: rtc.Track,
        publication: rtc.RemoteTrackPublication, 
        participant: rtc.RemoteParticipant):
        logging.info("track subscribed: %s", publication.sid)
        if track.kind == rtc.TrackKind.KIND_VIDEO:
            video_stream = rtc.VideoStream(track)
            asyncio.ensure_future(receive_frames(video_stream))

    # By default, autosubscribe is enabled. The participant will be subscribed to
    # all published tracks in the room
    await room.connect(
        URL,
        TOKEN
    )
    logging.info("connected to room %s", room.name)

    # participants and tracks that are already available in the room
    # participant_connected and track_published events will *not* be emitted for them
    for participant in room.remote_participants.items():
        logging.info("participant already in room: %s", participant.identity)
        for publication in participant.track_publications.values():
            logging.info("track already published: %s", publication.sid)

    # Keep the connection alive
    await asyncio.Future()
    
    # for participant in room.participants.items():
    #     for publication in participant.track_publications.items():
    #         print("track publication: %s", publication.sid)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())