import requests


class HttpMethodHelper:
    @staticmethod
    def get_link_content(link):
        return requests.get(link).content

    @staticmethod
    def get_link_content_type(link):
        return requests.get(link).headers.get("Content-Type", "").lower()

    @staticmethod
    def get_link_content_encoding(link):
        return requests.get(link).encoding
