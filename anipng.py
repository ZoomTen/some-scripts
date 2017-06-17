#!/bin/python3

# anipng 1.0

# DESCRIPTION:
# Splits Windows animated icon frames into png files

# DEPENDENCIES:
# python3
# wand (python module)
# imagemagick

import sys
from wand.image import Image

if len(sys.argv) < 3:
	print("Usage: anipng.py [filename] [output, without extension]")
	
else:
	fname = sys.argv[1]
	oname = sys.argv[2]

	source = open(fname, "rb")
	contents = source.read()
	source.seek(0)
		
	instances = -1
	offsets = []
	
	while True:
		instances = contents.find(b'icon', instances+1)
		offsets.append(instances)
		
		if instances == -1:
			break
				
	source.seek(0)
	
	for i in range(0, len(offsets)-1):
		source.seek(offsets[i]+4)
		copi = ((int.from_bytes(source.read(4),byteorder='little'))) # Number of bytes to copy
		
		f_oname = oname + "_" + str(i) +".png"
		
		data = source.read(copi)	# Copy x bytes to this variable
		
		img = Image(format='ico',blob=data)
		
		with img.convert('png') as converted:
			converted.save(filename=f_oname)
			
		print("Converted frame %d in address %s to %s" % (i,hex(offsets[i]),f_oname))
	

	source.close()