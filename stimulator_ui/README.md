# Simulator UI App

This app provides the stimulation system with a basic user interface (UI) to interact with, and read out the state of the system. This system is designed to run on a Raspberry Pi 3B running the 64-bit Raspberry Pi OS.


## Project Structure

```
stimulator_ui
├── src
│   ├── app.py            # Main entry point of the application
│   ├── ui.py             # UI components and button functionalities
│   ├── stim_io.py        # Serial communication protocols for MCU connection
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

A working image of the OS, with this app included, is available from <url>.

If you are looking to install to your own Raspberry Pi, without reformatting, follow these instructions:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd my-python-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/app.py
   ```

## Usage

This app expects a connection between the systems' switching board MCU and the Raspberry Pi GPIO pins according to the circuit diagram below. This is to allow for simple UART communication between the UI and the system.

CIRCUIT DIAGRAM HERE

Once you have made these connections, launch the app. It will launch displaying the following interface:

IMAGE OF UI

- This basic UI will allow for the setting of stimulation parameters amplitude and pulse width.
- The log will display time stamps events that have occured within the system since startup. Note: This system will not log any system states before the UI has been initialised.
- Toggling the 'Triggers' switch will enable external triggering, this will require further hardware to enable these hardware triggers. Default: Internal Triggers 
- Toggling the 'Recording - Stimulation' switch will toggle between the 'Recording' and 'Stimulation' states of the system. Default:Recording
- When in the 'Recording' state, the 'Nerve Impedance' value will update based on feedback from the electrodes.
- The 'STOP' button will send a stop message through the entire system, haulting any operating until a reset has been performed.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.