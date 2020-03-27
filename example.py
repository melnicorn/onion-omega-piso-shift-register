import pisoDriver
import onionGpio
import time
from signal import signal, SIGINT

BUTTON_1 = 0x0001
BUTTON_2 = 0x0002
BUTTON_3 = 0x0004
BUTTON_4 = 0x0008
BUTTON_5 = 0x0010
BUTTON_6 = 0x0020
BUTTON_7 = 0x0030
BUTTON_8 = 0x0040

class TestPISO:
    def __init__(self):
        self.__piso = pisoDriver.PISO(2, 1, 3, 0)
        self.__running = False

    def loop(self):
        oldValue = 0x0
        self.__running = True
        while self.__running:
            value = self.__piso.readRegister()
            if oldValue != value and value > 0x0:
                self.__print(value)
            oldValue = value
            time.sleep(0.001)
        
        exit(0)

    def __print(self, value):
        if value & BUTTON_1 == BUTTON_1:
            print('Button 1')
        if value & BUTTON_2 == BUTTON_2:
            print('Button 2')
        if value & BUTTON_3 == BUTTON_3:
            print('Button 3')
        if value & BUTTON_4 == BUTTON_4:
            print('Button 4')
        if value & BUTTON_5 == BUTTON_5:
            print ('Button 5')
        if value & BUTTON_6 == BUTTON_6:
            print ('Button 6')
        if value & BUTTON_7 == BUTTON_7:
            print ('Button 7')
        if value & BUTTON_8 == BUTTON_8:
            print ('Button 8')

    def kill(self):
        self.__running = False

instance = None

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    instance.kill()

if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    print('Running. Press CTRL-C to exit.')
   
    instance = TestPISO()
    instance.loop()