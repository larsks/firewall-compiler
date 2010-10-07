import re
import logging

re_begin_table=re.compile('^\*(?P<table>.*)')
re_add_rule=re.compile('^-A (?P<chain>\S+) (?P<rule>[^#]*)\s*(#\s*(?P<comment>.*))?')
re_end_table=re.compile('^COMMIT$')
re_comment=re.compile('^#.*')
re_define_chain=re.compile('^:(?P<chain>\S+) (?P<policy>\S+) \[(?P<in>\d+):(?P<out>\d+)\]')

class SyntaxError(Exception):
    def __init__ (self, file=None, line=None):
        super(SyntaxError, self).__init__()
        self.file = file
        self.line = line

    def __str__ (self):
        return 'Syntax error in %s: %s' % (self.file, self.line)

class Firewall (object):
    def __init__ (self):
        self.log = logging.getLogger('fwc.firewall')
        self.statemap = {
            0:  [
                (re_begin_table, self.p_start_table),
                (re_comment, self.p_comment),
                ],

            1: [
                (re_define_chain, self.p_define_chain),
                (re_add_rule, self.p_add_rule),
                (re_end_table, self.p_end_table),
                (re_comment, self.p_comment),
                ]
        }

        self.rules = {}
        self.chains = {}

    def p_define_chain(self, mo, line):
        self.chains[mo.group('chain')] = mo.group('policy')

    def p_start_table(self, mo, line):
        table = mo.group('table')
        self.log.debug('start table: %s' % table)

        self.ctx['table'] = table
        if not table in self.rules:
            self.rules[table] = {}
        self.ctx['state'] = 1

    def p_comment(self, mo, line):
        pass

    def p_add_rule(self, mo,line):
        table = self.ctx['table']
        chain = mo.group('chain')

        if not chain in self.rules[table]:
            self.rules[table][chain] = []

        rule = mo.group('rule')
        self.log.debug('table=%s, chain=%s, rule=%s' % (table, chain,
            rule))
        if mo.group('comment'):
            rule += ' -m comment --comment "%s"' % mo.group('comment')

        self.rules[table][chain].append(rule)

    def p_end_table(self, mo, line):
        table = self.ctx['table']
        self.log.debug('finished table: %s' % table)
        self.ctx['state'] = 0

    def update(self, rfile):
        self.ctx = {'state': 0}

        for line in open(rfile):
            line = line.strip()
            if not line:
                continue

            handled=False
            for re, handler in self.statemap[self.ctx['state']]:
                mo = re.match(line)
                if mo:
                    handler(mo, line)
                    handled=True
                    break

            if not handled:
                raise SyntaxError(file=rfile, line=line)


