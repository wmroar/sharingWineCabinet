# coding: utf-8

import json
import operator

allop = {
	'==' : lambda x, y: x and y and operator.eq(x, y),
	'!=' : lambda x, y: x and y and operator.ne(x, y),
	'<' : lambda x, y: x and y and operator.lt(x, y),
	'>' : lambda x, y: x and y and operator.gt(x, y),
	'<=' : lambda x, y: x and y and operator.le(x, y),
	'>=' : lambda x, y: x and y and operator.ge(x, y),
	'': lambda x, y: True
}

class VarMap:
	allvar = {'a': 11, 'b': 11}

	@classmethod
	def set(self, k, v):
		self.allvar[k] = v

	@classmethod
	def get(self, k):
		return self.allvar.get(k)



classtype = {
}

class Index:
	index = 0

	@classmethod
	def get(self):
		self.index += 1
		return self.index
	@classmethod
	def update(self, id):
		self.index = max(self.index,  id)
		return self.index

class Task:
	def __init__(self, name):
		self.name = name
		self.id = Index.get()
		self.parent = None
		self.childs = []
		self.changeop = {
		    'args1' : 0,
			'args2' : 1
		}
####################
	def child(self, row):
		return self.childs[row]

	def childCount(self):
		return len(self.childs)

	def columnCount(self):
		return 1

	def data(self, column):
		if column == 0:
			return '%s:%s(%s)' % (self.id, self.__class__.__name__,  self.name)
		else:
			return None

	def getparent(self):
		return self.parent

	def row(self):
		if self.parent:
			return self.parent.childs.index(self)
		return 0


	def insertChildren(self, position,  columns):
		if position < 0:
			position = 0
		elif position > len(self.childs):
			position = len(self.childs)

		print 'insertChildren',  position,  self.todict()
		for item in columns:
			self.childs.insert(position, item)
			item.setparent(self)
		print 'insertChildren11',  position,  self.todict()
		return True

	def removeChildren(self, position, count):
		if position < 0 or position + count > len(self.childs):
			return False

		for row in range(count):
			self.childs.pop(position)

		return True


####################

	def getclsname(self):
		return self.__class__.__name__

	@classmethod
	def getclassname(self, clsname):
		return classtype.get(clsname)


	def buildtreechild(self, data):
		childsdata = data.get('childs')
		for c in childsdata:
			clsname = c.get('clsname')
			if clsname:
				cls = self.getclassname(clsname)
				if cls:
					tmp = cls('')
					tmp.buildtree(c)
					self.add_child(tmp)

	def buildtree(self, data):
		self.name = data.get('name')
		self.id = data.get('id')
		self.changeop.update(data.get('changeop',  {}))

		Index.update(self.id + 1)
		self.buildtreechild(data)

	def todict(self, withchilds=True):
		ret = {
			'clsname': self.__class__.__name__,
			'name' : self.name,
			'id': self.id,
			'changeop': self.changeop
		}
		if withchilds:
			ret['childs'] = [x.todict() for x in self.childs]
		return ret

	def tolist(self):
		tmp = {}
		tmp[self.id] = self
		for x in self.childs:
			tmp.update(x.tolist())
		return tmp

	def setparent(self, p):
		self.parent = p

	def add_child(self, c):
		self.childs.append(c)
		c.setparent(self)

	def gethstr(self):
		cut = 0
		parent = self.parent
		while parent:
			parent = parent.parent
			cut += 1
		return ' ' * cut * 4


	def nextcldid(self, c):
		if isinstance(self, Select):
			if self.parent:
				return self.parent.nextcldid(self)
		else:
			i = self.childs.index(c)
			if 0 <= i < len(self.childs) - 1:
				return self.childs[i + 1].id
			elif i == len(self.childs) - 1:
				if self.parent:
					return self.parent.nextcldid(self)
				else:
					return -1
			else:
				return -1

	def nextid(self, selectid = 0):
		if isinstance(self, Select):
			return self.childs[selectid].id
		if isinstance(self, Return):
			return -1

		if len(self.childs) > 0:
			return self.childs[0].id
		else:
			if self.parent:
				return self.parent.nextcldid(self)
			else:
				return -1

	def run(self):
		strh = self.gethstr()
		print '%s run_task_begin:%s' % (strh, self.name)
		for c in self.childs:
			c.run()
		print '%s run_task_end:%s' % (strh, self.name)

	def getchangeop(self):
		return self.changeop

	def setchangeop(self,  changeop):
		self.changeop =  changeop


