__author__ = 'Samuel'

from scipy.sparse import coo_matrix


def add_bimap(bimap, item):
    if item not in bimap:
        idx = len(bimap)//2
        bimap[idx] = item
        bimap[item] = idx


class SparseOccurrenceMatrix:
    def __init__(self):
        self.row = {}
        self.col = {}
        self.matrix = ([], ([], []))

    def __str__(self):
        return '\n'.join('(%s, %s) (%s, %s) %s' %
                         (self.matrix[1][0][i],
                          self.matrix[1][1][i],
                          self.row[self.matrix[1][0][i]],
                          self.col[self.matrix[1][1][i]],
                          self.matrix[0][i])
                         for i in range(0, len(self.matrix[0])))

    def add(self, row, col, count):
        add_bimap(self.row, row)
        add_bimap(self.col, col)
        self.matrix[0].append(count)
        self.matrix[1][0].append(self.row[row])
        self.matrix[1][1].append(self.col[col])

    def add_row(self, row, data):
        line = {}
        for col in data:
            if col not in line:
                line[col] = 1
            else:
                line[col] += 1

        add_bimap(self.row, row)
        for col in line:
            add_bimap(self.col, col)
            self.matrix[0].append(line[col])
            self.matrix[1][0].append(self.row[row])
            self.matrix[1][1].append(self.col[col])

    def get_sparse(self):
        return coo_matrix(self.matrix)
