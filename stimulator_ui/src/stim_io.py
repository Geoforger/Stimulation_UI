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
        self.lock = threading.Lock()
        self.polling_thread = None
        self.polling_active = False

    def write(self, data):
        with self.lock:
            self.ser.write(data)

    def read(self, size):
        with self.lock:
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

    def start_polling(self, update_callback):
        if not self.polling_active:
            self.polling_active = True
            self.polling_thread = threading.Thread(target=self.poll_serial, args=(update_callback,))
            self.polling_thread.daemon = True
            self.polling_thread.start()

    def stop_polling(self):
        if self.polling_active:
            self.polling_active = False
            if self.polling_thread:
                self.polling_thread.join()

    def poll_serial(self, update_callback):
        while self.polling_active:
            try:
                data = self.read(32).decode('utf-8').strip()
                if data:
                    if data.startswith("<A,"):
                        stim_amp = float(data[3:-1])
                        update_callback(stim_amp, None)
                    elif data.startswith("<P,"):
                        pulse_width = float(data[3:-1])
                        update_callback(None, pulse_width)
                    elif data.startswith("<T>"):
                        update_callback(None, None, toggle=True)
            except Exception as e:
                update_callback(None, None, error=str(e))

    def close(self):
        self.stop_polling()
        self.ser.close()

