
def _combine(f1, f2):
    label1 = f1[1]
    label2 = f2[1]
    if not isinstance(label1, tuple):
        label1 = (label1, )
    if not isinstance(label2, tuple):
        label2 = (label2, )

    return (f1[0] + f2[0], # frequency
            label1 + label2, # label
            ['0' + s for s in f1[2]] + [ '1' + s for s in f2[2]]) # encodings
 
def huffman(freqs):
    """Retrun a tree of huffman encoding.

    Args:
        freq: list of tuples of (freq, label, encodings)
    Returns:
        Tree of the encoding
    """
    def inner(freq):
        if len(freq) ==1:
            return freq

        freq_sorted = sorted(freq)
   
        return inner([_combine(freq_sorted[0], freq_sorted[1])] + freq_sorted[2:])

    result = inner(freqs)[0]

    letters = result[1]
    encodings = result[2]
    return dict((c, e) for c, e in zip(letters, encodings))

def huffman2(freq):
    """better algorithm, implemented with queue."""
    def pick2(q1, q2):
        q = q1[:2] + q2[:2]
        return tuple(sorted(q)[:2])

    def removeFrom(e, q1, q2):
        if e in q1[:2]:
            q1.remove(e)
        elif e in q2[:2]:
            q2.remove(e)
        else:
            raise Exception('%s Not in both %s, %s' % (e, q1, q2))

    queue1 = sorted(freq)
    queue2 = []

    while len(queue1) + len(queue2) > 1:
        n1, n2 = pick2(queue1, queue2)
        removeFrom(n1, queue1, queue2)
        removeFrom(n2, queue1, queue2)
        new_node = _combine(n1, n2)
        queue2.append(new_node)

    if len(queue1) > 0:
        result = queue1[0]
    else:
        result = queue2[0]

    letters = result[1]
    encodings = result[2]
    assert len(letters) == len(freq)
    assert len(encodings) == len(freq)
    return dict((c, e) for c, e in zip(letters, encodings))

sample1 = ((0.6, 'A1', ['']),
           (0.25, 'B2',['']),
           (0.1, 'C3', ['']),
           (0.05, 'D4', ['']))
        
def main():

    print huffman(sample1)
    print huffman2(sample1)

    print huffman(((0.28, 'A', ['']),
                  (0.27, 'B', ['']),
                  (0.2, 'C', ['']),
                  (0.15, 'D', ['']),
                  (0.1, 'E', [''])))

def build_test_case():
    import random
    import itertools
    import string

    n_of_letters = random.randint(5, 600)
    letters = itertools.product(string.ascii_uppercase, range(1,200))
    
    freq = []
    for l in list(letters)[:n_of_letters]:
        freq.append((random.randint(1, 50), str(l[0]) + str(l[1]), ['']))
    return freq

def total_weight(encoding, freq):
    sum = 0
    for weight, letter, _ in freq:
        sum += weight*len(encoding[letter])
    return sum

def test():

    testcases = [sample1]
    testcases.append(build_test_case())
    for _ in range(2000):
        testcases.append(build_test_case())

    for i, c in enumerate(testcases):
        print 'test case %s of length %s' % (i, len(c))
        e1 = huffman(c)
        e2 = huffman2(c)
        assert len(e1) == len(c)
        assert len(e2) == len(c)
        assert total_weight(e1, c) == total_weight(e2, c) 
        #assert e1 == e2, '%s \n %s \n %s' % (len(c), e1, e2)
        assert len(c) == len(e1) == len(e2)



if __name__ == '__main__':
    main()
    #test()
    
    
