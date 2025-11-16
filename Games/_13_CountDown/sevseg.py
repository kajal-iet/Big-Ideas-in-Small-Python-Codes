"""SevSeg, by Al Sweigart al@inventwithpython.com
A seven-segment number display module, used by several of the
games in this book. More info at https://en.wikipedia.org/wiki/Seven-segment_display
View this code at https://nostarch.com/big-book-small-python-projects
Tags: short, artistic, module"""

def getSevSegStr(number, minWidth=0):
    """Return a seven-segment display string of number. The returned
    string will be padded with spaces if it is smaller than minWidth."""

    number = str(number).zfill(minWidth)

    rows = ['', '', '']
    for i, numeral in enumerate(number):
        if numeral == '.':  # Render the decimal point:
            rows[0] += ' '
            rows[1] += ' '
            rows[2] += '.'
            continue  # Skip the other numeral segments for this iteration.

        # Each digit is rendered using a 3x3 grid of characters.
        if numeral == '0':
            segs = (' _ ',
                    '| |',
                    '|_|')
        elif numeral == '1':
            segs = ('   ',
                    '  |',
                    '  |')
        elif numeral == '2':
            segs = (' _ ',
                    ' _|',
                    '|_ ')
        elif numeral == '3':
            segs = (' _ ',
                    ' _|',
                    ' _|')
        elif numeral == '4':
            segs = ('   ',
                    '|_|',
                    '  |')
        elif numeral == '5':
            segs = (' _ ',
                    '|_ ',
                    ' _|')
        elif numeral == '6':
            segs = (' _ ',
                    '|_ ',
                    '|_|')
        elif numeral == '7':
            segs = (' _ ',
                    '  |',
                    '  |')
        elif numeral == '8':
            segs = (' _ ',
                    '|_|',
                    '|_|')
        elif numeral == '9':
            segs = (' _ ',
                    '|_|',
                    ' _|')
        elif numeral == '-':
            segs = ('   ',
                    ' _ ',
                    '   ')
        else:
            raise ValueError(f'Invalid numeral: {numeral}')

        # Add the appropriate sections to each row.
        rows[0] += segs[0] + ' '
        rows[1] += segs[1] + ' '
        rows[2] += segs[2] + ' '

    return '\n'.join(rows)
