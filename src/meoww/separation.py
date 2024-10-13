import subprocess
import threading
import time


# A blocking task that launches a GUI program in non-blocking mode
def blocking_task():
    # Start the GUI app and redirect stdout/stderr to prevent blocking
    subprocess.Popen(
        ["data/audacity-linux-3.6.4-x64.AppImage"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


# Function to handle user input
def input_loop():
    start_blocking_task()


# Start the blocking task in a separate thread
def start_blocking_task():
    task_thread = threading.Thread(target=blocking_task)
    task_thread.daemon = True  # Daemon thread will exit when the main program exits
    task_thread.start()


# Start the input loop in a separate thread
def main():
    input_thread = threading.Thread(target=input_loop)
    input_thread.daemon = True  # Keep the input thread running until the program exits
    input_thread.start()

    # Keep the main thread alive while input_thread is running
    while input_thread.is_alive():
        time.sleep(0.1)  # Main loop idling


if __name__ == "__main__":
    main()
