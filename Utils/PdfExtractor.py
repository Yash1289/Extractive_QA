from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io


def PdfExtractor(pdfPath):

    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdfPath, 'rb') as fh:

        for page in PDFPage.get_pages(fh,
                                  caching=True,
                                  check_extractable=True):
            page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    paras = text.split("\n\n")
    para_list = [para for para in paras if len(para) >20]
    return para_list