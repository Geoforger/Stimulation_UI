import serial

class UART_COMMS():
    def __init__(self, port='/dev/serial0', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(
            port=self.port,      # Update as needed for your configuration
            baudrate=self.baudrate,            # Set the baudrate; adjust as needed
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1                 # 1 second timeout for read operations
        )

    def write(self, data):
        self.ser.write(data)

    def read(self, size):
        return self.ser.read(size)

    def close(self):
        self.ser.close()