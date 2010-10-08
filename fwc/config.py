import optparse
from configdict.configdict import ConfigDict

class attrdict (dict):
    
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise None

    def __getitem__(self, k):
        try:
            v = super(attrdict, self).__getitem__(k)

            try:
                return v % self
            except TypeError:
                return v
        except KeyError:
            return None

config = attrdict(
    fwdir           = '/etc/firewall',
    template        = '%(fwdir)s/master.tmpl',
    rules_active    = '%(fwdir)s/rules.enabled',
    rules_inactive  = '%(fwdir)s/rules.d',
)

class Config (object):

    def __init__ (self):
        super(Config, self).__init__()

        self.config = config

        self.parser = optparse.OptionParser()
        self.parser.add_option('-f', '--config')
        self.parser.add_option('-d', '--fwdir')
        self.parser.add_option('-t', '--template')

    def add_option(self, *args, **kwargs):
        self.parser.add_option(*args, **kwargs)

    def parse_args(self, *args, **kwargs):
        opts, args = self.parser.parse_args(*args, **kwargs)

        if opts.config:
            self.update(opts.config)

        for k,v in opts.__dict__.items():
            if v is not None:
                self.config[k] = v
            elif not k in self.config:
                self.config[k] = None

        return config, args

    def update(self, path):
        cfg = ConfigDict(path)
        if 'fwc' in cfg:
            for k,v in cfg['fwc'].items():
                self.config[k] = v

if __name__ == '__main__':
    import pprint

    cfg = Config()
    cfg.add_option('-D', '--dump', action='store_true')
    opts, args = cfg.parse_args()

    pprint.pprint(opts)

