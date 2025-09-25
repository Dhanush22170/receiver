import socket
import os
import time

# ========== CONFIGURATION ==========
HOST = ' 192.168.1.6'  # This must be the IP of the receiving machine
PORT = 9999
SAVE_DIRECTORY = 'received_files'

# ========== Setup ==========
try:
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)
        print(f"✅ Created save directory: {SAVE_DIRECTORY}")

    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"👂 Listening for incoming connections on {HOST}:{PORT}")

    conn, addr = server.accept()
    print(f"✅ Connection established with {addr[0]}:{addr[1]}")

    # ========== Receive File ==========
    file_name = conn.recv(1024).decode()
    if not file_name:
        print("❌ Did not receive a file name. Connection closed.")
        conn.close()
        server.close()
        exit()

    file_path = os.path.join(SAVE_DIRECTORY, file_name)
    print(f"📥 Receiving file: {file_name}")

    with open(file_path, 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)

    print(f"✅ File saved successfully to: {file_path}")

except Exception as e:
    print(f"❌ An error occurred: {e}")

finally:
    # ========== Cleanup ==========
    if 'conn' in locals():
        conn.close()
    if 'server' in locals():
        server.close()
    print("Connection closed.")