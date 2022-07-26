class MathCore:
    @staticmethod
    def calculate_param(dict_max):
        try:
            dict_max['Failure rate'] = 1 / dict_max['MTBF']
        except:
            dict_max['Failure rate'] = 0
        dict_max['failure rate in storage mode'] = dict_max[
                                                       'Failure rate'] * 0.01
        try:
            dict_max['Storage time'] = round(
                1 / (dict_max['failure rate in storage mode'] * 8760), 3)
        except:
            dict_max['Storage time'] = 0
        dict_max['Minimal resource'] = round(0.01 * dict_max['MTBF'], 3)
        dict_max['Gamma percentage resource'] = round(
            0.051239 * dict_max['MTBF'], 3)
        dict_max['Average resource'] = round(0.6931 * dict_max['MTBF'], 3)
        dict_max['Average lifetime'] = round(
            dict_max['Average resource'] / 8760, 3)
        try:
            dict_max['recovery intensity'] = 1 / dict_max['MTTR']
        except:
            dict_max['recovery intensity'] = 0
        try:
            if dict_max['MTBF'] != 0 and dict_max['MTTR'] != 0:
                dict_max['System Reliability'] = dict_max['MTBF'] / (
                            dict_max['MTBF'] + dict_max['MTTR'])
            else:
                dict_max['System Reliability'] = 0
        except:
            dict_max['System Reliability'] = 0
        return dict_max
