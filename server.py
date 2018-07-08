#   Heights sockets Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017

import datetime
import socket
import subprocess
import shutil
from PIL import ImageGrab
import glob
import os
from distutils.spawn import find_executable

IP = "0.0.0.0"
PORT = 1729


def receive_client_request(client_socket):
    command = client_socket.recv(1024)
    print command
    if "EXIT" == command[:] or "TAKE_SCREENSHOT" == command[:]:
        return command[:], ""
    return command[:command.index(" ")], command[command.index(" ") + 1:]


def check_client_request(command, params):
    if command == "SEND_FILE":
        return os.path.exists(params), "File does not exist"
    elif command == "TAKE_SCREENSHOT":
        return True, "Error"
    elif command == "DIR":
        return os.path.isdir(params), "Directory does not exist"
    elif command == "DELETE":
        return os.path.exists(params), "File doesnt exist"
    elif command == "COPY":
        return os.path.exists(params[:params.index(".") + 4]) and os.path.exists(params[params.index(".") + 4:]), "Failed"
    elif command == "EXECUTE":
        return find_executable('notepad.exe') is not None, "Cannot execute command"
    else:
        return True, "Invalid command"


def handle_client_request(command, params):
    if command == "TAKE_SCREENSHOT":
        ImageGrab.grab().save(str(datetime.datetime.now().second)+'.jpg', 'JPEG')
        return "Screenshot taken"
    elif command == "DIR":
        return glob.glob(params + "//*")
    elif command == "SEND_FILE":
        return params
    elif command == "DELETE":
        os.remove(params)
        return "Picture deleted"
    elif command == "COPY":
        shutil.copy(params[:params.index(".") + 4], params[params.index(".") + 4:])
        return "File copied"
    elif command == "EXECUTE":
        subprocess.call(params, shell=True)
        return "File executed"


#server
def send_response_to_client(response, client_socket, command):
    """Create a protocol which sends the response to the client

    The protocol should be able to handle short responses as well as files
    (for example when needed to send the screenshot to the client)
    """
    if command == "SEND_FILE":
        with open(str(response), "rb") as filename:
            data = filename.read(1024)
            while data:
                client_socket.send(data)
                data = filename.read(1024)
                print "Image sending..."
            print "Image sent!"
            client_socket.send("Image sent!")
    else:
        client_socket.send(str(response))


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()

    # handle requests until user asks to exit
    done = False
    while not done:
        command, params = receive_client_request(client_socket)
        params = params.replace(" ", "")
        params = params.replace("\\", "/")
        command = command.replace(" ", "")
        valid, error_msg = check_client_request(command, params)
        if valid:
            response = handle_client_request(command, params)
            send_response_to_client(response, client_socket, command)
        else:
            send_response_to_client(error_msg, client_socket, '')

        if command == 'EXIT':
            done = True

    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()