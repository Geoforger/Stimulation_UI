from tkinter import Tk, Button, Checkbutton, IntVar, Label, StringVar, Text, Entry, END, DISABLED, NORMAL
from datetime import datetime
from stim_io import UART_COMMS
import serial
import serial.tools.list_ports

class AppUI:
    def __init__(self, master):
        self.master = master
        master.title("Test Stimulator App") 

        # UI Display variables
        self.stim_amplitude = 0.00
        self.pulse_width = 0.00
        self.nerve_impedance = 0.00

        # Display Labels
        self.stim_amplitude_var = StringVar()
        self.stim_amplitude_var.set(f"Stim Amplitude: {self.stim_amplitude:.2f}uA")
        self.stim_amplitude_label = Label(master, textvariable=self.stim_amplitude_var)
        self.stim_amplitude_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.pulse_width_var = StringVar()
        self.pulse_width_var.set(f"Pulse Width: {self.pulse_width:.2f}")
        self.pulse_width_label = Label(master, textvariable=self.pulse_width_var)
        self.pulse_width_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.nerve_impedance_var = StringVar()
        self.nerve_impedance_var.set(f"Nerve Impedance: {self.nerve_impedance:.2f}ohms")
        self.nerve_impedance_label = Label(master, textvariable=self.nerve_impedance_var)
        self.nerve_impedance_label.grid(row=2, column=2, padx=10, pady=10)

        # UI Buttons
        self.stim_up_but = Button(master, text="+", command=self.stim_amp_up, width=10, height=2, state=DISABLED)
        self.stim_up_but.grid(row=1, column=0, padx=10, pady=10)

        self.stim_down_but = Button(master, text="-", command=self.stim_amp_down, width=10, height=2, state=DISABLED)
        self.stim_down_but.grid(row=1, column=1, padx=10, pady=10)

        self.pulse_up_but = Button(master, text="+", command=self.pulse_width_up, width=10, height=2, state=DISABLED)
        self.pulse_up_but.grid(row=3, column=0, padx=10, pady=10)

        self.pulse_down_but = Button(master, text="-", command=self.pulse_width_down, width=10, height=2, state=DISABLED)
        self.pulse_down_but.grid(row=3, column=1, padx=10, pady=10)

        self.STOP_but = Button(master, text="STOP", command=self.STOP, width=10, height=2, state=DISABLED)
        self.STOP_but.grid(row=4, column=2, rowspan=3, padx=10, pady=10)

        # Reconnect button
        self.reconnect_but = Button(master, text="Reconnect", command=self.initialize_serial, state=NORMAL)
        self.reconnect_but.grid(row=6, column=2, rowspan=3, padx=10, pady=10)

        # Poll Status button
        self.poll_status_but = Button(master, text="Poll Status", command=self.poll_status, width=10, height=2, state=DISABLED)
        self.poll_status_but.grid(row=9, column=2, padx=10, pady=10)

        # Entry boxes for manual input
        self.stim_amplitude_entry = Entry(master, state=DISABLED)
        self.stim_amplitude_entry.grid(row=1, column=2, padx=10, pady=10)
        self.stim_amplitude_entry.bind("<Return>", self.update_stim_amplitude)

        self.pulse_width_entry = Entry(master, state=DISABLED)
        self.pulse_width_entry.grid(row=3, column=2, padx=10, pady=10)
        self.pulse_width_entry.bind("<Return>", self.update_pulse_width)

        # Switches
        self.triggers_label = Label(master, text="Triggers (Internal - External)")
        self.triggers_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.switch_var = IntVar()
        self.triggers_switch = Checkbutton(master, text="", variable=self.switch_var, command=self.toggle_trigger, state=DISABLED)
        self.triggers_switch.grid(row=6, column=0, columnspan=2, padx=10, pady=0)

        self.recording_switch_var = IntVar()
        self.recording_switch = Checkbutton(master, text="Recording - Stimulation", variable=self.recording_switch_var, command=self.toggle_recording, state=DISABLED)
        self.recording_switch.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.pc_user_switch_var = IntVar()
        self.pc_user_switch = Checkbutton(master, text="PC - User", variable=self.pc_user_switch_var, command=self.toggle_pc_user, state=DISABLED)
        self.pc_user_switch.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Event log
        self.event_log = Text(master, width=80, height=20)
        self.event_log.grid(row=0, column=3, rowspan=14, padx=10, pady=10)

        # Initialize serial communication
        self.uart = None
        self.pc_usr_toggle = 1
        self.initialize_serial()

    def initialize_serial(self):
        try:
            # port = self.find_arduino_port()
            # self.uart = UART_COMMS(port=port)
            self.uart = UART_COMMS(port='/dev/ttyACM0', baudrate=9600)  # Currently the default port found on pi
            self.pc_usr_toggle = self.uart.comm_state
            self.enable_ui()
            self.reconnect_but.config(state=DISABLED)
            self.log_event("Serial connection established")
        except Exception as e:
            self.log_event(f"Failed to establish serial connection: {e}")
            self.disable_ui()
            self.reconnect_but.config(state=NORMAL)

    def log_event(self, event):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.event_log.insert(END, f"{timestamp} - {event}\n")
        self.event_log.see(END)

    def stim_amp_up(self):
        self.stim_amplitude += 1.00
        self.stim_amplitude_var.set(f"Stim Amplitude: {self.stim_amplitude:.2f}uA")
        self.log_event(f"Increased Stimulation Amplitude to {self.stim_amplitude:.2f}uA")

    def stim_amp_down(self):
        self.stim_amplitude -= 1.00
        self.stim_amplitude_var.set(f"Stim Amplitude: {self.stim_amplitude:.2f}uA")
        self.log_event(f"Decreased Stimulation Amplitude to {self.stim_amplitude:.2f}uA")

    def pulse_width_up(self):
        self.pulse_width += 1.00
        self.pulse_width_var.set(f"Pulse Width: {self.pulse_width:.2f}")
        self.log_event(f"Increased Pulse Width to {self.pulse_width:.2f}")

    def pulse_width_down(self):
        self.pulse_width -= 1.00
        if self.pulse_width < 0:
            self.pulse_width = 0
        self.pulse_width_var.set(f"Pulse Width: {self.pulse_width:.2f}")
        self.log_event(f"Decreased Pulse Width to {self.pulse_width:.2f}")

    def STOP(self):
        if self.uart:
            ack = self.uart.STOP()
        if ack:
            self.log_event("STIMULATION STOPPED")
        else:
            self.log_event("STOP ACK not received")

    def toggle_trigger(self):
        if self.uart:
            self.uart.toggle_trigger()
        if self.switch_var.get():
            self.log_event("INTERNAL TRIGGERS")
        else:
            self.log_event("EXTERNAL TRIGGERS")

    def toggle_recording(self):
        if self.uart:
            self.uart.toggle_recording()
        if self.recording_switch_var.get():
            self.log_event("Recording Mode Enabled")
            self.recording_ui()
        else:
            self.log_event("Stimulation Mode Enabled")
            self.stimulation_ui()

    def toggle_pc_user(self):
        if self.uart:
            ack = self.uart.toggle_PC_usr()
        if ack:
            self.pc_usr_toggle ^= 1
            if self.pc_user_switch_var.get():
                self.log_event("PC Mode Enabled")
                self.pc_mode_ui()
            else:
                self.log_event("User Mode Enabled")
                self.user_mode_ui()
        else:
            self.log_event("User Toggle ACK not received")

    def recording_ui(self):
        self.stim_up_but.config(state=DISABLED)
        self.stim_down_but.config(state=DISABLED)
        self.pulse_up_but.config(state=DISABLED)
        self.pulse_down_but.config(state=DISABLED)
        self.stim_amplitude_entry.config(state=DISABLED)
        self.pulse_width_entry.config(state=DISABLED)
        self.triggers_switch.config(state=DISABLED)
        self.pc_user_switch.config(state=DISABLED)

    def stimulation_ui(self):
        self.stim_up_but.config(state=NORMAL)
        self.stim_down_but.config(state=NORMAL)
        self.pulse_up_but.config(state=NORMAL)
        self.pulse_down_but.config(state=NORMAL)
        self.stim_amplitude_entry.config(state=NORMAL)
        self.pulse_width_entry.config(state=NORMAL)
        self.triggers_switch.config(state=NORMAL)
        self.pc_user_switch.config(state=NORMAL)

    def pc_mode_ui(self):
        self.stim_up_but.config(state=DISABLED)
        self.stim_down_but.config(state=DISABLED)
        self.pulse_up_but.config(state=DISABLED)
        self.pulse_down_but.config(state=DISABLED)
        self.stim_amplitude_entry.config(state=DISABLED)
        self.pulse_width_entry.config(state=DISABLED)
        self.triggers_switch.config(state=DISABLED)
        self.recording_switch.config(state=DISABLED)

    def user_mode_ui(self):
        self.stim_up_but.config(state=NORMAL)
        self.stim_down_but.config(state=NORMAL)
        self.pulse_up_but.config(state=NORMAL)
        self.pulse_down_but.config(state=NORMAL)
        self.stim_amplitude_entry.config(state=NORMAL)
        self.pulse_width_entry.config(state=NORMAL)
        self.triggers_switch.config(state=NORMAL)
        self.recording_switch.config(state=NORMAL)

    def update_stim_amplitude(self, event):
        try:
            value = float(self.stim_amplitude_entry.get())
            self.stim_amplitude = value
            self.stim_amplitude_var.set(f"Stim Amplitude: {self.stim_amplitude:.2f}uA")
            self.log_event(f"Set Stimulation Amplitude to {self.stim_amplitude:.2f}uA")
            if self.pc_usr_toggle == 1:
                self.uart.write(f"{self.stim_amplitude},{self.pulse_width}\n".encode('utf-8'))
        except ValueError:
            self.log_event("Invalid input for Stimulation Amplitude")

    def update_pulse_width(self, event):
        try:
            value = float(self.pulse_width_entry.get())
            self.pulse_width = value
            self.pulse_width_var.set(f"Pulse Width: {self.pulse_width:.2f}")
            self.log_event(f"Set Pulse Width to {self.pulse_width:.2f}")
            if self.pc_usr_toggle == 1:
                self.uart.write(f"{self.stim_amplitude},{self.pulse_width}\n".encode('utf-8'))
        except ValueError:
            self.log_event("Invalid input for Pulse Width")

    def disable_ui(self):
        self.stim_up_but.config(state=DISABLED)
        self.stim_down_but.config(state=DISABLED)
        self.pulse_up_but.config(state=DISABLED)
        self.pulse_down_but.config(state=DISABLED)
        self.stim_amplitude_entry.config(state=DISABLED)
        self.pulse_width_entry.config(state=DISABLED)
        self.triggers_switch.config(state=DISABLED)
        self.recording_switch.config(state=DISABLED)
        self.pc_user_switch.config(state=DISABLED)
        self.STOP_but.config(state=DISABLED)

    def enable_ui(self):
        self.stim_up_but.config(state=NORMAL)
        self.stim_down_but.config(state=NORMAL)
        self.pulse_up_but.config(state=NORMAL)
        self.pulse_down_but.config(state=NORMAL)
        self.stim_amplitude_entry.config(state=NORMAL)
        self.pulse_width_entry.config(state=NORMAL)
        self.triggers_switch.config(state=NORMAL)
        self.recording_switch.config(state=NORMAL)
        self.pc_user_switch.config(state=NORMAL)
        self.STOP_but.config(state=NORMAL)

    def close(self):
        if self.uart:
            self.STOP()
            self.uart.close()
        self.master.destroy()

    def find_arduino_port(self):
        # List all available ports
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            # Check if "Arduino" appears in the description
            # or if the device name matches common Arduino naming conventions.
            if "Arduino" in port.description or port.device.startswith("/dev/ttyACM") or port.device.startswith("/dev/ttyUSB"):
                return port.device
        return None
    
    def poll_status(self):
        """Send an <ACK> message to the serial device and log the response."""
        if self.uart:
            try:
                self.uart.write(b"<ACK>")
                response = self.uart.readline().decode('utf-8').strip()
                self.log_event(f"Poll Status Response: {response}")
            except Exception as e:
                self.log_event(f"Error polling status: {e}")

if __name__ == "__main__":
    root = Tk()
    app = AppUI(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()