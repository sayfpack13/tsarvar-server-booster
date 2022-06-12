import Tools
from settings import *

option = 0



while True:
    while option < 1 or option > 4:
        print("1) generate accounts")
        print("2) vote server")
        print("3) both")
        print("4) Exit")

        option = int(input("Select option: "))

    if option == 4:
        exit()

    if option == 1:
        Tools.option1()

    if option==2:
        Tools.option2()


    if option==3:
        Tools.option1()
        Tools.option2()

    option = 0


