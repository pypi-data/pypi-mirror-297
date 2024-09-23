const { Room } = LivekitClient;

const url = "http://localhost:7880"; // Replace with your LiveKit server URL
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6IiIsIm5hbWUiOiJzdWJzY3JpYmVyIiwidmlkZW8iOnsicm9vbUNyZWF0ZSI6ZmFsc2UsInJvb21MaXN0IjpmYWxzZSwicm9vbVJlY29yZCI6ZmFsc2UsInJvb21BZG1pbiI6ZmFsc2UsInJvb21Kb2luIjp0cnVlLCJyb29tIjoiYW5hbSIsImNhblB1Ymxpc2giOnRydWUsImNhblN1YnNjcmliZSI6dHJ1ZSwiY2FuUHVibGlzaERhdGEiOnRydWUsImNhblB1Ymxpc2hTb3VyY2VzIjpbXSwiY2FuVXBkYXRlT3duTWV0YWRhdGEiOmZhbHNlLCJpbmdyZXNzQWRtaW4iOmZhbHNlLCJoaWRkZW4iOmZhbHNlLCJyZWNvcmRlciI6ZmFsc2UsImFnZW50IjpmYWxzZX0sInNpcCI6eyJhZG1pbiI6ZmFsc2UsImNhbGwiOmZhbHNlfSwiYXR0cmlidXRlcyI6e30sIm1ldGFkYXRhIjoiIiwic2hhMjU2IjoiIiwic3ViIjoic3Vic2NyaWJlciIsImlzcyI6ImRldmtleSIsIm5iZiI6MTcyNTYxMTAyMSwiZXhwIjoxNzI1NjMyNjIxfQ.Bnc82DSa6RG1jgU3M7hoFnE_7wgycGwGFViTh-XyZXQ"; // Replace with your generated token

async function connectToRoom() {
    const room = new Room();
    
    room.on('connected', () => {
        console.log('Subscriber connected to room:', room.name);
        console.log('Subscriber identity:', room.localParticipant.identity);
    });

    room.on('connectionStateChanged', (state) => {
        console.log('Connection state changed:', state);
    });

    room.on('participantConnected', (participant) => {
        console.log('Participant connected:', participant.identity);
        handleParticipant(participant);
    });

    room.on('participantDisconnected', (participant) => {
        console.log('Participant disconnected:', participant.identity);
    });


    // Connect to the room
    await room.connect(url, token);
    console.log(`Connected to room ${room.name}`);

    try {
        await room.connect(url, token);
        console.log(`Connected to room ${room.name}`);

        // Handle existing participants
        if (room.participants) {
            room.participants.forEach((participant) => {
                handleParticipant(participant);
            });
        }
    } catch (error) {
        console.error('Failed to connect to the room:', error);
    }

    //Handle local participant (no need for this)
    // const localParticipant = room.localParticipant;
    // const localVideo = document.getElementById('localVideo');
    // localParticipant.on('trackPublished', (publication) => {
    //     if (publication.track.kind === 'video') {
    //         localVideo.srcObject = new MediaStream([publication.track.mediaStreamTrack]);
    //     }
    // });

    // Handle remote participants
    room.on('participantConnected', (participant) => {
        console.log(`Participant connected: ${participant.identity}`);
    });

}

function handleParticipant(participant) {
    participant.on('trackSubscribed', (track, publication) => {
        console.log('Track subscribed:', track.kind, 'from', participant.identity);
        console.log('Track details:', track);
        console.log('Publication details:', publication);

        if (track.kind === 'video') {
            const videoElement = document.createElement('video');
            videoElement.id = `video-${participant.identity}`;
            videoElement.autoplay = true;
            videoElement.playsInline = true;
            console.log('Attaching track to video element');
            track.attach(videoElement);
            document.getElementById('remoteVideos').appendChild(videoElement);
            console.log('Video element added to DOM');
        } else if (track.kind === 'audio') {
            const audioElement = new Audio();
            audioElement.autoplay = true;
            console.log('Attaching track to audio element');
            track.attach(audioElement);
            console.log('Audio element created (not added to DOM)');
        }
    });

    participant.on('trackUnsubscribed', (track) => {
        console.log('Track unsubscribed:', track.kind, 'from', participant.identity);
        track.detach();
    });

    // // Handle already subscribed tracks
    // participant.tracks.forEach(publication => {
    //     if (publication.isSubscribed) {
    //         const track = publication.track;
    //         if (track.kind === 'video') {
    //             track.attach(remoteVideo);
    //         } else if (track.kind === 'audio') {
    //             const audioElement = new Audio();
    //             audioElement.autoplay = true;
    //             track.attach(audioElement);
    //         }
    //     }
    // });
}

function handleTrackSubscribed(track, participant) {
    if (track.kind === 'video') {
        const videoElement = document.createElement('video');
        videoElement.id = `video-${participant.identity}`;
        videoElement.autoplay = true;
        videoElement.playsInline = true;
        track.attach(videoElement);
        document.getElementById('remoteVideos').appendChild(videoElement);
    } else if (track.kind === 'audio') {
        const audioElement = new Audio();
        audioElement.autoplay = true;
        track.attach(audioElement);
    }
}


connectToRoom().catch(console.error);

// Fix for audio not playing
document.body.addEventListener('click', () => {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    audioContext.resume();
});