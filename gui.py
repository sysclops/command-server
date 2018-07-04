import sys
from PyQt4 import QtGui, QtCore
import socket
import Pillow

IP = '127.0.0.1'
PORT = 1729


class Window(QtGui.QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50, 50, 500, 300)
		self.setWindowTitle("Command server!")
		self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

		extractAction = QtGui.QAction("&Exit the app", self)
		extractAction.setShortcut("Ctrl+Q")
		extractAction.setStatusTip('Leave The App')
		extractAction.triggered.connect(self.close_application)

		openEditor = QtGui.QAction("&Editor", self)
		openEditor.setShortcut("Ctrl+E")
		openEditor.setStatusTip('Open Editor')
		openEditor.triggered.connect(self.editor)

		mainMenu = self.menuBar()
		editorMenu = mainMenu.addMenu("&Editor")
		editorMenu.addAction(openEditor)

		self.home()

	def home(self):
		btn = QtGui.QPushButton("Quit", self)
		btn.clicked.connect(self.close_application)
		btn.resize(btn.minimumSizeHint())
		btn.move(0, 100)

		extractAction = QtGui.QAction(QtGui.QIcon('todachoppa.png'), 'Flee the Scene', self)
		extractAction.triggered.connect(self.close_application)
		self.toolBar = self.addToolBar("Extraction")
		self.toolBar.addAction(extractAction)

		fontChoice = QtGui.QAction('Font', self)
		fontChoice.triggered.connect(self.font_choice)
		# self.toolBar = self.addToolBar("Font")
		self.toolBar.addAction(fontChoice)

		color = QtGui.QColor(0, 0, 0)

		fontColor = QtGui.QAction('Font bg Color', self)
		fontColor.triggered.connect(self.color_picker)

		self.toolBar.addAction(fontColor)

		checkBox = QtGui.QCheckBox('Enlarge Window', self)
		checkBox.move(300, 25)
		checkBox.stateChanged.connect(self.enlarge_window)

		comboBox = QtGui.QComboBox(self)
		comboBox.addItem("motif")
		comboBox.addItem("Windows")
		comboBox.addItem("cde")
		comboBox.addItem("Plastique")
		comboBox.addItem("Cleanlooks")

		comboBox.move(50,250)
		self.styleChoice.move(50, 150)
		comboBox.activated[str].connect(self.style_choice)

		self.show()

	def color_picker(self):
		color = QtGui.QColorDialog.getColor()
		self.styleChoice.setStyleSheet("QWidget { background-color: %s}" % color.name())

	def editor(self):
		self.textEdit = QtGui.QTextEdit()
		self.setCentralWidget(self.textEdit)

	def style_choice(self, text):
		self.styleChoice.setText(text)
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))

	def close_application(self):
		choice = QtGui.QMessageBox.question(self, 'Extract!', "Get into the chopper?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if choice == QtGui.QMessageBox.Yes:
			print("Extracting Naaaaaaoooww!!!!")
			sys.exit()
		else:
			pass

	def valid_request(request):
		if "TAKE_SCREENSHOT" in request or "DIR" in request or "DELETE" in request or \
			"COPY" in request or "EXECUTE" in request or "EXIT" in request or "SEND_FILE" in request:
				return True
		return False

	def send_request_to_server(my_socket, request):
            if len(request) <= 9:
                my_socket.send("0" + str(len(request)) + request)
            else:
                my_socket.send(str(len(request)) + request)

        def handle_server_response(my_socket, request):
            """Receive the response from the server and handle it, according to the request

            For example, DIR should result in printing the contents to the screen,
            while SEND_FILE should result in saving the received file and notifying the user
            """
            if "SEND_FILE" in request:
                newfile = open('D:\\newimage.jpg', 'wb')
                while True:
                    data = my_socket.recv(1024)
                    newfile.write(data)
                    if "Image sent!" in data:
                        break
                print "Image sent!"
            else:
                print my_socket.recv(1024)

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

def main():
	# open socket with the server

	my_socket = socket.socket(socket.af_inet, socket.sock_stream)
    my_socket.connect((ip, port))
    # print instructions
    print('welcome to remote computer application. available commands are:\n')
    print('take_screenshot\nsend_file\ndir\ndelete\ncopy\nexecute\nexit')
    done = False
    # loop until user requested to exit
    while not done:
        run()
        request = raw_input("please enter command:\n")
        if valid_request(request):
            send_request_to_server(my_socket, request)
            handle_server_response(my_socket, request)
            if request == 'exit':
                done = True
    my_socket.close()

