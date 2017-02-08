import sys

class Base:
	x = None
	y = None

	def __init__(self):
		self.x = 5

	def hook(self):
		print("lol")

class Derived(Base):

	def __init__(self):
		Base.__init__(self)
		self.x = 6
		self.y = 1

	def call(self):
		Base.hook(self)

base = Base()
der = Derived()
der.call()
