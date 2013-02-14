import tsp
import math

def read_input(filename):
    cities = []
    city_cnt = 0, 0
    with open(filename) as f:
        first_line = f.readline().strip()
        city_cnt = int(first_line)
        for line in f:
            x_cord, y_cord = line.strip().split(' ')
            cities.append((float(x_cord), float(y_cord)))

    g = {}
    for i in range(city_cnt):
        node_i = i + 1
        g[node_i] = {}
        for j in range(city_cnt):
            node_j = j + 1
            g[node_i][node_j] = math.sqrt((cities[i][0] - cities[j][0])**2 + 
                                          (cities[i][1] - cities[j][1])**2)
    return g

def main():
    g = read_input('tsp.txt')
    print 'solving...'
    print g
    print tsp.tsp_dp2(g)

if __name__ == '__main__':
    main()

