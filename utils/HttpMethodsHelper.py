import requests


class HttpMethodHelper:
    @staticmethod
    def get_link_content(link):
        try:
            return requests.get(link, timeout=5).content
        except (requests.exceptions.SSLError, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, requests.exceptions.ContentDecodingError):
            return ""

    @staticmethod
    def get_link_content_type(link):
        try:
            return requests.get(link, timeout=5).headers.get("Content-Type", "").lower()
        except (requests.exceptions.SSLError, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, requests.exceptions.ContentDecodingError):
            return ""

    @staticmethod
    def get_link_content_encoding(link):
        try:
            return requests.get(link, timeout=5).encoding
        except (requests.exceptions.SSLError, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, requests.exceptions.ContentDecodingError):
            return ""
