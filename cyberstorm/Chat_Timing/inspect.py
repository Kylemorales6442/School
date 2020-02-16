##############################################################################################################
# Team Name: Egpytians
# Date: 4/17/2019
# Description: Receives a message from a chat server and calculates possible modes for delays.
#              This is best used in conjunction with a covert timing program that implements leniency
##############################################################################################################
import socket
import sys
import time
from heapq import nlargest
from math import floor

def main():
    # Server information
    ADDRESS = "www.jeangourd.com"
    PORT = 31337
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # How good of a prediction you want.
    # Lower = better, but will take a little longer
    # Resolutions below like .005 are probably useless
    RESOLUTION = .01
    RESOLUTION = float(RESOLUTION)

    # Instantiate and connect to the socket
    SERVER.connect((ADDRESS, PORT))
    
    delays = []
    
    # Receive up to 4096 characters from the server, decode into a Python string
    # Keep getting characters until an "EOF" is received
    data = str(SERVER.recv(4096), "utf-8")
    last = time.time()
    while data.strip("\n") != "EOF":
        sys.stdout.write(data)
        sys.stdout.flush()
        data = str(SERVER.recv(4096), "utf-8")
        delays, last = getDelay(data, delays, last)
    SERVER.close()
    
    # Sort the delays for easier categorization
    delays.sort()
    categorize(delays, RESOLUTION)

# Categorize the delays separated by the provided resolution
def categorize(delays, res):
    categorized = {}

    i = 0.0
    while(i < round(max(delays), len(str(res)) - 2) + res):
        categorized[round(i, len(str(res)) - 2)] = 0
        i += res
    
    # Normalize the number of decimal places
    # I was getting weird precision sometimes from the way python stores floating points
    for delay in delays:
        delay *= 1/res
        delay = round(floor(delay)*res, len(str(res)) - 2)
        categorized[delay] += 1

    # Find the two ranges with the largest number of hits, and guess around those values.
    estimated = []
    modes = nlargest(2, categorized.values())
    for section in sorted(list(categorized.keys())):
        print("{}: {}".format(section, categorized[section]))
        if categorized[section] in sorted(modes):
            if len(estimated) == 0:
                estimated.append(["Short", section, section + res/2, section - res/2])
            else: 
                estimated.append(["Long", section, section + res/2, section - res/2])

    # Display the predictions in a neat format
    print()
    for part in estimated:
        print("{} estimates: {}, {}, and {}".format(*part))

# Grab the delay.
# Basically the same as the pdf, I just made a function to make main look nicer.
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

