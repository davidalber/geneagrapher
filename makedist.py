"""This tool sets up a distribution of the software by automating
several tasks that need to be done."""

import os

if __name__ == '__main__':
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
