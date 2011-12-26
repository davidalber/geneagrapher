import urllib2

if __name__ == '__main__':
    record_ids = [7298, 7383, 10275, 12681, 15165, 17851, 17946, 18230, 18231,
                  18232, 18233, 18603, 19953, 19964, 28292, 29458, 29642,
                  30484, 36991, 47064, 51261, 51907, 52965, 52996, 53658,
                  55175, 62547, 79297, 79562, 79568, 84016, 89841, 99457,
                  127470, 127946, 137705, 137717, 143630, 151876, 999999999,
                  79568583832]

    for record_id in record_ids:
        url = 'http://genealogy.math.ndsu.nodak.edu/id.php?id='+str(record_id)
        print 'Getting record {}'.format(record_id)
        page = urllib2.urlopen(url)
        with open('{}.html'.format(record_id), 'w') as fout:
            fout.write(page.read())
