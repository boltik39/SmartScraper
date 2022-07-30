import os

from utils.StringHelper import StringHelper
from utils.HttpMethodsHelper import HttpMethodHelper
from bs4 import BeautifulSoup
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


class FileHelper:
    @staticmethod
    def transform_link_content_to_txt(link):
        path_to_file = StringHelper.get_random_path("txt")
        with open(path_to_file, "w", encoding='utf-8') as file:
            if 'html' in HttpMethodHelper.get_link_content_type(link):
                if 'charset' in HttpMethodHelper.get_link_content_type(link):
                    encoding = HttpMethodHelper.get_link_content_encoding(link)
                else:
                    encoding = None
                parser = 'html.parser'
                soup = BeautifulSoup(HttpMethodHelper.get_link_content(link),
                                     parser,
                                     from_encoding=encoding)
                file.write(soup.getText())
            elif 'pdf' in HttpMethodHelper.get_link_content_type(link):
                path_to_pdf = StringHelper.get_random_path("pdf")
                with open(path_to_pdf, "wb") as f:
                    f.write(HttpMethodHelper.get_link_content(link))
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(resource_manager,
                                              fake_file_handle)
                    page_interpreter = PDFPageInterpreter(resource_manager,
                                                          converter)

                    with open(path_to_pdf, 'rb') as fh:
                        for page in PDFPage.get_pages(fh,
                                                      caching=True,
                                                      check_extractable=False):
                            page_interpreter.process_page(page)

                        text = fake_file_handle.getvalue()

                    # close open handles
                    converter.close()
                    fake_file_handle.close()

                    if text:
                        file.write(text)
                os.remove(path_to_pdf)
        return path_to_file
