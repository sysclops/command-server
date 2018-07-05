import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
import socket


class Window(QtGui.QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50, 50, 100, 115)
		self.setWindowTitle("Command server!")
		self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
		

		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.connect(('127.0.0.1', 1729))

		extractAction = QtGui.QAction("&Exit the app", self)
		extractAction.setShortcut("Ctrl+Q")
		extractAction.setStatusTip('Leave The App')
		extractAction.triggered.connect(self.close_application)

		self.home()

	def home(self):
		btn = QtGui.QPushButton("Quit", self)
		btn.clicked.connect(self.close_application)
		btn.resize(btn.minimumSizeHint())
		btn.move(0, 80)

		printScrnAction = QtGui.QAction(QtGui.QIcon('camera.png'), 'Print the screen', self)
		printScrnAction.triggered.connect(self.print_screen)
		self.toolBar = self.addToolBar("Take a screencap")
		self.toolBar.addAction(printScrnAction)

		dirAction = QtGui.QAction(QtGui.QIcon('folder.png'), 'Print contents of directory', self)
		dirAction.triggered.connect(self.directory)
		self.toolBar = self.addToolBar("Print contents of directory")
		self.toolBar.addAction(dirAction)

		deleteAction = QtGui.QAction(QtGui.QIcon('delete.png'), 'Deletes a file', self)
		deleteAction.triggered.connect(self.delete)
		self.toolBar = self.addToolBar("Delete a file")
		self.toolBar.addAction(deleteAction)

		copyAction = QtGui.QAction(QtGui.QIcon('copy.png'), 'Copies a file', self)
		copyAction.triggered.connect(self.copy)
		self.toolBar = self.addToolBar("Copy a file")
		self.toolBar.addAction(copyAction)

		execAction = QtGui.QAction(QtGui.QIcon('execute.png'), 'Executes a file', self)
		execAction.triggered.connect(self.execute)
		self.toolBar = self.addToolBar("Execute a file")
		self.toolBar.addAction(execAction)

		color = QtGui.QColor(0, 0, 0)

		fontColor = QtGui.QAction('Font bg Color', self)
		fontColor.triggered.connect(self.color_picker)
		self.toolBar.addAction(fontColor)

		self.styleChoice = QtGui.QLabel("", self)
		self.styleChoice.move(0, 0)
		self.styleChoice.setGeometry(1, 1, 800, 400)
		comboBox = QtGui.QComboBox(self)
		comboBox.addItem("motif")
		comboBox.addItem("Windows")
		comboBox.addItem("cde")
		comboBox.addItem("Plastique")
		comboBox.addItem("Cleanlooks")

		comboBox.move(0, 50)
		self.styleChoice.move(0, 150)
		comboBox.activated[str].connect(self.style_choice)

		self.show()

	def color_picker(self):
		color = QtGui.QColorDialog.getColor()
		self.styleChoice.setStyleSheet("QWidget { background-color: %s}" % color.name())

	def style_choice(self, text):
		self.styleChoice.setText(text)
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))

	def close_application(self):
		choice = QtGui.QMessageBox.question(self, 'Qutting!', "Are you sure you want to exit the app?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if choice == QtGui.QMessageBox.Yes:
			sys.exit()
		else:
			pass

	def print_screen(self):
		self.send_request_to_server(self.my_socket, "TAKE_SCREENSHOT")
		self.send_request_to_server(self.my_socket,  "SEND_FILE B:/newimage.jpg")
		newfile = open('B:\\newimage.jpg', 'wb')
		while True:
			data = self.my_socket.recv(1024)
			newfile.write(data)
			if "Image sent!" in data:
				break
			popup = QtGui.QMessageBox.information(self, 'Image recieved!', 'The image has been recevied.')

	def directory(self):
		text, ok = QInputDialog.getText(self, 'Enter your desired directory', 'Please entire your desired directory:')
		if ok and text != '':
			text = 'DIR ' + text
			self.send_request_to_server(self.my_socket, str(text))
			popup = QtGui.QMessageBox.information(self, 'Contents:', str(self.my_socket.recv(1024)))

	def delete(self):
		text, ok = QInputDialog.getText(self, 'Enter your desired file', 'Please entire your desired file:')
		if ok and text != '':
			text = 'DELETE ' + text
			self.send_request_to_server(self.my_socket, str(text))
			popup = QtGui.QMessageBox.information(self, 'Deleted!', 'File has been deleted!')

	def copy(self):
		text1, ok1 = QInputDialog.getText(self, 'Enter your desired file', 'Please entire your desired file:')
		text2, ok2 = QInputDialog.getText(self, 'Enter your desired destination', 'Please entire your desired destination:')
		if ok1 and ok2 and text1 != '' and text2 != '':
			text = 'COPY ' + text1 + " " + text2
			self.send_request_to_server(self.my_socket, str(text))
			popup = QtGui.QMessageBox.information(self, 'Copied!', 'File has been copied!')

	def execute(self):
		text, ok = QInputDialog.getText(self, 'Enter your desired file', 'Please entire your desired file:')
		if ok and text != '':
			text = "EXECUTE " + text
			self.send_request_to_server(self.my_socket, str(text))
			popup = QtGui.QMessageBox.information(self, 'Executed!', 'File has been executed!')

	@staticmethod
	def send_request_to_server(my_socket, request):
		my_socket.send(request)

app = QtGui.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())
