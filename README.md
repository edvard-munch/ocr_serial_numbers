Input a folder with photos of serial numbers of Axiomtec industrial PCs, recognize the text from the picture and then parse the serial number.
Replace initial picture name a correctly parsed serial number.

Example input:

![IMAGE435546899](https://github.com/edvard-munch/ocr_serial_numbers/assets/26732881/d1ce4e91-2c39-41a2-aaec-13747495f8ed)

Example output filename:

E234606301270003.jpg

Set `USE_GPU = True` if you have a videocard that supports technologies used by easyocr, else set `USE_GPU = False`
