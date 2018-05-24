import subprocess
from time import sleep, strftime, time
from threading import Thread

# Edit these for how many people/devices you want to track
occupant = [""]

# MAC addresses for our phones
address = [""]

# Some arrays to help minimize streaming and account for devices
# disappearing from the network when asleep
firstRun = [1] * len(occupant)
presentSent = [0] * len(occupant)
notPresentSent = [0] * len(occupant)
counter = [0] * len(occupant)

def write_presence(occupant):
    with open("presence.json", "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(occupant)))
        
def write_address(output):
    with open("mac.json", "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(output)))

# Function that checks for device presence
def whosHere(i):
    
    sleep(15)

    # Loop through checking for devices and counting if they're not present
    while True:
        
        # Exits thread if Keyboard Interrupt occurs
        if stop == True:
            print "Exiting Thread"
            exit()
        else:
            pass

        # If a listed device address is present print and stream
        if address[i] in output:
            print(occupant[i] + "'s device is connected to your network")
            if presentSent[i] == 0:
                firstRun[i] = 0
                presentSent[i] = 1
                notPresentSent[i] = 0
                counter[i] = 0
                sleep(60)
            else:
                # If a stream's already been sent, just wait for 30 seconds
                counter[i] = 0
                sleep(60)
        # If a listed device address is not present, print and stream
        else:
            print(occupant[i] + "'s device is not present")
            # Only consider a device offline if it's counter has reached 30
            # This is the same as 15 minutes passing
            if counter[i] == 30 or firstRun[i] == 1:
                firstRun[i] = 0
                if notPresentSent[i] == 0:
                    notPresentSent[i] = 1
                    presentSent[i] = 0
                    counter[i] = 0
                else:
                    # If a stream's already been sent, wait 30 seconds
                    counter[i] = 0
                    sleep(60)
            # Count how many 30 second intervals have happened since the device 
            # disappeared from the network
            else:
                counter[i] = counter[i] + 1
                print(occupant[i] + "'s counter at " + str(counter[i]))
                sleep(60)


# Main thread

try:

    # Initialize a variable to trigger threads to exit when True
    global stop
    stop = False

    # Start the thread(s)
    # It will start as many threads as there are values in the occupant array
    for i in range(len(occupant)):
        t = Thread(target=whosHere, args=(i,))
        t.start()

    while True:
        # Make output global so the threads can see it
        global output
        # Assign list of devices on the network to "output"
        output = subprocess.check_output("sudo arp-scan -l", shell=True)
        write_presence(occupant)
        write_address(output)
        
        # Wait 60 seconds between scans
        sleep(60)
except KeyboardInterrupt:
    # On a keyboard interrupt signal threads to exit
    stop = True
    exit()
