"""This tool sets up a distribution of the software by automating
several tasks that need to be done.

The directory should be in pristine condition when this is run (i.e.,
devoid of files that need to be removed before packaging begins). It
is best to run this on a fresh check out of the repository."""

import os
import licensify

if __name__ == '__main__':
    # "Licensify" the source files.
    files = ['geneagrapher/GGraph.py', 'geneagrapher/geneagrapher.py',
             'geneagrapher/grab.py', 'geneagrapher/ggrapher.py']
    license = 'COPYING'
    for file in files:
        res = licensify.prependLicense(file, license)
        fout = open(file, "w")
        fout.write(res)
        fout.close()

    # Remove files (including this one) that are not to be in the
    # distribution.
    os.system('svn rm licensify.py')
    os.system('rm -f licensify.pyc')
    os.system('svn rm makedist.py')
    os.system('rm -f makedist.pyc')

    # Make the distribution.
    os.system('python setup.py sdist --format gztar,zip')

    # Compute digests and signatures.
    os.chdir('dist')
    dirl = os.listdir('.')
    for file in dirl:
        comm = 'sha1sum %s > %s.sha1' % (file, file)
        os.system(comm)

        comm = 'gpg -abs %s' % (file)
        os.system(comm)
    os.chdir('..')

    # Add files to repository.
    os.system('svn add Geneagrapher.egg-info')
    os.system('svn add dist')
