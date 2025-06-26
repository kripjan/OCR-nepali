a simple code to detect letters and characters in english and nepali using easyocr 
here it is tested in number plates

reader = easyocr.Reader(['en'], gpu=True) for english
reader = easyocr.Reader(['ne'], gpu=True) for nepali

you can pull/fork this repo and the just : pip install -r requirements.txt 

and run the .py file