class SelectItem(Task):
	def __init__(self, name, lable=''):
		Task.__init__(self, name)
		self.lable = lable

	def buildtree(self, data):
		self.lable = data.get('lable')
		Task.buildtree(self,  data)

	def todict(self, withchilds=True):
		ret = Task.todict(self, withchilds)
		ret['lable'] = self.lable
		return ret

	def run(self):
		strh = self.gethstr()
		print '%s run_begin:%s' % (strh, self.name)

		for c in self.childs:
			c.run()

		print '%s run_end:%s' % (strh, self.name)


class Select(Task):
	def add_child(self, c):
		assert isinstance(c, SelectItem)
		self.childs.append(c)
		c.setparent(self)


	def todict(self, withchilds=True):
		ret = Task.todict(self, withchilds)
		if not withchilds:
			ret['lables'] = [x.lable for x in self.childs]
		return ret


	def run(self):
		strh = self.gethstr()
		print '%s run_begin:%s' % (strh, self.name)

		name = self.getinput()

		if name:
			for c in self.childs:
				if name == c.lable:
					c.run()

		print '%s run_end:%s' % (strh, self.name)

	def getinput(self):
		tmpl = [c.lable for c in self.childs]
		tmp = zip(list(range(len(tmpl))), tmpl)

		tip = '\n'.join(['%d:%s' % (x[0], x[1]) for x in tmp])
		tip = 'input id:\n' + tip + '\n'
		id = int(raw_input(tip))
		if 0 <= id < len(tmpl):
			return tmpl[id]
		return None

class Cond(Task):
	def __init__(self, name, nameop = '', name1 = '', name2 = ''):
		Task.__init__(self, name)
		self.name1 = name1
		self.name2 = name2
		self.nameop = nameop


	def buildtree(self, data):
		self.name1 = data.get('name1')
		self.name2 = data.get('name2')
		self.nameop = data.get('nameop')
		Task.buildtree(self,  data)


	def todict(self, withchilds=True):
		ret = Task.todict(self, withchilds)
		ret['name1'] = self.name1
		ret['name2'] = self.name2
		ret['nameop'] = self.nameop
		return ret

	def run(self):
		strh = self.gethstr()
		print '%s run_begin:%s' % (strh, self.name)
		v1 = VarMap.get(self.name1)
		v2 = VarMap.get(self.name2)
		op = allop.get(self.nameop)
		ret = op and op(v1, v2)
		if ret:
			for c in self.childs:
				c.run()
		print '%s run_end:%s' % (strh, self.name)

class Loop(Task):
	def __init__(self, name, count = -1):
		Task.__init__(self, name)
		self.count = count
		self.breakflag = False


	def buildtree(self, data):
		self.count = data.get('count')
		Task.buildtree(self,  data)

	def todict(self, withchilds=True):
		ret = Task.todict(self, withchilds)
		ret['count'] = self.count
		return ret

	def run(self):
		strh = self.gethstr()
		print '%s run_loop_begin:%s' % (strh, self.name)
		if self.count < 0:
			while not self.breakflag:
				for c in self.childs:
					c.run()
		else:
			count = self.count
			while not self.breakflag and count > 0:
				for c in self.childs:
					c.run()
				count -= 1
		print '%s run_loop_end:%s' % (strh, self.name)

	def setbreak(self):
		self.breakflag = True


