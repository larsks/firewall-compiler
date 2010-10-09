import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='firewall-compiler',
        version=read('VERSION'),
        description='Generate an iptables firewall from modules.',
        long_description=read('README.rst'),
        author='Lars Kellogg-Stedman',
        author_email='lars@seas.harvard.edu',
        packages=['fwc'],
        scripts=['bin/fwc', 'bin/fwc-tool', 'bin/fwc-activate'],
        )

