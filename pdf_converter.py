

import pdfkit
import os
# Sample data
def make_html_pdf(out_file = "my",html_content =None,main_path = "pdfs"):
    
   
    try:
        options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
    }
        pdfkit.from_string(html_content,f"{main_path}/{out_file}.pdf", options=options)
    except Exception as e:
        options = {
        'no-images': None,  # Add this option to disable loading of images
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
                        }
        pdfkit.from_string(html_content,f"{main_path}/{out_file}.pdf", options=options)
    # with open(f"htmls/{out_file}-temp.html", "w",encoding="utf-8" ) as file:
    #     file.write(html_content)
    print(f"{main_path}/{out_file}.pdf","  created")
  












    