"""This small tool copies the license text in the file defined in the
'license' variable below to the top of each file defined in the
'files' variable. The license is prepended by the comment character.

This script is meant to be called before packaging."""

import sys

def prependLicense(file, license):
    res = ''

    lin = open(license, 'r')
    for line in lin:
        res = '%s# %s' % (res, line)
    lin.close()
    res = '%s\n' % (res)

    fin = open(file, 'r')
    for line in fin:
        res = '%s%s' % (res, line)

    fin.close()
    return res

if __name__ == '__main__':
    files = ['geneagrapher/GGraph.py', 'geneagrapher/geneagrapher.py',
             'geneagrapher/grab.py', 'geneagrapher/ggrapher.py']
    license = 'COPYING'
    for file in files:
        res = prependLicense(file, license)
        fout = open(file, "w")
        fout.write(res)
        fout.close()
