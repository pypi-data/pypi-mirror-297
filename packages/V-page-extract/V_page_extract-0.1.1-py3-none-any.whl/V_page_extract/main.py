from PyPDF2 import PdfReader, PdfWriter
def extract_pages(source_pdf_path, output_pdf_path, start_page, end_page):
   
    reader = PdfReader(source_pdf_path)
    
    writer = PdfWriter()

   
    for page_num in range(start_page - 1, end_page):  
        try:
            writer.add_page(reader.pages[page_num])
        except IndexError:
            print(f"Page {page_num + 1} is out of range.")
            break

    
    with open(output_pdf_path, 'wb') as f:
        writer.write(f)

    