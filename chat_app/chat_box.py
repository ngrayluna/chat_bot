#!bin/usr/python3

import os
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen



class ConnectPage(GridLayout):
	def __init__(self, **kwargs):
		# we want to run __init__ of both ConnectPage AAAAND GridLayout
		super().__init__(**kwargs)
		self.cols = 1

		## Inide Grid##
		self.inside = GridLayout()
		self.inside.cols = 2


		if os.path.isfile("prev_details.txt"):
			with open("prev_details.txt", "r") as f:
				d = f.read().split(",")
				prev_ip = d[0]
				prev_port = d[1]
				prev_username = d[2]

		else:
			prev_ip = ''
			prev_port = ''
			prev_username = ''


		# widgets added in order, so mind the order.
		self.inside.add_widget(Label(text='IP:'))  # widget #1, top left

		self.ip = TextInput(text=prev_ip, multiline=False)  # defining self.ip...
		self.inside.add_widget(self.ip) # widget #2, top right

		self.inside.add_widget(Label(text='Port:'))

		self.port = TextInput(text=prev_port, multiline=False)
		self.inside.add_widget(self.port)

		self.inside.add_widget(Label(text='Username:'))

		self.username = TextInput(text=prev_username,multiline=False)
		self.inside.add_widget(self.username)

		# Now back to main grid
		self.add_widget(self.inside)

		## BUTTON #
		# Creating a buttton is similar to making a txt box.
		# Simply declare a variable to hold our button and then
		# add that to the grid layout (w/ self.add_widget).
		self.submit = Button(text='Submit', font_size=40)
		# We are binding a button to a fn./method that we create so that
		# when the button is clicked, the fn. will run. 
		# pressed is the name of the fn./method we want to run
		self.submit.bind(on_press= self.pressed) 
		self.add_widget(self.submit)

	def pressed(self, instance):
		ip = self.ip.text
		port = self.port.text
		username = self.username.text

		# Let's save the details of the fields when someone clicks
		# the joing button
		with open("prev_details.txt", "w") as f:
			f.write("{}, {}, {}".format(ip, port, username))

		info = " Joining {}:{} as {}".format(ip, port, username)
		chat_app.info_page.update_info(info)
		chat_app.screen_manager.current = "Info"



class InfoPage(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		# Just one column
		self.cols = 1

		# And one label with bigger font and centered text
		self.message = Label(halign="center", valign="middle", font_size = 30)

		self.message.bind(width = self.update_text_width)

		# Add text widget to the layout
		self.add_widget(self.message)

	# Called with a message, to update message text in widget
	def update_info(self, message):
		self.message.text = message

	# Called on label width update, so we can set text width 
	# properly - to 90% of label width
	def update_text_width(self, *_):
		self.message.text_size = (self.message.width * 0.9, None)



class MyEpicApp(App):
	def build(self):
		self.screen_manager = ScreenManager()

		# Connect page
		# 1] create a page, 
		# 2] create new screen, 
		# 3] add page to screen 
		# 4] and then screen to screen manager
		self.connect_page = ConnectPage()
		screen = Screen(name='Connect')
		screen.add_widget(self.connect_page)
		self.screen_manager.add_widget(screen)

		# Info page
		self.info_page = InfoPage()
		screen = Screen(name='Info')
		screen.add_widget(self.info_page)
		self.screen_manager.add_widget(screen)

		return self.screen_manager


if __name__ == "__main__":
	chat_app = MyEpicApp()
	chat_app.run()
