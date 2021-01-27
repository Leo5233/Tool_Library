import pytesseract
from PIL import Image
a = Image.open("../static/assember.jpg")
a = a.convert('L')

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
ans = pytesseract.image_to_string(a)
# 有各式各樣的空白要清除\n=chr(10) 
# \r=chr(13)回車:新增一行但游標不移到下一行  
# chr(12)換頁(在python等於結束這次執行並清除紀錄)
ans = "".join([i for i in ans if i.isalpha() or i.isdigit()])
print(ans)
