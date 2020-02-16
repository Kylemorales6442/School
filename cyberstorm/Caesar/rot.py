######################################################
# Author: Chris Given
# Date: 3/30/2019
# Description: It's a rot cipher
######################################################
import sys

def main():
    mode = 1 if sys.argv[1] == "-e" else -1
    key = int(sys.argv[2])
    while(1):
        plaintext = input()
        ciphertext = ""
        for letter in plaintext:
            if letter.isalpha():
                ptLetter = letter
                letter = letter.lower()
                newLetter = chr((ord(letter) % 97 + key) % 26 + 97)
                ciphertext += newLetter if ptLetter == letter else newLetter.upper()
            else:
                ciphertext += letter
        print(ciphertext)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        pass
