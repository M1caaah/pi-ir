# This script is based on the following script: https://github.com/akkana/scripts/blob/master/rpi/pyirw.py
# It opens a socket connection to the lirc daemon and parses the commands that the daemon receives
# It then checks whether a specific command was received and generates output accordingly

import socket

SOCKPATH = "/var/run/lirc/lircd"

button_to_letter = {
    'KEY_POWER': 'a',
    'KEY_OPEN': 'b',
    'PROGRAM': 'c',
    'KEY_1': 'd',
    'KEY_2': 'e',
    'KEY_3': 'f',
    'KEY_AGAIN': 'g',
    'KEY_4': 'h',
    'KEY_5': 'i',
    'KEY_6': 'j',
    'A-B_REPEAT': 'k',
    'KEY_7': 'l',
    'KEY_8': 'm',
    'KEY_9': 'n',
    'KEY_ZOOM': 'o',
    'KEY_0': 'p',
    'KEY_CANCEL': 'q',
    'KEY_MENU': 'r',
    'KEY_SETUP': 's',
    'KEY_UP': 't',
    'KEY_SEARCH': 'u',
    'KEY_LEFT': 'v',
    'KEY_ENTER': 'w',
    'KEY_RIGHT': 'x',
    'KEY_TITLE': 'y',
    'KEY_DOWN': 'z',
    'KEY_PLAY': ' ',
    'REV': 'start/stop'
}

sock = None

# Establish a socket connection to the lirc daemon
def init_irw():
	global sock
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	sock.connect(SOCKPATH)
	print ('Socket connection established!')
	print ('Ready...')

# parse the output from the daemon socket
def getKey():
    while True:
        data = sock.recv(128)
        data = data.strip()

        if (len(data) > 0):
            break

    words = data.split()
    return words[2], words[1]

def ProcessCodes(key, dir):
    if (dir != "00"):
        return

    return button_to_letter[key]


# Main entry point
# The try/except structures allows the users to exit out of the program
# with Ctrl + C. Doing so will close the socket gracefully.

message = ""
sending = False

try:
    init_irw()

    while True:
        key, dir = getKey()
        key = key.decode() # This variable contains the name of the key
        dir = dir.decode() # This variable contains the direction (pressed/released)
        
        command = button_to_letter[key]
        if dir != "00":
            continue
        
        if command == 'start/stop':
            if sending == True:
                sending = False
                print("Message: "+message)
                message = ""
            else:
                sending = True
                print("Receiving message")
        elif sending:
            message += command

except KeyboardInterrupt:
    print ("\nShutting down...")
    # Close the socket (if it exists)
    if (sock != None):
        sock.close()
    print ("Done!")