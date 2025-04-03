import serial
import threading

class UART_COMMS():
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.comm_state = 1     # 0: User Mode, 1: PC Mode
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
    
    def readline(self):
        with self.lock:
            return self.ser.readline()
    
    def STOP(self, attempts=100):
        msg = b"<STOP>"
        for _ in range(attempts):              # retry up to × times
            self.write(msg)
            resp = self.readline().decode()
            if "<ACK>" in resp:
                return True
        return False 
    
    def toggle_PC_usr(self, attempts=5):
        msg = b"<T>"
        for _ in range(attempts):              # retry up to × times
            self.write(msg)
            resp = self.readline().decode()
            if "<ACK>" in resp:
                self.comm_state ^= 1
                return True
        return False

    def toggle_trigger(self):
        msg = b"<EX>"
        self.write(msg)

    def toggle_recording(self):
        # NOTE: This may require a stop, reset command before toggling to prevent any issues
        msg = b"<STIM>"
        self.write(msg)

    def set_stim_amplitude(self, amplitude):
        msg = f"<A,{amplitude}>".encode()
        self.write(msg)

    def set_pulse_width(self, width):
        msg = f"<P,{width}>".encode()
        self.write(msg)

    def close(self):
        self.ser.close()

