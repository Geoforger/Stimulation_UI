import tkinter as tk
from tkinter import messagebox
import serial.tools.list_ports

class SerialSearchApp:
    def __init__(self, master):
        self.master = master
        master.title("Serial Device Setup")

        # Step tracking
        self.step = 0
        self.detected_devices = []
        self.control_board_serial = None
        self.user_board_serial = None

        # Instructions label
        self.instruction_label = tk.Label(master, text="Step 1: Disconnect all USB devices from the system.", font=("Arial", 12))
        self.instruction_label.pack(pady=20)

        # Action button
        self.action_button = tk.Button(master, text="Next", command=self.next_step, width=20, height=2)
        self.action_button.pack(pady=10)

        # Event log
        self.event_log = tk.Text(master, width=60, height=15, state=tk.DISABLED)
        self.event_log.pack(pady=20)

    def log_event(self, message):
        """Log a message to the event log."""
        self.event_log.config(state=tk.NORMAL)
        self.event_log.insert(tk.END, f"{message}\n")
        self.event_log.see(tk.END)
        self.event_log.config(state=tk.DISABLED)

    def next_step(self):
        """Handle the next step in the setup process."""
        if self.step == 0:
            self.log_event("Step 1 complete: All USB devices disconnected.")
            self.instruction_label.config(text="Step 2: Plug in the control board USB cable to the Raspberry Pi.")
            self.action_button.config(text="Control Board Connected")
            self.step += 1
        elif self.step == 1:
            self.log_event("Detecting control board...")
            new_device = self.detect_new_device()
            if new_device:
                self.control_board_serial = new_device
                self.log_event(f"Control board detected: {new_device}")
                self.instruction_label.config(text="Step 3: Plug in the user board USB cable to the Raspberry Pi.")
                self.action_button.config(text="User Board Connected")
                self.step += 1
            else:
                messagebox.showerror("Error", "No new USB device detected. Please try again.")
        elif self.step == 2:
            self.log_event("Detecting user board...")
            new_device = self.detect_new_device()
            if new_device:
                self.user_board_serial = new_device
                self.log_event(f"User board detected: {new_device}")
                self.instruction_label.config(text="Setup complete! Serial numbers saved to 'device_serials.txt'.")
                self.action_button.config(state=tk.DISABLED)
                self.save_serials()
                self.step += 1
            else:
                messagebox.showerror("Error", "No new USB device detected. Please try again.")

    def detect_new_device(self):
        """Detect a new USB device by comparing the current list of devices to the previously detected ones."""
        current_devices = list(serial.tools.list_ports.comports())
        current_serials = [device.serial_number for device in current_devices if device.serial_number]
        new_devices = [serial for serial in current_serials if serial not in self.detected_devices]

        if new_devices:
            self.detected_devices.extend(new_devices)
            return new_devices[0]  # Return the first new device detected
        return None

    def save_serials(self):
        """Save the detected serial numbers to a text file."""
        with open("device_serials.txt", "w") as file:
            file.write(f"Control Board Serial: {self.control_board_serial}\n")
            file.write(f"User Board Serial: {self.user_board_serial}\n")
        self.log_event("Serial numbers saved to 'device_serials.txt'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialSearchApp(root)
    root.mainloop()