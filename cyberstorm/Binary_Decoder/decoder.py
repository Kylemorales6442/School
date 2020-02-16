#############################################################################################
# Author: Chris Given
# Date: 3/19/2019
# Language: Python 3.7
# Description: Converts a binary string of 7 or 8 bits to a printable string
# You should already be able to see the gitlab but the repo is here: 
#   https://www.gitlab.com/Hime0698/cyberstorm
# Improvements for Cyberstorm: Detect or manually input patterns like alternating 7-bit/8-bit
#############################################################################################

import sys

def main():
    # Read the binary string
    binary = sys.stdin.read().strip("\n")
    
    # Detect the number of bits per character.  In the case of a number divisible by 56, print both.
    bitsPerChar = [part for part in (7, 8) if len(binary) % part == 0]
   
    # Grabs a correctly-sized slice of the binary array, converts it to a base 2 integer, and converts that to an ASCII char
    # It does this until the string is exhausted, and prints each item in the resulting array of characters
    # They are separated by an empty string.
    for output in bitsPerChar:
        print(str(output) + "-bit: ", *[chr(int(binary[i:i+output], base=2)) for i in range(0, len(binary), output)], sep="")

if __name__ == "__main__":
    main()
