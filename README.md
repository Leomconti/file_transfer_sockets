# Sending files to a group, when file is sent they get notified and can download it

### Server-side: done?..

-   Create a server socket that listens for incoming connections.
-   Accept client connections and spawn a new thread or process to handle each client.
-   In the client handler, receive the uploaded file from the client and save it to a designated location on the server.
-   Maintain a list of available files and their corresponding metadata (e.g., name, size, timestamp) in a data structure.
-   Implement a mechanism for clients to request the list of available files.
-   Serve the requested files to clients when they make a download request.

### Client-side: kinda done

-   Create a client socket to connect to the server.
-   Implement an upload function that allows the user to select a file and send it to the server.
-   Implement a download function that requests the list of available files from the server and allows the user to select a file to download.

# What is done

-   sender and receiver done for sending and downloading the file
-   client and server side with download and upload

# to-do

-   work on the main function for the client, so it can choose more than one operation to do, in a loop, receive the messages from the group, probably leaving a thread open or something... check that..

-   probably create a tag < MESSAGE > so it knows its a message and not data to be "processed"
