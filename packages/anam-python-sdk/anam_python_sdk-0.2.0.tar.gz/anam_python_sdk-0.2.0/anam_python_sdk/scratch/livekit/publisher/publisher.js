const { Room } = LivekitClient;

let room;
const url = 'ws://localhost:7880'; // Your LiveKit server URL
const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6IiIsIm5hbWUiOiJwdWJsaXNoZXIiLCJ2aWRlbyI6eyJyb29tQ3JlYXRlIjpmYWxzZSwicm9vbUxpc3QiOmZhbHNlLCJyb29tUmVjb3JkIjpmYWxzZSwicm9vbUFkbWluIjpmYWxzZSwicm9vbUpvaW4iOnRydWUsInJvb20iOiJhbmFtIiwiY2FuUHVibGlzaCI6dHJ1ZSwiY2FuU3Vic2NyaWJlIjp0cnVlLCJjYW5QdWJsaXNoRGF0YSI6dHJ1ZSwiY2FuUHVibGlzaFNvdXJjZXMiOltdLCJjYW5VcGRhdGVPd25NZXRhZGF0YSI6ZmFsc2UsImluZ3Jlc3NBZG1pbiI6ZmFsc2UsImhpZGRlbiI6ZmFsc2UsInJlY29yZGVyIjpmYWxzZSwiYWdlbnQiOmZhbHNlfSwic2lwIjp7ImFkbWluIjpmYWxzZSwiY2FsbCI6ZmFsc2V9LCJhdHRyaWJ1dGVzIjp7fSwibWV0YWRhdGEiOiIiLCJzaGEyNTYiOiIiLCJzdWIiOiJwdWJsaXNoZXIiLCJpc3MiOiJkZXZrZXkiLCJuYmYiOjE3MjU2MTEwMjEsImV4cCI6MTcyNTYzMjYyMX0.M2Qfjd15jjQxiR9slst3GHsaVwr2SpUUzbGpQ5aEbTw'; // Retrieve token from server call 

async function startPublishing() {
    const room = new Room();

    room.on('connected', () => {
        console.log('Connected to room:', room.name);
        console.log('Publisher identity:', room.localParticipant.identity);

    });

    room.on('localTrackPublished', (publication) => {
        console.log('Local track published:', publication.trackSid);
    });

    await room.connect(url, token);

    // Create local audio and video tracks
    const localTracks = await LivekitClient.createLocalTracks({
        audio: true,
        video: true
    });

    // Publish tracks to the room
    for (const track of localTracks) {
        await room.localParticipant.publishTrack(track);
    }

    // Display local video
    const videoTrack = localTracks.find(track => track.kind === 'video');
    if (videoTrack) {
        videoTrack.attach(document.getElementById('localVideo'));
    }
}

document.getElementById('startButton').addEventListener('click', startPublishing);

// Prevent the room from being garbage collected
window.keepAlive = room;