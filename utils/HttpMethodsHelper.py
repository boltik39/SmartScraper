import requests


class HttpMethodHelper:
    @staticmethod
    def get_link_content(link):
        try:
            return requests.get(link).content
        except requests.exceptions.SSLError:
            return ""

    @staticmethod
    def get_link_content_type(link):
        try:
            return requests.get(link).headers.get("Content-Type", "").lower()
        except requests.exceptions.SSLError:
            return ""

    @staticmethod
    def get_link_content_encoding(link):
        try:
            return requests.get(link).encoding
        except requests.exceptions.SSLError:
            return ""
