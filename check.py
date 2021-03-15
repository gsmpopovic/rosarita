import psutil
import sys
from subprocess import Popen
import subprocess
import schedule 
import time 
from datetime import datetime


def c(script_name):
    j = 0
    for process in psutil.process_iter():
        try: 
            if process.cmdline() == ['py',f"{script_name}"]:
                #print(process.cmdline())
                print("**********************************************")
                print('Process found. No need to start.')
                print("**********************************************")
                return
            else:
                pass
                # {process.cmdline()} 
                # print(f"Nope. Process {j} isn't it.")

            j += 1

        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):

            pass
    print("**********************************************")
    print("Couldn't find that process. Let's start it up.")
    print("**********************************************")

    #will open process in a new terminal for ease.
    subprocess.call('py main.py', creationflags=subprocess.CREATE_NEW_CONSOLE)

    #Popen(['py', f"{script_name}"])

# 03/07/21

# I keep getting this error that I'm not passing a callable? But I am?
# schedule.every(10).seconds.do(c("main.py"),)

#So, we'll do it live. 

i = 0

while True:
    i += 1
    print("============")
    print("------------")
    print(f"Round {i}:")
    print(f"Time and date: {datetime.now()}")
    c("main.py")
    print("------------")
    print("============")
    time.sleep(600)
