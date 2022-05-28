from __future__ import print_function

'''

*** Variable and function naming conventions were based on instructions at the beginning of the class ***

Instructions
After Reviewing and Studying Chapter 2 in Black Hat Python you are to Create a Standalone Python Script that will act
as a TCP Server. The Server will accept connections on Port 5555 from TCP Clients Operating on the same local IP range
as the Server. The server will receive the message, create an MD5 Hash of the Message and respond to the Client with
the MD5 Digest generated. The server will continue to operate until terminated by the user.

'''

import socket  # Import Python Standard Socket Library
import sys
import hashlib


print("The Server is starting...")

count = 0

try:

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create Socket for listening

    ip = '0.0.0.0'

    localPort = 5555  # Specify a local Port to accept connections on

    serverSocket.bind((ip, localPort))  # Bind mySocket to localHost

    serverSocket.listen(1)  # Listen for connections

    print('\nWaiting for Connection Request')

    ''' Wait for a connection request
        Note this is a synchronous Call meaning the program will halt until
        a connection is received.  Once a connection is received
        we will accept the connection and obtain the 
        ipAddress of the connecting computer
    '''

    conn, client = serverSocket.accept()

    print("Connection Received from Client: ", client)
    print()

    while True:

        buffer = conn.recv(2048)  # Wait for Data

        if buffer:  # If a response is received from client, proceed
            stringBuffer = buffer.decode('UTF-8')  # Create a string version of the buffer
            hashResult = hashlib.md5(buffer)  # Create an md5 hash object of the buffer
            hashString = hashResult.hexdigest()  # Get the hex digest from hash object
            hashByteString = str.encode(hashString)  # Remove the b'' from hash string

            conn.sendall(hashByteString)  # Send the created hash to the client
            print(
                f'String: {stringBuffer} | md5 Hash: {hashString} | Hash returned to client...\n')
            count += 1  # Keeps track of the number of hashes produced and sent by the server

        else:  # If nothing is received from client, break out of loop
            break

    print(f"The server processed {count} messages into md5 hashes.")  # Prints the total number of hashes

except Exception as err:  # Handles a connection error
    sys.exit(str(err))

print()
print("===============================================================================================================")
print("                                               End of script")
print("===============================================================================================================")
