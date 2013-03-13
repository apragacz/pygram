import re


class GrammarStatement(object):

    def is_leaf(self):
        raise NotImplementedError

    def is_token(self):
        raise NotImplementedError


class AtomStatement(GrammarStatement):

    def is_leaf(self):
        return True


class StringStatement(AtomStatement):

    def __init__(self, string):
        assert(string[0] == '"')
        assert(string[-1] == '"')
        self.string = string[1:-1].replace('\\"', '"')

    def is_token(self):
        return True

    def get_token_regex_string(self):
        return re.escape(self.string)


class IdentStatement(AtomStatement):

    def __init__(self, ident):
        self.ident = ident

    def is_token(self):
        return False


class SpecialStatement(AtomStatement):

    def __init__(self, special):
        self.special = special[1:-1]

    def is_token(self):
        return False


class ComplexStatement(GrammarStatement):

    def __init__(self, statement_list):
        try:
            self.statement_list = list(statement_list)
        except TypeError:
            self.statement_list = [statement_list]

    def is_leaf(self):
        return False

    def is_token(self):
        return False

    def get_children(self):
        return self.statement_list

    def appended(self, sub_statement):
        l = self.statement_list[:]
        l.append(sub_statement)
        return self.__class__(l)


class RuleBodyStatement(ComplexStatement):

    def is_token(self):
        return all([s.is_token() for s in self.statement_list])

    def get_children_regexps(self):
        return [s.get_token_regex_string() for s in self.statement_list]


class AlternativeStatement(RuleBodyStatement):

    def get_token_regex_string(self):
        return '(%s)' % '|'.join(self.get_children_regexps())


class RepetitionStatement(RuleBodyStatement):

    def get_token_regex_string(self):
        return '(%s*)' % ''.join(self.get_children_regexps())


class OptionStatement(RuleBodyStatement):

    def get_token_regex_string(self):
        return '(%s?)' % ''.join(self.get_children_regexps())


class RuleStatement(ComplexStatement):
    pass


class SpecificationStatement(ComplexStatement):
    pass
