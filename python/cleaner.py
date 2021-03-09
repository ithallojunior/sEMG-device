"""
Cleans the files that come from the acquisitions with a NI device.
Dots must not be in the filepath, except for the extension.
Spaces are used as delimiters.
Author: Ithallo Junior Alves Guimaraes
"""

from sys import argv


def cleaner(filepath, delimiter=' '):
    """
    Cleans data from an NI device to a format readable by numpy.
    It uses spaces as delimiters.
    """

    with open(filepath, 'r') as f:
        lines = f.readlines()[1:]  # ignoring the header

    new_lines = ''
    for line in lines:

        line = line.replace(',', '.')  # data uses commas for decimals
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        line = line.replace('\t', delimiter)
        line = line.replace(';', delimiter)

        if 'm' in line:
            split_line = line.split(delimiter)
            voltage = str(float(split_line[1][:-1])/1000.)
            line = ('%s' % delimiter).join([split_line[0], voltage])

            new_lines += (line + '\n')

    split_filepath = filepath.split('.')
    new_filepath = split_filepath[0] + '_cleaned.txt'

    with open(new_filepath, 'w') as f:
        f.write(new_lines)


if __name__ == '__main__':

    try:
        filepath = argv[1]
        cleaner(filepath)
    except (IndexError, IOError):
        raise Exception('You must pass a valid filepath as argument')

