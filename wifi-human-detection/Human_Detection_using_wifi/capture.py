import serial
import time
import os

PORT = 'COM3'
BAUD = 115200
ACTIVITY = 'walking'
SESSION = '3'

save_dir = f'data/{ACTIVITY}'
os.makedirs(save_dir, exist_ok=True)
filename = f'{save_dir}/session{SESSION}.csv'

print(f"Recording {ACTIVITY} session {SESSION}")
print(f"Saving to: {filename}")
print("Make sure phone is connected to ESP32_CSI")
print("Press Ctrl+C to stop\n")

with serial.Serial(PORT, BAUD, timeout=2) as ser:
    with open(filename, 'w') as f:
        header_written = False
        count = 0
        buffer = ''
        
        while True:
            try:
                # Read raw bytes and accumulate
                chunk = ser.read(ser.in_waiting or 1).decode('utf-8', errors='ignore')
                buffer += chunk
                
                # Process complete lines ending with ]
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    # If CSI_DATA line is split, join with next chunk
                    if line.startswith('CSI_DATA') and not line.endswith(']'):
                        # incomplete line, put back and wait for more
                        buffer = line + '\n' + buffer
                        break
                    
                    if 'type,role,mac' in line and not header_written:
                        f.write(line + '\n')
                        f.flush()
                        header_written = True
                        print("Header written.")
                    
                    elif line.startswith('CSI_DATA') and line.endswith(']'):
                        f.write(line + '\n')
                        f.flush()
                        count += 1
                        print(f"Rows captured: {count}", end='\r')
                        
            except KeyboardInterrupt:
                print(f"\nDone. {count} rows saved to {filename}")
                break