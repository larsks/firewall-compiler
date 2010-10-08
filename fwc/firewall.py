import os
import re
import logging
import optparse
import logging

from exceptions import *

re_begin_table=re.compile('^\*(?P<table>.*)')
re_add_rule=re.compile('^-A (?P<chain>\S+) (?P<rule>[^#]*)\s*(#\s*(?P<comment>.*))?')
re_end_table=re.compile('^COMMIT$')
re_comment=re.compile('^#.*')
re_define_chain=re.compile('^:(?P<chain>\S+) (?P<policy>\S+) \[(?P<in>\d+):(?P<out>\d+)\]')

class Firewall (object):
    def __init__ (self, config):
        self.config = config
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

    def read_rules (self):
        for rfile in sorted(os.listdir(self.config.rules_active)):
            # ignore dotfiles.
            if rfile.startswith('.'):
                continue

            # only read *.rules files.
            if not rfile.endswith('.rules'):
                continue

            # handle explicit exclusions via -x command line option.
            if os.path.splitext(rfile)[0] in self.config.exclude:
                self.log.info('excluding %s' % rfile)
                continue

            self.log.info('Reading %s' % rfile)
            self.update(os.path.join(self.config.rules_active, rfile))

    def enable_ruleset(self, ruleset):
        if not ruleset.endswith('.rules'):
            ruleset = '%s.rules' % ruleset

        spath = os.path.join(self.config.rules_inactive, ruleset)
        dpath = os.path.join(self.config.rules_active, ruleset)

        if os.path.exists(dpath):
            self.log.info('ruleset %s is already active.' % ruleset)
        else:
            os.symlink(os.path.abspath(spath), dpath)
            self.log.info('activated ruleset %s.' % ruleset)

    def disable_ruleset(self, ruleset):
        if not ruleset.endswith('.rules'):
            ruleset = '%s.rules' % ruleset

        spath = os.path.join(self.config.rules_inactive, ruleset)
        dpath = os.path.join(self.config.rules_active, ruleset)

        if os.path.exists(dpath):
            os.unlink(dpath)
            self.log.info('deactivated ruleset %s.' % ruleset)
        else:
            self.log.info('ruleset %s is not active.' % ruleset)

def configure_logging(opts):
    if opts.debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
            level=level,
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(name)s [%(levelname)s]: %(message)s')

