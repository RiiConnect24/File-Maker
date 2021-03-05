from sys import argv
from cmoc import ResetList

try:
    listname = argv[1].upper().encode()  # converts to uppercase, then passed as bytes
    ResetList(listname)

except IndexError as error:
    print("No list provided! Usage: python3 ./reset.py [type]")
    print("Available types are SL, PL, RL, NL, RL")
    print("This will remove all miis in the specified list!")

except ValueError as error:
    print("Invalid List! Usage: python3 ./reset.py [type]")
    print("Available types are SL, PL, RL, NL, RL")
    print("This will remove all miis in the specified list!")
