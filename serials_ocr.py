from datetime import datetime

import os
import re

import easyocr
import pytesseract


USE_GPU = False
PYTESSERACT_LANGUAGE = 'eng'
EASYOCR_LANGUAGES = ['en', 'ru']
EASYOCR_OUTPUT_DETAILIZATION = 0
FOLDER = 'input'
IMAGE_EXTENSIONS = ('.png', '.jpg')
SERIAL_NUMBER_REGEX =  r"E[0-9]{15,}"

NOT_RECOGNIZED_BY_PYTESSERACT = 'Serial number not recognized via pytesseract\nUsing easyocr now'
NOT_RECOGNIZED_BY_EASYOCR = 'Serial number not recognized via easyocr\nProceeding with the next file now'
TIME_TAKEN_MESSAGE = 'Time: '

NEW_FILENAME = 'clean_serials/{}.jpg'
FILENAME_SUFFIX = '_'
TXT_FILENAME = 'pics/{}.txt'


def iterate_files():
	for file in os.scandir(FOLDER):
		if file.name.endswith(IMAGE_EXTENSIONS):
			print(file.name)
			start_ocr(file)
		else:
			continue


def start_ocr(file):
	image = f"{FOLDER}/{file.name}"
	match = use_tesseract(image, PYTESSERACT_LANGUAGE)

	if match:
		print(match[0])
		rename_file(file, match)
	else:
		print(NOT_RECOGNIZED_BY_PYTESSERACT)
		match = use_easyocr(image)

		if match:
			print(match[0])
			rename_file(file, match)

		else:
			print(NOT_RECOGNIZED_BY_EASYOCR)


def rename_file(file, match):
	try:
		os.rename(file, NEW_FILENAME.format(match[0]))
	except FileExistsError:
		os.rename(file, NEW_FILENAME.format(match[0]) + SUFFIX)


def write_full_ocr_output_to_txt(file, ocr_output):
	with open(TXT_FILENAME.format(file.name), "w") as f:
		f.write(ocr_output)


def use_easyocr(image):
	start = datetime.now()
	result = reader.readtext(image, detail=EASYOCR_OUTPUT_DETAILIZATION)
	end = datetime.now()
	time_taken = end - start
	print(TIME_TAKEN_MESSAGE, time_taken)

	return [match[0] for res in result if (match := re.search(SERIAL_NUMBER_REGEX, res))]


def use_tesseract(image, lang):
	start = datetime.now()
	text = pytesseract.image_to_string(image, lang=lang)
	end = datetime.now()
	time_taken = end - start
	print(TIME_TAKEN_MESSAGE, time_taken)
	match = re.search(SERIAL_NUMBER_REGEX, text)
	
	return match


if __name__ == '__main__':
	reader = easyocr.Reader(EASYOCR_LANGUAGES, gpu=USE_GPU)
	iterate_files()
