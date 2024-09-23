# Webkit Server 
This is a simple server that creates a room and provides a token to the client.

## Usage
### Start the server 
Ensure to provide your own api key and secret as part of `ENVIRONMENT` in compose.yml. 

```bash
docker compose up
```

### Get a Room
Ensure a `.env` file is present with the following keys: 

```bash
LIVEKIT_API_KEY=<your api key>
LIVEKIT_API_SECRET=<your api secret>
LIVEKIT_ROOM_NAME=anam
LIVEKIT_URL=http://localhost:7880
```

Run the following to create a room and get its joining token: 

```python 
python token.py 
```

