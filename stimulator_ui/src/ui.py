from tkinter import Tk, Button, Checkbutton, IntVar, Label, StringVar, Text, Entry, END, DISABLED, NORMAL
from datetime import datetime
from stim_io import UART_COMMS

class AppUI:
    def __init__(self, master):
        self.master = master
        master.title("Test Stimulator App") 

        # Initialize serial communication
        self.uart = UART_COMMS()

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
        self.stim_up_but = Button(master, text="+", command=self.stim_amp_up, width=10, height=2)
        self.stim_up_but.grid(row=1, column=0, padx=10, pady=10)

        self.stim_down_but = Button(master, text="-", command=self.stim_amp_down, width=10, height=2)
        self.stim_down_but.grid(row=1, column=1, padx=10, pady=10)

        self.pulse_up_but = Button(master, text="+", command=self.pulse_width_up, width=10, height=2)
        self.pulse_up_but.grid(row=3, column=0, padx=10, pady=10)

        self.pulse_down_but = Button(master, text="-", command=self.pulse_width_down, width=10, height=2)
        self.pulse_down_but.grid(row=3, column=1, padx=10, pady=10)

        self.STOP_but = Button(master, text="STOP", command=self.STOP, width=10, height=2)
        self.STOP_but.grid(row=4, column=2, rowspan=3, padx=10, pady=10)

        # Entry boxes for manual input
        self.stim_amplitude_entry = Entry(master)
        self.stim_amplitude_entry.grid(row=1, column=2, padx=10, pady=10)
        self.stim_amplitude_entry.bind("<Return>", self.update_stim_amplitude)

        self.pulse_width_entry = Entry(master)
        self.pulse_width_entry.grid(row=3, column=2, padx=10, pady=10)
        self.pulse_width_entry.bind("<Return>", self.update_pulse_width)

        # Switches
        self.triggers_label = Label(master, text="Triggers (Internal - External)")
        self.triggers_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.switch_var = IntVar()
        self.triggers_switch = Checkbutton(master, text="", variable=self.switch_var, command=self.toggle_switch)
        self.triggers_switch.grid(row=6, column=0, columnspan=2, padx=10, pady=0)

        self.recording_switch_var = IntVar()
        self.recording_switch = Checkbutton(master, text="Recording - Stimulation", variable=self.recording_switch_var, command=self.toggle_recording)
        self.recording_switch.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.pc_user_switch_var = IntVar()
        self.pc_user_switch = Checkbutton(master, text="PC - User", variable=self.pc_user_switch_var, command=self.toggle_pc_user)
        self.pc_user_switch.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Event log
        self.event_log = Text(master, width=40, height=20)
        self.event_log.grid(row=0, column=3, rowspan=9, padx=10, pady=10)

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
        self.log_event("STIMULATION STOPPED")

    def toggle_switch(self):
        if self.switch_var.get():
            self.log_event("INTERNAL TRIGGERS")
        else:
            self.log_event("EXTERNAL TRIGGERS")

    def toggle_recording(self):
        if self.recording_switch_var.get():
            self.log_event("Recording Mode Enabled")
            self.recording_ui()
        else:
            self.log_event("Stimulation Mode Enabled")
            self.stimulation_ui()

    def toggle_pc_user(self):
        if self.pc_user_switch_var.get():
            self.log_event("PC Mode Enabled")
            self.pc_mode_ui()
        else:
            self.log_event("User Mode Enabled")
            self.user_mode_ui()

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
        self.update_from_serial()

    def user_mode_ui(self):
        self.stim_up_but.config(state=NORMAL)
        self.stim_down_but.config(state=NORMAL)
        self.pulse_up_but.config(state=NORMAL)
        self.pulse_down_but.config(state=NORMAL)
        self.stim_amplitude_entry.config(state=NORMAL)
        self.pulse_width_entry.config(state=NORMAL)
        self.triggers_switch.config(state=NORMAL)
        self.recording_switch.config(state=NORMAL)

    def update_from_serial(self):
        try:
            while self.pc_user_switch_var.get():
                data = self.uart.read(32).decode('utf-8').strip()
                if data:
                    stim_amp, pulse_width = map(float, data.split(','))
                    self.stim_amplitude = stim_amp
                    self.pulse_width = pulse_width
                    self.stim_amplitude_var.set(f"Stim Amplitude: {self.stim_amplitude:.2f}uA")
                    self.pulse_width_var.set(f"Pulse Width: {self.pulse_width:.2f}")
                    self.log_event(f"Updated from PC: Stim Amplitude: {self.stim_amplitude:.2f}uA, Pulse Width: {self.pulse_width:.2f}")
        except Exception as e:
            self.log_event(f"Error reading from serial: {e}")

    def update_stim_amplitude(self, event):
        try:
            value = float(self.stim_amplitude_entry.get())
            self.stim_amplitude = value
            self.stim_amplitude_var.set(f"Stim Amplitude: {self.stim_amplitude:.2f}uA")
            self.log_event(f"Set Stimulation Amplitude to {self.stim_amplitude:.2f}uA")
            if self.pc_user_switch_var.get():
                self.uart.write(f"{self.stim_amplitude},{self.pulse_width}\n".encode('utf-8'))
        except ValueError:
            self.log_event("Invalid input for Stimulation Amplitude")

    def update_pulse_width(self, event):
        try:
            value = float(self.pulse_width_entry.get())
            self.pulse_width = value
            self.pulse_width_var.set(f"Pulse Width: {self.pulse_width:.2f}")
            self.log_event(f"Set Pulse Width to {self.pulse_width:.2f}")
            if self.pc_user_switch_var.get():
                self.uart.write(f"{self.stim_amplitude},{self.pulse_width}\n".encode('utf-8'))
        except ValueError:
            self.log_event("Invalid input for Pulse Width")

if __name__ == "__main__":
    root = Tk()
    app = AppUI(root)
    root.mainloop()