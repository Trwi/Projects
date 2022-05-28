from __future__ import print_function

'''

*** Variable and function naming conventions were based on instructions at the beginning of the class ***

Instructions
After Reviewing and Studying Chapter 2 in Black Hat Python you are to Create a Standalone Python Script that will act
as a TCP Client. The Client will connect to the TCP Server Created in Assignment 10 on Port 5555.  The client will 
send 10 message to the Server with differing content and receive the hex digest response provided by the TCP Server. 

'''

import socket  # Import Python Standard Socket Library
import sys

print("Client Application")
print("Establish a connection to a server")
print("Available on the same network using PORT 5555\n")

PORT = 5555  # Port Number of Server
answer = 'y'

try:
    # Create a Socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get ip address of server or use host address with if statement below
    ip = input("If you are testing on your local machine, just press enter. Else: What is the IP address for the "
               "server?: ")

    if not ip:  # If no IP address is entered, use host address
        ip = socket.gethostname()

    print("\nAttempt Connection to: ", ip, PORT)

    clientSocket.connect((ip, PORT))  # Connect client to server

    # Sending message if there was a connection
    print("Socket Connected ...\n")

    while answer == 'y':
        message = input("What message would you like a md5 hash of?: ")  # Get message to make md5 hash of
        byteMessage = str.encode(message)  # Convert message to bytes
        clientSocket.sendall(byteMessage)  # Send message to server

        hashResult = clientSocket.recv(2048)  # Receive hashed message back from server
        hashResultString = hashResult.decode('UTF-8')  # Convert from bytes to regular string
        print(f'Hash: {hashResultString}')  # Print the received hash
        print()

        answer = input("Press 'q' to quit or press 'y' to continue sending strings and receiving md5 hashes: ").lower()
        print()

except Exception as err:  # Handles a connection error
    sys.exit(err)

print()
print("===============================================================================================================")
print("                                               End of script")
print("===============================================================================================================")
