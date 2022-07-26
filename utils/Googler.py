from googlesearch import search
from utils.FileHelper import FileHelper
from utils.Parser import Pars
import os
from utils.StringHelper import StringHelper


class Googler:
    @staticmethod
    def google(query):
        """Searches the query in Google
        Requires "Googler" command-line tool
        Returns list of URLS
        """
        lst = []
        for url in search(query, stop=20):
            if url.startswith("http"):
                lst.append(url)
        lst = list(filter(None, [s.strip() for s in lst]))
        return lst

    @staticmethod
    def search_by_query(query: str):
        links = Googler.google(query + ' mtbf')
        fnd = dict()
        for link in links:
            file_path = FileHelper.transform_link_content_to_txt(link)
            fnd[link] = Pars().yargy_parser(file_path)
            os.remove(file_path)
        res = StringHelper.finding_num(fnd, query)
        res['query'] = query

        # patch column names
        res = Googler._patch_dict_keys(res)

        # if all props == 0, skip saving in DB
        if res['mttr'] == 0 and res['mtbf'] == 0:
            print("Nothing to save")
            return res

        res['links'] = links
        return res

    @staticmethod
    def _patch_dict_keys(dict_):
        for k, v in dict_.copy().items():
            new_k = '_'.join(k.lower().split())
            dict_[new_k] = dict_.pop(k)
        return dict_
