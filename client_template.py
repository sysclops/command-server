import socket

IP = "127.0.0.1"
PORT = 1729


def valid_request(request):
    if "TAKE_SCREENSHOT" in request or "DIR" in request or "DELETE" in request or \
            "COPY" in request or "EXECUTE" in request or "EXIT" in request or "SEND_FILE" in request:
        return True

    return False


def send_request_to_server(my_socket, request):
    my_socket.send(request)


def handle_server_response(my_socket, request):
    """Receive the response from the server and handle it, according to the request

    For example, DIR should result in printing the contents to the screen,
    while SEND_FILE should result in saving the received file and notifying the user
    """
    if "SEND_FILE" in request:
        newfile = open('B:\\newimage.jpg', 'wb')
        while True:
            data = my_socket.recv(1024)
            newfile.write(data)
            if "Image sent!" in data:
                break
        print "Image sent!"
    else:
        print my_socket.recv(1024)


def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, PORT))

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_FILE\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    done = False
    # loop until user requested to exit
    while not done:
        request = raw_input("Please enter command:\n")
        if valid_request(request):
            send_request_to_server(my_socket, request)
            handle_server_response(my_socket, request)
            if request == 'EXIT':
                done = True
    my_socket.close()


if __name__ == '__main__':
    main()
