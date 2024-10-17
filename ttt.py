import time
import subprocess
import logging



def is_anydesk_running():
    try:
        # Check if AnyDesk is running
        output = subprocess.check_output(['pgrep', 'AnyDesk'])
        return bool(output)
    except subprocess.CalledProcessError:
        return False

def start_anydesk():
    try:
        # Start AnyDesk with elevated privileges
        subprocess.Popen(['sudo', './start_anydesk.sh'])
        logging.debug("AnyDesk started.")
    except Exception as e:
        logging.error(f"An error occurred while trying to start AnyDesk: {e}")

def set_process_priority(pid):
    try:
        # Set process priority to higher level (lower nice value means higher priority)
        subprocess.check_call(['renice', '-n', '-20', '-p', str(pid)])
        logging.debug(f"Set higher priority for AnyDesk process with PID {pid}.")
    except Exception as e:
        logging.error(f"An error occurred while setting priority for AnyDesk: {e}")

def main():
    logging.debug("Script started.")
    while True:
        if not is_anydesk_running():
            start_anydesk()
            time.sleep(2)  # Give time for AnyDesk to start
            try:
                output = subprocess.check_output(['pgrep', 'AnyDesk'])
                anydesk_pids = output.strip().split()
                for pid in anydesk_pids:
                    set_process_priority(pid)
            except subprocess.CalledProcessError:
                logging.error("Failed to get AnyDesk PID.")
        else:
            logging.debug("AnyDesk is already running.")
        time.sleep(5)

if __name__ == "__main__":
    main()

