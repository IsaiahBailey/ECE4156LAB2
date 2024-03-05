import serial
import time

def generate_write_key_commands(base_config_command, base_write_bridge_command, key):
    commands = [
        f'{base_config_command} -f aes_axi.rbf',
        f'{base_write_bridge_command} -lw 0 -h {key[24:32]}',  
        f'{base_write_bridge_command} -lw 10 -h {key[16:24]}', 
        f'{base_write_bridge_command} -lw 20 -h {key[8:16]}',  
        f'{base_write_bridge_command} -lw 30 -h {key[:8]}', 
        #replace the next 4 command with the plaintext values you want make sure to follow the new guidelines for input order
        'FPGA-writeBridge -lw 40 -h 90780000',
        'FPGA-writeBridge -lw 50 -h 78560000',
        'FPGA-writeBridge -lw 60 -h 56340000',
        'FPGA-writeBridge -lw 70 -h 34120000',
        'FPGA-writeBridge -lw 120 -h 1',
        'FPGA-writeBridge -lw 120 -h 0',
        'FPGA-readBridge -lw 80',
        'FPGA-readBridge -lw 90',
        'FPGA-readBridge -lw 100',
        'FPGA-readBridge -lw 110'
    ]
    return commands

def run_putty_commands(serial_port, baud_rate, commands):
    try:
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            time.sleep(2)
            for command in commands:
                ser.write((command + '\r\n').encode())
                time.sleep(0.25)
                response = ser.read_all().decode()
                print(response)

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    serial_port = 'COM3'  # Adjust the COM port accordingly
    baud_rate = 115200

    base_config_command = 'FPGA-writeConfig'
    base_write_bridge_command = 'FPGA-writeBridge'

    # Put your keys, endianness should be flipped from the c code
    keys = [
        '34120000563400007856000090780000',
        '34120000563400007856000090780000',
        '34120000563400007856000090780000',
        '34120000563400007856000090780000',
        '34120000563400007856000090780000'
    ]

    for key in keys:
        commands_to_run = generate_write_key_commands(base_config_command, base_write_bridge_command, key)
        run_putty_commands(serial_port, baud_rate, commands_to_run)
