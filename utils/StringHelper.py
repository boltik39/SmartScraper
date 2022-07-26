from random import randint
from statistics import mean
from collections import Counter
import itertools
from utils.MathCore import MathCore
from utils.DoITrust import DoITrust


class StringHelper:

    @staticmethod
    def get_random_path(ext):
        """Generates random number with txt extention"""
        path = str(randint(0, 100000)) + "." + ext
        return path

    @staticmethod
    def strip_num(string):
        """There are several options for input numbers
        '1,123,234 year/hours', '1123234.5 year/hours', '1123234.5'
        '1 123 234 year/hours', '1 123 234'
        """
        # At first we replace ',' to '' and split string for grabbing the number
        src_list = string.replace(',', '').split(' ')
        # TODO: avoid try-except
        try:
            # Here we grab the number when possible.
            # This is possible when the number is without a unit
            number = int(float(''.join(src_list)))
        except:
            try:
                # Delete the unit so only num remains
                del src_list[-1]
                number = int(float(''.join(src_list)))
            except:
                print(src_list)
                print('Error convert')
                number = 0
        return number

    @staticmethod
    def to_hours(string):
        """ Converts stuff like '13 years' or '13 тыс. часов' into hours """
        result = 0
        if ('years' in string
                or 'year' in string
                or 'год' in string):
            try:
                num = float(string.split(' ')[0])
                num = num * 8760
                result = int(round(num))
            except:
                print('Error with float')
        # TODO: apply all possible cases
        elif 'тыс. часов' in string:
            try:
                num = float(string.split(' ')[0])
                num = num * 1000
                result = int(round(num))
            except:
                print('Error with float')
        elif ('minute' in string
              or 'мин' in string):
            try:
                num = float(string.split(' ')[0])
                result = num / 60
            except:
                print('Error with float')
        else:
            result = StringHelper.strip_num(string)
        return result

    @staticmethod
    def finding_num(parsed, query):
        # MTTF is listed as a synonym to MBTF as their difference is
        # more about recovery than about the time. They are almost
        # identical then it comes to calculating probabilities
        names_mtbf = ['mtbf', 'mttf',
                      'mean time between',
                      'mean time between failures',
                      'mean time between failure', ]
        names_mttr = ['mttr',
                      'mean time to',
                      'mean time to repair',
                      'mean time to repairs',
                      'repair time']
        dict_num = {'MTTR': [], 'MTBF': []}
        dict_links = {'MTTR': {}, 'MTBF': {}}
        dict_max = {'MTTR': 0, 'MTBF': 0, 'Links': []}
        score_max = 0
        for link in parsed:
            for item in parsed[link]:
                # Unify titles
                if item.name.lower() in names_mtbf:
                    item.name = 'MTBF'
                elif item.name.lower() in names_mttr:
                    item.name = 'MTTR'
                item.num = StringHelper.to_hours(item.num)
                # TODO: fix multiline recognition.
                # Temporary workaround
                if item.name == 'MTTR' and item.num > 20:
                    item.num = item.num / 60
                dict_num[item.name].append(item.num)
                if item.num in dict_links[item.name]:
                    if link not in dict_links[item.name][item.num]:
                        dict_links[item.name][item.num].append(link)
                else:
                    dict_links[item.name][item.num] = [link]
        # Set maximum delta (%)
        max_delta = 5
        for param_name in dict_num:
            values = dict_num[param_name]
            counted_values = dict(Counter(values))
            # Join close and equal values
            deleted = []
            for first_value, second_value in itertools.permutations(
                    counted_values.keys(), 2):
                if first_value in deleted or second_value in deleted:
                    continue
                delta = 100 * abs(first_value - second_value) / mean(
                    [first_value, second_value])
                # If the difference is less than delta and values are not equal
                # Keep in mind we are iterating the same dict twice
                if delta < max_delta:
                    to_keep = 0
                    to_replace = 0
                    if counted_values[first_value] >= \
                            counted_values[second_value]:
                        to_keep = first_value
                        to_replace = second_value
                    else:
                        to_keep = second_value
                        to_replace = first_value
                    deleted.append(to_replace)
                    # Recount
                    counted_values[to_keep] += counted_values[to_replace]
                    del counted_values[to_replace]
                    # Merge links
                    if dict_links[param_name][to_keep] != \
                            dict_links[param_name][to_replace]:
                        dict_links[param_name][to_keep] += \
                            dict_links[param_name][to_replace]
                    del dict_links[param_name][to_replace]
            # Default values
            amount_res = 0
            value_res = 0
            links_res = []
            # Drop insane values and find the most popular one
            for num in counted_values:
                if ((param_name == 'MTTR' and 0 < num < 100) or
                        (param_name == 'MTBF' and num > 50000)):
                    if counted_values[num] > amount_res:
                        amount_res = counted_values[num]
                        value_res = num
                        links_res = dict_links[param_name][value_res]
            dict_max[param_name] = value_res
            for link in links_res:
                if link not in dict_max['Links']:
                    dict_max['Links'].append(link)
            # Amount_res can be greater than amount of links
            # as the same value can be providen twice on
            # the same resource. Thus, we use amount_res
            cur_score = DoITrust.score(links_res, amount_res, query)
            # Divide cur_score by params
            score_max += cur_score / len(dict_num)
        dict_max = MathCore.calculate_param(dict_max)
        dict_max['score'] = int(score_max)
        print(dict_max)
        return dict_max
