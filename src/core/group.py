from abc import ABC, abstractmethod
from enum import Enum

from sortedcontainers import SortedList, SortedKeyList, SortedDict, SortedSet

class GroupBase(ABC):
	_instances = 0
	def __init__(self, name=None):
		self.name = name or f"Anonymous group ({GroupBase._instances})"
		GroupBase._instances += 1
		self.callbacks = {'add':[], 'remove':[], 'clear':[],
			'register':[], 'unregister':[]}

	def add(self, *kargs):
		for arg in kargs:
			self._trigger_callbacks('add', arg)
		return self

	def remove(self, *kargs):
		for arg in kargs:
			self._trigger_callbacks('remove', arg)
		return self

	def clear(self):
		self._trigger_callbacks('clear')

	@abstractmethod
	def contains(self, element):
		pass

	def register(self, action, *callbacks):
		if action not in self.callbacks:
			self.callbacks[action] = []
		for cb in callbacks:
			if cb not in self.callbacks[action]:
				self.callbacks[action].append(cb)
				self._trigger_callbacks('register', cb)
		return self

	def unregister(self, action, *callbacks):
		if action not in self.callbacks:
			return self
		for cb in callbacks:
			if cb in self.callbacks[action]:
				self.callbacks[action].remove(cb)
				self._trigger_callbacks('unregister', cb)
		return self

	def _trigger_callbacks(self, action, *kargs):
		if action not in self.callbacks:
			return self
		for cb in self.callbacks[action]:
			cb(*kargs)
		return self

	@abstractmethod
	def contains(self, element):
		pass

	@abstractmethod
	def __len__(self):
		pass

	@abstractmethod
	def __iter__(self):
		pass

	def __repr__(self):
		return self.name or "Unknown"


class Group(GroupBase):
	_counter = 0
	def __init__(self, name=None, ordered=False):
		if name is None:
			name = f"Anonymous Group ({Group._counter})"
			Group._counter += 1
		self.ordered = ordered
		self.elements = [] if ordered else set()
		super().__init__(name)

	def add(self, *elements):
		if self.ordered:
			for element in elements:
				if not self.contains(element):
					self.elements.append(element)
					super().add(element)
		else:
			for element in elements:
				if not self.contains(element):
					self.elements.add(element)
					self._trigger_callbacks('add', element)
					super().add(element)
		return self
	def remove(self, *elements):
		if self.ordered:
			for element in elements:
				if self.contains(element):
					self.elements.remove(element)
					super().remove(element)
		else:
			for element in elements:
				if self.contains(element):
					self.elements.discard(element)
					super().remove(element)
		return self
	def contains(self, element):
		return element in self.elements
	def clear(self):
		self.elements = [] if self.ordered else set()
		super().clear()
		return self
	def __iter__(self):
		return iter(self.elements)
	def __len__(self):
		return len(self.elements)
	def __repr__(self):
		return self.name or "Unknown"

class CatGroup(GroupBase):
	_instances = 0
	def __init__(self, name=None, categorizer=None):
		if name is None:
			name = f"Anonymous CatGroup ({CatGroup._instances})"
			CatGroup._instances += 1
		super().__init__(name)
		self.categorizer = categorizer or (lambda x: f"{type(x).__name__}")
		self.categories = {}
		self.num = 0
	def add(self, *elements):
		for element in elements:
			cat = self.categorizer(element)
			if cat not in self.categories:
				self.categories[cat] = Group(name=cat)
			self.categories[cat].add(element)
			self.num += 1
			super().add(element)
		return self
	def get_category(self, cat):
		return self.categories.get(cat, None)
	def remove(self, *elements):
		for element in elements:
			cat = self.categorizer(element)
			if cat in self.categories:
				self.categories[cat].remove(element)
			if len(self.categories[cat]) == 0:
				del self.categories[category]
			self.num -= 1
			super().remove(element)
		return self
	def contains(self, element):
		return element in self.categories
	def __iter__(self):
		return iter(self.categories)
	def __len__(self):
		return self.num
	def __repr__(self):
		return self.name or "Unknown"

def accesser(i):
	return lambda x: x[i]

class SortedGroup(Group):
	_instances = 0
	def __init__(self, name=None, keyfn = accesser(0)):
		if name is None:
			name = f"Anonymous SortedGroup ({SortedGroup._instances})"
			SortedGroup._instances += 1
		super().__init__(name)
		self.elements = SortedKeyList(key=keyfn)
		self.keyfn = keyfn
	def add(self, *elements):
		for element in elements:
			if element not in self.elements:
				self.elements.add(element)
				super().add(element)
		return self
	def remove(self, *elements):
		for element in elements:
			if element in self.elements:
				self.elements.discard(element)
				super().remove(element)
		return self
	def clear(self):
		self.elements = SortedKeyList(self.keyfn)
		super().clear()
	def contains(self, element):
		return element in self.elements
	def __iter__(self):
		return iter(self.elements)
	def __len__(self):
		return len(self.elements)
	def __repr__(self):
		return self.name or "Unknown"
