import twosat

def read_input(filename):
    clauses = []
    variable_cnt = 0
    with open(filename) as f:
        first_line = f.readline().strip()
        variable_cnt = int(first_line)
        for line in f:
            x1, x2 = line.strip().split(' ')
            clauses.append((int(x1), int(x2)))
    return variable_cnt, clauses


def main(filename):
    variable_cnt, clauses = read_input(filename)
    print 'done reading input %s, %s' % (variable_cnt, len(clauses))
    #print twosat.backtrack(variable_cnt, clauses)
    print twosat.papadimitrious(variable_cnt, clauses)


import sys
if __name__ == '__main__':
    filename = sys.argv[1]
    main(filename)
