import re
from yargy.interpretation import fact
from yargy import rule, Parser, or_, not_, and_
from yargy.predicates import eq, type
from yargy.pipelines import morph_pipeline


class Pars:
    RULE = fact(
        'RULE',
        ['name', 'tresh', 'num']
    )
    INT = type('INT')
    PUNCT = type('PUNCT')

    DOT = or_(eq('.'), eq(','))

    NAME_mtbf = morph_pipeline(
        [
            'MTTF',
            'MTBF',
            'mean time between',
            'mean time between failures',
            'mean time between failure',
        ]
    ).interpretation(
        RULE.name
    )

    NAME_mttr = morph_pipeline(
        [
            'MTTR',
            'mean time to',
            'Mean Time To Repair',
            'repair time',
        ]
    ).interpretation(
        RULE.name
    )

    NUM_MTBF = or_(rule(INT, DOT, INT), rule(INT),
                   rule(INT, DOT, INT, DOT, INT),
                   rule(INT, INT), rule(INT, INT, INT))

    UNIT_mtbf = morph_pipeline(
        [
            'year',
            'years',
            'hour',
            'hours',
            'год',
            'час',
            'h',
            'ч',
            'тыс. часов'
        ]
    )

    UNIT_mttr = morph_pipeline(
        [
            'hour',
            'hours',
            'час',
            'h',
            'ч',
            'мин',
            'minutes',
            'minute',
            'минут'
        ]
    )

    def yargy_parser(self, path):
        x_mtbf = rule(self.NUM_MTBF, self.UNIT_mtbf.optional()
                      ).interpretation(
            self.RULE.num
        )

        x_mttr = rule(self.INT, self.UNIT_mttr.optional()
                      ).interpretation(
            self.RULE.num
        )

        tresh = rule(and_(not_(eq(self.NUM_MTBF)), or_(not_(eq(self.NAME_mttr)),
                                                       not_(eq(
                                                           self.NAME_mtbf))),
                          not_(eq(self.UNIT_mtbf)), not_(eq(self.DOT)),
                          not_(eq(self.INT)), not_(eq(x_mttr)),
                          not_(eq(x_mtbf)))
                     ).interpretation(
           self.RULE.tresh
        )

        rule_1 = (rule(self.NAME_mtbf, (tresh.optional()).repeatable(),
                       x_mtbf).repeatable()
                  ).interpretation(
            self.RULE
        )

        rule_2 = (rule(self.NAME_mttr, (tresh.optional()).repeatable(),
                       x_mttr).repeatable()
                  ).interpretation(
            self.RULE
        )

        f = open(path, 'r', encoding='utf-8')
        text = f.read()
        text = text.replace('|', ' ')
        # Remove line separators
        text = re.sub("^\s+|\n|\r|\s+$", '', text)
        line = text
        # Temporary workaround. Remove it as the performance grows
        n = 10000
        text = [
            line[i - 5 if i - 5 > 0 else 0:
                 i + n + 5 if i + n + 5 < len(line) else len(line) - 1]
            for i in range(0, len(line), n)]
        measure = rule(or_(x_mttr, x_mtbf, self.NAME_mttr, self.NAME_mtbf))
        new_line = []
        # Parser #1 text preprocessing
        parser = Parser(measure)
        for line in text:
            matches = list(parser.findall(line))
            spans = [list(_.span) for _ in matches]
            new_span = [0, 0]
            if spans != [] and len(spans) >= 2:
                mini = 1000000
                maxi = 0
                for i in range(0, len(spans) - 1, 1):
                    if spans[i][0] < mini:
                        new_span[0] = spans[i][0]
                        mini = spans[i][0]
                    if spans[i + 1][1] > maxi:
                        new_span[1] = spans[i + 1][1]
                        maxi = spans[i + 1][1]
                    for j in range(new_span[0], new_span[1]):
                        new_line.append(line[j])
                    new_line.append(' \n ')
        new_line = ''.join(new_line)
        new_line = new_line.split('\n')
        lst = []
        measure = or_(rule_1, rule_2).interpretation(
            self.RULE
        )
        # Parser #2 Parsing reliability metrics.
        parser = Parser(measure)
        for line in new_line:
            try:
                matches = list(parser.findall(line))
                spans = [_.span for _ in matches]
                if spans:
                    if matches:
                        for match in matches:
                            lst.append(match.fact)
            except:
                print(
                    'Yargy failure: you normally '
                    'don`t need to report that to us.')
        print(lst)
        return lst
