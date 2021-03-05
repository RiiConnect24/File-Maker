from time import sleep
from os import system

# temporary until we set up cron

while True:
    system("./ForceUpdate.sh")
    sleep(1800)
