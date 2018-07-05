import sys
from pstl.ast.Lists import AQ_Checkboxes
PY3 = sys.version_info[0] == 3

if PY3:
	xrange = range

import numpy as np
import cv2 as cv

import PIL
from wand.image import Image
import os
import io

class AutoCorrector(object):
	def __init__(self, *args, **kwargs):
		self.teacher_copie_path = 'input.rst' #correction_copie_path
		self.copie_to_correct_path = 'AutoQCM.pdf' #input_path
		self.correct_answers = []
		self.student_answers = []
		self.nb_correct_answers = 0
		self.nb_question = 0
		self.page_images = convertPdf(self.copie_to_correct_path)
		self.findCheckboxes()
		with open(self.teacher_copie_path, 'r') as rst_file:
			code = rst_file.read()

		# This is the scary part that you don't need to worry about.

		inputStream = InputStream(code)
		l = AutoQcmLexer(inputStream)
		tokenStream = CommonTokenStream(l)
		p = AutoQcmParser(tokenStream)
		p._errHandler = BailErrorStrategy()
		p._interp.predictionMode = PredictionMode.SLL
		cst = p.document()

	
		#print_ast(cst)
		ast = Visitor().visitDocument(cst)
		for child in ast.children:
			if isinstance(child, AQ_Checkboxes):
				for item in child.items:
					if item.isChecked:
						self.correct_answers.append(1)
						self.nb_question +=1
					else:
						self.correct_answers.append(0)
		for i in range(0, len(self.correct_answers)):
			if self.correct_answers[i] == self.student_answers[i]:
				self.nb_correct_answers += 1
		print(str(self.nb_correct_answers)+'/'+str(self.nb_question))


	def findCheckboxes(self):
		from glob import glob
		for im in self.page_images:
			for fn in glob(im):
				img = cv.imread(fn)
				squares = find_squares(img)
				#print(squares)
				for s in squares:
					(x, y, w, h) = s
					if isChecked(img, x+2, y+2, w-2):
						cv.rectangle(img,(x+1,y+1),(x+w-2,y+h-2),(0,255,0),1)
						self.student_answers.append(1)
					else:
						cv.rectangle(img,(x+1,y+1),(x+w-2,y+h-2),(0,0,255),1)
						self.student_answers.append(0)
					#cv.drawContours( img, squares, -1, (0, 255, 0), 1 )

				cv.imshow('squares', img)
				#cv.imwrite('Exam-3-1-squares.png', img)
				ch = cv.waitKey()
				if ch == 27:
					break
			cv.destroyAllWindows()







def angle_cos(p0, p1, p2):
	d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
	return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
	img = cv.GaussianBlur(img, (9, 9), 0)
	squares = []
	for gray in cv.split(img):
		for thrs in xrange(0, 255, 26):
			if thrs == 0:
				bin = cv.Canny(gray, 0, 50, apertureSize=5)
				bin = cv.dilate(bin, None)
			else:
				_retval, bin = cv.threshold(gray, thrs, 255, cv.THRESH_BINARY)
			bin, contours, _hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
			for cnt in contours:
				cnt_len = cv.arcLength(cnt, True)
				cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
				if len(cnt) == 4 and cv.contourArea(cnt) > 500 and cv.contourArea(cnt) < 650 and cv.isContourConvex(cnt):
					(x, y, w, h) = cv.boundingRect(cnt)
					ar = w / float(h)
					rect = cv.minAreaRect(cnt)
					box = cv.boxPoints(rect)
					box = np.int0(box)
					#cnt = cnt.reshape(-1, 2)
					#max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
					#if max_cos < 0.1:
					if ar >= 0.95 and ar <= 1.05:
						squares.append((x, y, w, h))
						area = cv.contourArea(cnt)
	return squares

def isChecked(image, x, y, size, ratio=0.5):
	copy_img = cv.cvtColor(image.copy(), cv.COLOR_RGB2GRAY)
	black_pixels = 0
	white_pixels = 0
	px = image[x,y]
	for i in range(y, y+size):
		for j in range(x, x+size):
			if  np.all(image[i,j]==255):
				continue
			else:
				black_pixels +=1
	r = black_pixels / (size * size)
	return r >= ratio

def convertPdf(pdf_file):
	filepath = "fill this in"
	assert os.path.exists(pdf_file)
	with Image(filename=pdf_file, resolution=200) as img:
		page_images = []
		for page_wand_image_seq in img.sequence:
			page_wand_image = Image(page_wand_image_seq)
			page_jpeg_bytes = page_wand_image.make_blob(format="jpeg")
			page_jpeg_data = io.BytesIO(page_jpeg_bytes)
			page_image = PIL.Image.open(page_jpeg_data)
			page_images.append(page_image)
	return page_images



if __name__=='__main__':
	AutoCorrector()