import olefile, sys

class PCBLibrary(object):
	def __init__(self, filename):
		self.ole = olefile.OleFileIO(filename)

		fh = self.ole.openstream("FileHeader")
		self.header = fh.read().split(b"|")
		fh.close()

		self.parts = {}

		parts = self.ole.listdir(streams = True, storages = False)
		for part in parts:
			if part[0] not in ["FileHeader", "Storage", "SectionKeys"]:
				stream = self.ole.openstream(part)
				data = stream.read()
				stream.close()
				self.parts[part[0]] = SchematicPart(part[0], data)

	def diff(self, other):
		added = set(self.parts) - set(other.parts)
		removed = set(other.parts) - set(self.parts)
		changed = {}
		common = set(self.parts) - added - removed

		for name in common:
			this_part = self.parts[name]
			that_part = other.parts[name]
			if this_part != that_part:
				changes = []

				#Figure out what's different
				differences = set(this_part.properties.items()) ^ set(that_part.properties.items())
				properties = {name for name, prop in differences}

				for prop in properties:
					if prop in this_part.properties.keys() and prop in that_part.properties.keys():
						changes.append("changed %s: %s -> %s" % (prop, this_part.properties[prop], that_part.properties[prop]))
					elif prop in this_part.properties.keys():
						changes.append("removed %s" % (prop))
					else:
						changes.append("added %s: %s" % (prop, that_part.properties[prop]))

				changed[name] = changes


		return added, removed, changed

class SchematicLibrary(object):
	def __init__(self, filename):
		self.ole = olefile.OleFileIO(filename)

		fh = self.ole.openstream("FileHeader")
		self.header = fh.read().split(b"|")
		fh.close()

		self.parts = {}

		parts = self.ole.listdir(streams = True, storages = False)
		for part in parts:
			if part[0] not in ["FileHeader", "Storage", "SectionKeys"]:
				stream = self.ole.openstream(part)
				data = stream.read()
				stream.close()
				self.parts[part[0]] = SchematicPart(part[0], data)

	def diff(self, other):
		added = set(self.parts) - set(other.parts)
		removed = set(other.parts) - set(self.parts)
		changed = {}
		common = set(self.parts) - added - removed

		for name in common:
			this_part = self.parts[name]
			that_part = other.parts[name]
			if this_part != that_part:
				changes = []

				#Figure out what's different
				differences = set(this_part.properties.items()) ^ set(that_part.properties.items())
				properties = {name for name, prop in differences}

				for prop in properties:
					if prop in this_part.properties.keys() and prop in that_part.properties.keys():
						changes.append("changed %s: %s -> %s" % (prop, this_part.properties[prop], that_part.properties[prop]))
					elif prop in this_part.properties.keys():
						changes.append("removed %s" % (prop))
					else:
						changes.append("added %s: %s" % (prop, that_part.properties[prop]))

				changed[name] = changes


		return added, removed, changed

class SchematicPart(object):
	def __init__(self, name, binary):
		self.name = name
		self.properties = {}

		for prop in binary.split(b"|"):
			if b"=" in prop:
				try:
					key = prop.split(b"=")[0].decode()
				except:
					key = prop.split(b"=")[0]

				try:
					value = prop.split(b"=")[1].decode()
				except:
					value = prop.split(b"=")[1]
				self.properties[key] = value

		self.hash = hash((self.name, frozenset(self.properties.items())))

	def __hash__(self):
		return self.hash

	def __eq__(self, other):
		return hash(self) == hash(other)

	def __ne__(self, other):
		return hash(self) != hash(other)

	def __str__(self):
		return self.name

def parse(filename):
	ole = olefile.OleFileIO(filename)

	#Figure out what kind of file it is
	if ole.exists("FileHeader"):
		header = ole.openstream("FileHeader")
		contents = header.read()
		header.close()
		if b"Schematic Library" in contents:
			return SchematicLibrary(filename)
		elif b"PCB" in contents and b"Binary Library" in contents:
			return PCBLibrary(filename)
	
	return None

try:
	old_file = sys.argv[1]
	new_file = sys.argv[2]
except:
	print("Two files required.")
	sys.exit(1)

old_lib = parse(old_file)
new_lib = parse(new_file)
added, removed, changed = new_lib.diff(old_lib)

print("Added:")
for part in added:
	print("\t", part)

print("Removed:")
for part in removed:
	print("\t", removed)

print("Changed:")
for part in changed:
	print("\t",part)
	print("\t\t", "\n\t\t".join(changed[part]))

