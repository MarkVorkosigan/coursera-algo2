def optimal_bts(freq_tuples):
    """Return an optimal binary search tree."""
    mat = []
    size = len(freq_tuples)
    for i in range(size):
        row = []
        mat.append(row)
        for j in range(size):
            row.append(0)

    for i in range(size):
        mat[i][i] = freq_tuples[i][1]

    for s in range(1, size):
        for i in range(size):
            # setting mat[i][i + s]
            right_bound = i + s
            if i + s >= size: continue
            min_p = 1000

            for r in range(i, right_bound + 1):
                if r > 0:
                    left_p = mat[i][r - 1]
                else:
                    left_p = 0

                if r + 1 <= right_bound:
                    right_p = mat[r + 1][right_bound]
                else:
                    right_p = 0
                this_p = left_p + right_p
                if this_p < min_p:
                    min_p = this_p
            sum_p = sum(freq for label, freq in freq_tuples[i:right_bound + 1])
            print 'setting mat[%s, %s]: min_p: %s, sum_p: %s' % (i, right_bound, min_p, sum_p)
            mat[i][right_bound] = sum_p + min_p
        print '-----size %s ------' % s
        for row in mat:
            for cell in row:
                print '%0.2f' % cell,
            print ''

def main():
    freq_tuples = [(1, 0.05),
                   (2, 0.4),
                   (3, 0.08),
                   (4, 0.04),
                   (5, 0.1),
                   (6, 0.1),
                   (7, 0.23)]
    assert(sum(freq for label, freq in freq_tuples) == 1)

    optimal_bts(freq_tuples)

    freq_tuples2= [(1, 0.2),
                   (2, 0.05),
                   (3, 0.17),
                   (4, 0.1),
                   (5, 0.2),
                   (6, 0.03),
                   (7, 0.25)]
    optimal_bts(freq_tuples2)

main()
        
