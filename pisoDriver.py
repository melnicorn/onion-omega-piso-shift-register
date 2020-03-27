import onionGpio
import logging

# Driver for the 74HC165 chip
class PISO:
    # Instantiates the shift register based on the specified pins
    def __init__(self, loadPin, clockEnablePin, clockPin, dataPin, numberPISO = 1):
        self._loadPin = onionGpio.OnionGpio(loadPin)
        self._clockEnablePin = onionGpio.OnionGpio(clockEnablePin)
        self._clockPin = onionGpio.OnionGpio(clockPin)
        self._dataPin = onionGpio.OnionGpio(dataPin)
        self._dataWidth = numberPISO * 8
        
        self._loadPin.setOutputDirection(0)
        self._clockEnablePin.setOutputDirection(0)
        self._clockPin.setOutputDirection(0)
        self._dataPin.setInputDirection()

        self._clockPin.setValue(0)
        self._loadPin.setValue(1)

    def __del__(self):
        logging.debug('Tearing down PISO object')
        del self._loadPin
        del self._clockEnablePin
        del self._clockPin
        del self._dataPin

    def readRegister(self):
        value = 0x0

        self._clockEnablePin.setValue(1)
        self._loadPin.setValue(0)
        self._loadPin.setValue(1)
        self._clockEnablePin.setValue(0)

        for i in range(self._dataWidth):
            bitVal = self.__readBit()
            value = value | (bitVal << ((self._dataWidth - 1) - i))

        return value

    def dataWidth(self):
        return self._dataWidth
    
    def __readBit(self):
        value = int(self._dataPin.getValue())

        self._clockPin.setValue(1)
        self._clockPin.setValue(0)

        return value