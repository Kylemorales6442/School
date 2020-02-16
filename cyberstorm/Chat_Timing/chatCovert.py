#########################################################################################################################
# Team Name: Egyptians
# Date: 4/17/2019
# Description: Receives the message from a chat server, identifies probable delays, and then finds the likely message
#              Tests 7 and 8 bit binary, and tests both timing setups.  Work could be done to extend this to 3 timings
#              but it would take a while and probably isn't worth it until Cyberstorm.
# Note: We should not turn this in because I'm not positive it will always work, and will probably not net us more points
#########################################################################################################################
import socket
import sys
import time
from heapq import nlargest
from math import floor
from binascii import unhexlify, Error

def main():
    # Server information
    ADDRESS = "www.jeangourd.com"
    PORT = 31337
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # How close you want the prediction to be.  Lower is better.
    # However, lower than .005 is probably not useful.
    RESOLUTION = .01
    
    # Instantiate and connect to the socket
    SERVER.connect((ADDRESS, PORT))
    
    # Receive up to 4096 characters from the server, decode into a Python string
    # Keep getting characters until an "EOF" is received
    delays = []
    data = str(SERVER.recv(4096), "utf-8")
    last = time.time()
    
    # Note: will fail if EOF is sent with another character
    # Easiest fix is honestly just to restart the program since it's rare
    while data.strip("\n") != "EOF":
        sys.stdout.write(data)
        sys.stdout.flush()
        data = str(SERVER.recv(4096), "utf-8")
        delays, last = getDelay(data, delays, last)
    SERVER.close()
    
    # Create a copy of te delays array and sort it for categorization
    # We will need an unsorted version for later
    delaysCopy = delays[:]
    delaysCopy.sort()
    categorized = categorize(delaysCopy, RESOLUTION)

    # Get the index where we need to split the sorted delays array.
    # One portion will be 1, the other will be 0
    split = analyze(categorized, RESOLUTION)

    # Separate the delays array
    delaysCopy = [delaysCopy[0:split], delaysCopy[split:len(delays)]]

    # Get the covert message and respone
    response, allMessages = getString(delays, delaysCopy)
   
    # Output stuff
    print()
    print(response)
    print()

    # Show all the possible responses.
    print("Here are the other possible messages:")    
    for bit in allMessages.keys():
        print("{}-bit:".format(bit), *allMessages[bit], sep="\n")
        print()

# Grab the string from the organized delays
def getString(delays, organizedDelays):

    # Get the binary representations, with both possibilities for 1's and 0's
    binaries = ["", ""]
    for delay in delays:
        if delay in organizedDelays[0]:
            binaries[0] += "1"
            binaries[1] += "0"
        else:
            binaries[0] += "0"
            binaries[1] += "1"
    
    # Get the messages for each of the binaries using 7 and 8 bits
    # Stores the results in a dictionary.
    bitsToCheck = [7, 8]
    messages = {bit: [] for bit in bitsToCheck}
    for bit in bitsToCheck:
        coverts = ["", ""]
        i = 0
        while i < len(binaries[0]):
            # Make sure each character has an even number of bits to unhexlify
            # Only necessary for 7-bit binary but will save us a lot of time if the challenge does it
            chars = [binaries[0][i:i+bit].zfill(8), binaries[1][i:i+bit].zfill(8)]
            chars = [int("0b{}".format(chars[i]), 2) for i in range(2)]
            for j in range(2):
                # Try to unhexlify.  "Error" is the binascii error, occurs on last character
                # It will frequently be un-unhexlifyable.
                try:
                    chars[j] = str(unhexlify("{0:x}".format(chars[j])), "utf-8")
                except (UnicodeDecodeError, Error):
                    chars[j] = "?"
                coverts[j] += chars[j]
            i += bit
        messages[bit] = coverts

    # Looks for "EOF" in the messages
    # If none is found, something may have gone wrong.
    for bit in messages.keys():
        for covert in messages[bit]:
            try:
                end = covert.index("EOF")
            except ValueError:
                continue
            return "The message is probably the following: \"{}\"".format(covert[:end]), messages
    return "No EOF was found.", messages

# Find the modes in the delays
# Also find the split
def analyze(categorizedDelays, res):
    modes = nlargest(2, categorizedDelays.values())
    for key in categorizedDelays:
        if categorizedDelays[key] in modes:
            modes[modes.index(categorizedDelays[key])] = [modes[modes.index(categorizedDelays[key])], key]
    split = floor((float(modes[0][1]) + float(modes[1][1]))/(2*res))*res
    
    index = 0
    for key in sorted(list(categorizedDelays.keys())):
        index += categorizedDelays[key]
        if key == split:
            break
    return index

# Categorize the data into delays based on the resolution
def categorize(delays, res):
    categorized = {}

    i = 0.0
    while(i < round(max(delays), len(str(res)) - 2) + res):
        categorized[round(i, len(str(res)) - 2)] = 0
        i += res
    # Normalize the number of decimal points
    for delay in delays:
        delay /= res
        delay = round(floor(delay)*res, len(str(res)) - 2)
        categorized[delay] += 1
    return categorized

# Calculate the delay from the server
def getDelay(data, delays, last):
    if data.strip("\n") != "EOF":
        for character in data:
            delays.append(time.time() - last)
    else:
        delays.append(time.time() - last)
    last = time.time()    
    return delays, last

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

