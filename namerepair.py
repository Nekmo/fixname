#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Pasar nombres de archivos de codificaciones desconocidas al
   estandar UTF-8"""

CODECS = ['cp437', 'latin1', 'iso-8859-15']
LANGS = {
    'es': ['Á', 'É','Í', 'Ó', 'Ú', 'á', 'é',
           'í', 'ó', 'ú', 'ñ', 'Ñ', 'ü', 'Ü', '€',],
}
import sys
import os
import re
import argparse
import logging

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf8')
    input = raw_input

class File(object):
    valid_codecs = []
    def __init__(self, filename, lang='es'):
        self.lang = lang
         # Nombre incorrecto con el �
        self.bad_filename = os.path.split(filename)[-1]
        # Se usará el nombre incorrecto hasta que se tenga el "correcto"
        self.filename = os.path.split(filename)[-1]
        # Patrón regex para seleccionar el nombre
        self.pattern_filename = self.make_pattern(os.path.split(filename)[-1])
        # Directorio donde se encuentra el archivo
        directory = os.path.dirname(filename)
        if not directory: directory = '.' # Directorio actual
        self.directory = directory
        self.is_bad_encoding = self.get_status_encoding()
        if self.is_bad_encoding:
            self.valid_codecs = self.get_valid_codecs()
    def get_valid_codecs(self):
        valid_codecs_names = {} # "codec": "nombre con el códec"
        codecs_stats = [] # estadísticas para el codec
        valid_codecs = [] # códecs de mejor a peor estadísticas
        for codec in CODECS:
            try:
                # Si no es posible decodificar, fallará y pasará al siguiente
                valid_codecs_names[codec] = file.decode(codec)
            except:
                pass
        # Ordenar los codecs según el número de buenos resultados para el idioma
        for codec, filename in valid_codecs_names.items():
            stats = 0
            for char in filename:
                if char in LANGS[self.lang]: stats += 1
            codecs_stats.append((stats, codec))
        
        for codec_stats in sorted(codecs_stats, reverse=True):
            valid_codecs.append(codec_stats[1])
        return valid_codecs
        
    def make_pattern(self, filename):
        """Construir el patrón regex para la sección"""
        filename = (re.escape(filename))
        filename = filename.replace('\\�', '.')
        return filename
    def get_status_encoding(self):
        """Comprobar si la codificación es incorrecta"""
        # Comprobar, con el patrón Regex, cuál es el "nombre correcto" al
        # nombre incorrecto con el �
        files = os.listdir(self.directory)
        for file in files:
            try:
                if re.match(self.pattern_filename, file):
                    file.decode('utf-8')
            except UnicodeDecodeError:
                self.filename = file
                return True
        # No ha dado error con ninguno, así que o bien no existe el archivo,
        # o no tiene problemas de codificación.
        return False
    def decode(self, codec=False):
        if not codec: codec = self.valid_codecs[0]
        try:
            return self.filename.decode(codec)
        except:
            return False
    def rename(self, codec=False):
        if not codec: codec = self.valid_codecs[0]
        decode_name = self.decode(codec)
        if not decode_name: return False
        os.rename(
            os.path.join(self.directory, self.filename), # from
            os.path.join(self.directory, decode_name) # to
        )
        return True
    def __nonzero__(self):
        return self.is_bad_encoding

def recursive(files):
    recursive_files = []
    for file in files:
        for root, dirs, infiles in os.walk(file):
            for infile in infiles:
                recursive_files.append(os.path.join(root, infile))
        recursive_files.append(file)
    return recursive_files

def decode_files(files, codec=False):
    codecs = []
    for file in files:
        if not codec:
            file_codec = file.valid_codecs[0]
        else:
            file_codec = codec
        print("%13s   %s" % (file_codec.upper(), str(file.decode(codec))))
        codecs = list(set(codecs + file.valid_codecs))
    print(
        "¿Renombrar los archivos con los nombres anteriores? Pulse enter"\
        " para confirmar. Si desea usar un códec específico, escríbalo y "\
        "pulse enter. Le recomendamos los siguientes: %s" % ', '.join(codecs))
    resp = input('[Enter para aceptar] >> ')
    if not resp:
        renames = 0
        for file in files:
            if file.rename(codec): renames += 1
        print("Renombrados correctamente %i archivos." % renames)
    else:
        decode_files(files, resp)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-r', '--recursive', dest='recursive',
                    action='store_true',
                    help='Buscar también dentro de carpetas recursivamente.')
    parser.add_argument('-f', '--force', dest='force', action='store_true',
                    help='Forzar el renombrado sin preguntar.')
    parser.add_argument('-l', '--lang', dest='lang', default='es',
                    help='Idioma por defecto para estadísticas.')
    parser.add_argument('-i', '--interactive', dest='interactive',
                    action='store_true',
                    help='Confirmación individual por cada archivo.')
    parser.add_argument('files', nargs='+', help='Archivos a reparar')
    args = parser.parse_args()
    if args.recursive:
        args.files = recursive(args.files)
    args.files = set(args.files) # Eliminar repeticiones
    files = []
    for file in args.files:
        file = File(file)
        if file: files.append(file)
    if args.force:
        for file in files:
            print("%13s   %s" % (file_codec.upper(), str(file.decode(codec))))
            file.rename()
    elif args.interactive:
        for file in files:
            decode_files([file])
    else:
        decode_files(files)
    sys.exit(0)