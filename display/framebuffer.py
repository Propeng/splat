import fcntl, os, config, struct, array, time, numpy, mmap

class Framebuffer:
	def __init__(self, devpath):
		self.devpath = devpath
		self.device = os.open(devpath, os.O_RDWR)
		#self.device = os.open(devpath, 'wb')
		self.mm = mmap.mmap(self.device, config.width*config.height*4)
		self.dirty = []
		self.width = config.width # until we can auto-detect the size of the framebuffer, a lazy width-height setting
		self.height = config.height
		self.memBuff = ''
		self.prevMemBuff = ''
		self.lastRender = time.time()
	def configure(self):
		#self.memBuff = [bytearray(config.width * 4)] * self.height
		#self.memBuff = numpy.repeat(bytearray(config.width * 4), self.height)
		self.memBuff = bytearray(config.width * config.height * 4)
		#for h in range(self.height):
		#	self.memBuff[h] = bytearray(config.width * 4)
		self.prevMemBuff = self.memBuff
		#self.memBuff = bytearray((config.width * config.height) * 4)
		#self.prevMemBuff = bytearray((config.width * config.height) * 4)
		#self.memBuff = [[[0, 0, 233]] * self.width] * self.height
		#self.prevMemBuff = [[[0, 0, 0]] * self.width] * self.height
		self.blankRaw = b'\x00\x00\x00\x00' * (self.width*self.height)
		self.blank = bytearray(config.width * config.height * 4)
		#self.device.seek(0)
		#self.device.write(self.blank * 2)
	def update(self):
		#print(len(self.memBuff[0]))
		framebuffers = []
		#print('determining changes...')
		isSim = False
		updatedChunks = 0
		#for yi,y in enumerate(self.memBuff):
		#self.memBuff[1279][0] = 255
		#print(self.memBuff[1279][0])
		#print(self.memBuff[0][0])
		if len(self.dirty) > -1:
			self.mm[0:self.width*self.height*4] = self.memBuff
			#self.device.seek(0)
			#self.device.write(self.memBuff)
		else:
			for yi in range(config.height):
				ypos = yi*self.width*4
				self.device.seek(ypos)
				self.device.write(self.memBuff[yi])
		distance = time.time() - self.lastRender
		self.lastRender = time.time()
		#print('FPS: %s' % str(1/distance))
			#print(ypos)
			#if y is not self.prevMemBuff[yi]:
			#	self.device.seek(ypos)
			#	self.device.write(y)
			#	updatedChunks += 1
		#print('done with that')
		#for y in range(self.height):
#			line = self.memBuff[y*4*self.width:y*4*self.width+self.width]
#			pLine = self.prevMemBuff[y*4*self.width:y*4*self.width+self.width]
#			if line is not pLine:
#				self.device.seek(y*4*self.width)
#				self.device.write(line)
		#self.prevMemBuff = self.memBuff
		#n = 0
		#while n < self.width * self.height:
		#	line = self.memBuff[n*4] 
		#	n += 1
		#for y,yl in enumerate(self.memBuff):
#			#print(y)
#			if self.memBuff[y] is not self.prevMemBuff[y]:
#				pixarray = b''
#				if config.pix_fmt == 'rgba':
#					for pixel in self.memBuff[y]:
#						#pixarray += array.array('B', pixel + [0]).tostring()
#						#pixarray += struct.pack('B', pixel[0]) + struct.pack('B', pixel[1]) + struct.pack('B', pixel[2]) + b"\x00"
#						#pixarray += b'\x55\x55\x55\x55'
#						pixarray += struct.pack('BBBB', pixel[0], pixel[1], pixel[2], 0)
#				self.device.seek(y*4*self.width)
#				self.device.write(pixarray)
				#framebuffers.append([y*4*self.width, pixarray])
			#for x,xl in enumerate(yl):
			#	if self.memBuff[y][x] is not self.prevMemBuff[y][x]:
			#		continue
					#if not isSim:
#						current[0] = (x*y)*4
#						isSim = True
#					if config.pix_fmt == 'rgba':
#						current[1] += struct.pack('B', xl[0]) + struct.pack('B', xl[1]) + struct.pack('B', xl[2]) + b"\x00"
#						#print(current[1])
#					else:
#						print("invalid pixel format - need to turn this into a fancy error later")
			#	elif isSim:
			#		print("boop")
			#		current[1] = str(current)
			#		framebuffers.append(current)
			#		isSim = False
			#		current = [0, '']
		#print(framebuffers)
		#print("printing changes")
		#for buff in framebuffers:
		#	#print(buff)
		#	self.device.seek(buff[0])
		#	self.device.write(buff[1])
		#	updatedChunks += 1
		#self.device.seek(self.width*self.height*4)
		#self.device.write(self.blankRaw)
		#self.device.seek(0)
		#print("Section updates in frame: %s" % str(updatedChunks))
		#self.prevMemBuff = self.memBuff
		#framebuffer = []
		#for pixel in updated:
		#	if pixel[0]
		#c = 0
		#while c < len(self.memBuff):
		#	pixel = self.memBuff[3]
		#	c += 3
		#for rect in self.dirty:
			#for pixelarray in self.memBuff[]:
	def reset(self):
		self.memBuff = self.blank[:]
	def rect(self, x=0, y=0, w=0, h=0, rgba=[0, 0, 0]):
		color = struct.pack('BBBB', rgba[0], rgba[1], rgba[2], 1)
		#self.memBuff[1][x*4:(x*4)+(w*4)] = color*w
		lineData = color*w
		for hx in range(h):
			#self.memBuff[y+hx][5*4:(5*4)+(5*4)] = color*5
			#line = self.memBuff[y+hx]
			line = (hx*config.width*4)+(y*config.width*4)
			self.memBuff[line+x*4:line+(x*4)+(w*4)] = lineData
		#print(1/(time.time()-ts))
			#print([x*4, (x*4)+(w*4)])
			#print(hx)
			#del self.memBuff[y+hx][x:x+w]
			#self.memBuff[y+hx][x:x+w] = color * self.width
		#for hx in range(h):
		#	yb = (4*hx*(self.width*4)*y)
			#print(yb)
		#	self.memBuff[yb:yb+w] = color * w
		#for hx in range(h):
			#yp = (hx * w) * 3
			#self.memBuff[y][x:x*w] = [rgba] * w
			#self.memBuff[yp:yp+(w*3)] = bytearray(w*3)
			#self.dirty.append([yp,yp+(w*3)])
			#for wx in range(w):
			#	xp = (yp + (x + wx * 3))
			#	print("Y: %s, X: %s" % (str(yp), str(xp)))