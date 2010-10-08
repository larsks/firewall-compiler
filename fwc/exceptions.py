class FirewallError (Exception):
    pass

class SyntaxError(FirewallError):
    def __init__ (self, file=None, line=None):
        super(SyntaxError, self).__init__()
        self.file = file
        self.line = line

    def __str__ (self):
        return 'Syntax error in %s: %s' % (self.file, self.line)


