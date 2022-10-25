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

        X_mtbf = rule(NUM_MTBF, UNIT_mtbf.optional()
                      ).interpretation(
            RULE.num
        )

        X_mttr = rule(INT, UNIT_mttr.optional()
                      ).interpretation(
            RULE.num
        )

        TRESH = rule(and_(not_(eq(NUM_MTBF)), or_(not_(eq(NAME_mttr)),
                                                  not_(eq(NAME_mtbf))),
                          not_(eq(UNIT_mtbf)), not_(eq(DOT)),
                          not_(eq(INT)), not_(eq(X_mttr)), not_(eq(X_mtbf)))
                     ).interpretation(
            RULE.tresh
        )

        rule_1 = (rule(NAME_mtbf, (TRESH.optional()).repeatable(),
                       X_mtbf).repeatable()
                  ).interpretation(
            RULE
        )

        rule_2 = (rule(NAME_mttr, (TRESH.optional()).repeatable(),
                       X_mttr).repeatable()
                  ).interpretation(
            RULE
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
            line[i - 5 if i - 5 > 0 else 0:i + n + 5 if i + n + 5 < len(line)
            else len(line) - 1] for i in range(0, len(line), n)]
        MEASURE = rule(or_(X_mttr, X_mtbf, NAME_mttr, NAME_mtbf))
        new_line = []
        # Parser #1 text preprocessing
        parser = Parser(MEASURE)
        for line in text:
            matches = list(parser.findall(line))
            spans = [list(_.span) for _ in matches]
            new_span = [0, 0]
            if spans != [] and len(spans) >= 2:
                for i in range(0, len(spans) - 1, 1):
                    mini = 1000000
                    maxi = 0
                    if spans[i][0] < mini:
                        new_span[0] = spans[i][0]
                        mini = spans[i][0]
                    if spans[i + 1][1] > maxi:
                        new_span[1] = spans[i + 1][1]
                        maxi = spans[i + 1][1]
                    for i in range(new_span[0], new_span[1]):
                        new_line.append(line[i])
                    new_line.append(' \n ')
        new_line = ''.join(new_line)
        new_line = new_line.split('\n')
        LIST = []
        MEASURE = or_(rule_1, rule_2).interpretation(
            RULE
        )
        # Parser #2 Parsing reliability metrics.
        parser = Parser(MEASURE)
        for line in new_line:
            try:
                matches = list(parser.findall(line))
                spans = [_.span for _ in matches]
                if spans != []:
                    if matches:
                        for match in matches:
                            LIST.append(match.fact)
            except:
                print(
                    'Yargy failure: you normally don`t need to report that to us.')
        print(LIST)
        f.close()
        return LIST
