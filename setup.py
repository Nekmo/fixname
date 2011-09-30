#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Nekmo Software 2011 ( contacto [at] nekmo.com ) - Licencia: GPLv3 
# 
# Envíe sus sugerencias y reportes a: https://bitbucket.org/Nekmo/fixname
#
##

from distutils.core import setup
import sys

VERSION = '1.0'
DESCRIPTION = 'Reparar nombres de fichero incorrectos (con carácter "�"),'\
              'para poder trabajar con ellos.'

LONG_DESCRIPTION = """
Este renombrador de archivos le permite, de manera sencilla, renombrar
aquellos archivos que tienen caracteres extraños (del tipo "�") que impiden
trabajar con ellos. 
"""

CLASSIFIERS = [
    'Topic :: System :: Filesystems',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: System Administrators',
]

packages = []

scripts = ['fixname']

setup(
    name = "fixname",
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    author = 'Nekmo',
    author_email = 'contacto [at] nekmo.com',
    url = 'http://nekmo.com',
    license = 'GPLv3',
    platforms = ['any',],
    packages = packages,
    requires = ['argparse'],
    scripts = scripts
)