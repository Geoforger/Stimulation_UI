import serial

class USER_COMMS:
    def __init__(self, port='/dev/ttyS0', baudrate=9600):
        """
        Initialize the serial communication with the specified port and baudrate.
        """
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1  # 1 second timeout for read operations
        )

    def write(self, data):
        self.ser.write(data)

    def read(self, size):
        return self.ser.read(size)

    def readline(self):
        return self.ser.readline()

    def close(self):
        self.ser.close()