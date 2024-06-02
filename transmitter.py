import lirc
import time

client = lirc.Client()

letter_to_button = {
    'a': 'KEY_POWER',
    'b': 'KEY_OPEN',
    'c': 'PROGRAM',
    'd': 'KEY_1',
    'e': 'KEY_2',
    'f': 'KEY_3',
    'g': 'KEY_AGAIN',
    'h': 'KEY_4',
    'i': 'KEY_5',
    'j': 'KEY_6',
    'k': 'A-B_REPEAT',
    'l': 'KEY_7',
    'm': 'KEY_8',
    'n': 'KEY_9',
    'o': 'KEY_ZOOM',
    'p': 'KEY_0',
    'q': 'KEY_CANCEL',
    'r': 'KEY_MENU',
    's': 'KEY_SETUP',
    't': 'KEY_UP',
    'u': 'KEY_SEARCH',
    'v': 'KEY_LEFT',
    'w': 'KEY_ENTER',
    'x': 'KEY_RIGHT',
    'y': 'KEY_TITLE',
    'z': 'KEY_DOWN',
    ' ': 'KEY_PLAY',
}

while True:
    sentence = input("Enter a sentence: ")
    client.send_once("DK_Digital_DVD-228", "REV")
    for char in sentence:
        # Get the button corresponding to the character
        button = letter_to_button.get(char.lower())

        if button is None:
            print(f"No button mapped for the character {char}")
        else:
            try:
                client.send_once('DK_Digital_DVD-228', button)
            except Exception as error:
                print('Unable to send the power key!')
                print(error)  # Error has more info on what lircd sent back.
    client.send_once("DK_Digital_DVD-228", "REV")
    