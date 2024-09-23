This is a simple publisher that publishes a video/audio track to a room.

## Usage

**Note: You need to run the server first before running the publisher.**

To run the publisher as a web server, serving the `publisher.html` file:

1. Install a simple HTTP server. If you have Python installed, you can use its built-in HTTP server.

2. Navigate to the directory containing `publisher.html` in your terminal.

3. Run one of the following commands based on your Python version:

   Python 3.x:
   ```bash
   python -m http.server 8020
   ```

   Python 2.x:
   ```bash
   python -m SimpleHTTPServer 8020
   ```

4. Open a web browser and visit:
   ```
   http://localhost:8000/publisher.html
   ```

You can change `8000` to any port number you prefer.

## Note

Make sure your `publisher.html` file is properly configured with the necessary LiveKit client-side JavaScript and any required authentication mechanisms.