class Break(Task):
	def __init__(self, name, count = 1):
		Task.__init__(self, name)
		self.count = count


	def buildtree(self, data):
		self.count = data.get('count')
		Task.buildtree(self,  data)

	def todict(self, withchilds=True):
		ret = Task.todict(self, withchilds)
		ret['count'] = self.count
		return ret

	def run(self):
		strh = self.gethstr()
		print '%s run_begin:%s' % (strh, self.name)

		parent = self
		isok = True
		for i in range(self.count):
			while True:
				parent = parent.parent
				if parent or isinstance(self.parent, Loop):
					break
			if not parent:
				isok = False
				break
		if isok:
			parent.setbreak()

		print '%s run_end:%s' % (strh, self.name)

class Return(Task):
	pass

class CodeItem(Task):
	def __init__(self, name):
		Task.__init__(self, name)
		self.codedata = {
				'bkimg': '',
				'fontimg':{'img1':{'img':'',  'mirroring':False},  'img2': {'img':'',  'mirroring':False},  'img3':{'img':'',  'mirroring':False}},
				'txt':'tttttttttttttttttttt'
		}

		self.changeop = {
			'arg1': 0,
			'arg2': 0,
			'arg3': 0,
			'arg4':0
		}
	def buildtree(self, data):
		Task.buildtree(self, data)
		self.codedata = data.get('codedata')

	def todict(self, withchilds=True):
		ret = Task.todict(self, withchilds)
		ret['codedata'] = self.codedata
		return ret

	def getcodedata(self):
		return self.codedata

	def input(self):
		print 'aaaaaaaaa'
		msg =  yield
		print 'input',  msg

	def run(self):
		strh = self.gethstr()
		print '%s run_CodeItem_begin:%s' % (strh, self.name)
		self.show(self)
		self.input()
		print '%s run_CodeItem_end:%s' % (strh, self.name)

	def show(self,  item):
		pass

class CodeSelect(Select):
	def __init__(self, name):
		Select.__init__(self, name)
		self.codedata = {
				'bkimg': '',
				'fontimg':{'img1':{'img':'',  'mirroring':False},  'img2':{'img':'',  'mirroring':False},  'img3':{'img':'',  'mirroring':False}},
				'txt':'tttttttttttttttttttt'
		}
		self.changeop = {
			'arg1': 0,
			'arg2': 0,
			'arg3': 0,
			'arg4': 0,
			'arg5': 0
		}
	def buildtree(self, data):
		Select.buildtree(self, data)
		self.codedata = data.get('codedata')

	def todict(self, withchilds=True):
		ret = Select.todict(self, withchilds)
		ret['codedata'] = self.codedata
		return ret


	def getcodedata(self):
		return self.codedata

	def input(self,  *args):
		print args

	def run(self):
		print self.codedata
		self.show(self)

	def show(self,  item):
		pass

classtype = {
	'Task': Task,
	'SelectItem': SelectItem,
	'Select': Select,
	'Cond': Cond,
	'Loop': Loop,
	'Break': Break,
	'CodeItem': CodeItem,
	'CodeSelect':   CodeSelect,
	'Return': Return
}


if __name__ == '__main__':

	a = Task('all')

	tmp = [Task('aaa'), Task('ccc'), Task('bbb')]
	for t in tmp:
		a.add_child(t)


	c = Cond('c1', '!=', 'a', 'b')
	tmp = [Task('aaa1'), Task('ccc1'), Task('bbb1')]
	for t in tmp:
		c.add_child(t)

	a.add_child(c)


	l = Loop('l1', 10)
	tmp = [Task('llll')]
	for t in tmp:
		l.add_child(t)

	a.add_child(l)

	x = CodeItem('aaaaaaa')
	print 'aaaaaaa',  x.todict()
	a.add_child(x)
	a.run()

	fp = open('out.txt', 'w')
	fp.write(json.dumps(a.todict()))
	fp.close()



	tmp = json.dumps(a.todict())
	tmp = json.loads(tmp)
	aa = Task('')


	aa.buildtree(tmp)

	print a.todict()
	print aa.todict()

	aa.run()
