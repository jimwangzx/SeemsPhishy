from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage
import requests
import unicodedata
import re
import os

class TextParser:

    def __init__(self, files):
        self.files = files #{header-title : url}
        self.text = {}


    def convertFiles(self, filenumber):
        counter = 0
        #download pdfs and parse text
        for key in self.files:
            if counter < int(filenumber):
                #self.downloadPDF(self.files[key], key)
                try:
                    self.downloadPDF(self.files[key], key)
                except:
                    counter = counter +1
                    print("Exception")
                counter = counter +1
            else:
                print("Skipped")
            
        return self.text
    
    def textParser(self, pdf_path, filename):
        
        #Teil 1 (Extrahieren des Textes aus der Datei)
        resource_manager = PDFResourceManager(caching=True)
        out_text = StringIO()
        codec = 'utf-8'
        laParams = LAParams()
        text_converter = TextConverter(resource_manager, out_text, laparams=laParams)
        fp = open(pdf_path, 'rb')
        interpreter = PDFPageInterpreter(resource_manager, text_converter)

        for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, caching=True, check_extractable=False):
            interpreter.process_page(page)

        text = out_text.getvalue()
        fp.close()
        text_converter.close()
        out_text.close()

        text = text.replace("'","")
        text = text.replace('"','')

        self.text[filename] = text
        
        #Teil 2 (Erstellen einer .txt Datei und speichern des Textes aus Teil 1)
        #file = open(name_txt_file + '.txt', "w", encoding = "utf-8")
        #file.write(text)
        #file.close()
        
    def slugify(value, allow_unicode=False):
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '-', value).strip('-_')
    
    def downloadPDF(self, url_name, filename):
        full_filename = filename
        filename = filename[:25].replace(" ","_")
        slugified = self.slugify(filename)
        filepath = f"src/SeemsPhishy/dataretrieval/lib/PDF/{slugified}.pdf"
        response = requests.get(url_name)
        print(filename)
        print(slugified)
        file = open(filepath, "wb")
        file.write(response.content)
        file.close()
        #conver2text
        self.textParser(filepath, full_filename)
        os.remove(filepath)