"""Solve 2 SAT problem."""

import collections
import math
import random

class Partial_Solution:
    """Represents a partial solution."""
    UNASSIGNED = -1

    def __init__(self, size):
        # use an array to represent a solution
        # sol[x] = True for assinging variable x to True
        #        = False for assigning variable x to False
        #        = -1 for the variable x have not been assigned.
        self.sol = [self.UNASSIGNED] * (size + 1)
        self.assigned_values = 0
        self.size = size


    def must_false_clause(self, x1, x2):
        """Return True if the clause X1 OR X2 must be false for current partial solution."""
        x1_index = abs(x1)
        x2_index = abs(x2)
        x1_bool = x1 > 0
        x2_bool = x2 > 0

        if (self.sol[x1_index] == self.UNASSIGNED or
            self.sol[x2_index] == self.UNASSIGNED):
            return False

        return  (x1_bool != self.sol[x1_index] and
                 x2_bool != self.sol[x2_index])

    def not_satisfiable(self, expression):
        """Return True if the expression will not be satified by the parital solution."""
        return any(self.must_false_clause(x1, x2) for x1, x2 in expression)

    def set_sol(self, x):
        x_index = abs(x)
        x_bool = x > 0

        if self.sol[x_index] == self.UNASSIGNED:
            self.assigned_values += 1

        self.sol[x_index] = x_bool

    def unassigned_variables(self):
        for i in range(1, len(self.sol)):
            if self.sol[i] == self.UNASSIGNED:
                yield i

    def get_next_unassigned(self):
        for i in range(1, len(self.sol)):
            if self.sol[i] == self.UNASSIGNED:
                return i

    def get_copy(self):
        new_sol = Partial_Solution(self.size)
        new_sol.sol = list(self.sol)
        new_sol.assigned_values = self.assigned_values
        return new_sol

    def get_sol(self):
        return [self.sol[i] for i in range(1, len(self.sol))]

    def get_assigned(self):
        return ', '.join(str(i) for i in range(1, len(self.sol))
                         if self.sol[i] != self.UNASSIGNED)

class Sol2():

    def __init__(self, var_cnt, clauses):
        self.sol = []
        # make random assignment for each variable
        for i in xrange(var_cnt):
            self.sol.append(random.choice([True, False]))

        # map variable to clauses
        self.unsat_clauses = set()
        self.vars = collections.defaultdict(set)
        for x1, x2 in clauses:
            if not self.is_true(x1, x2):
                self.unsat_clauses.add((x1, x2))

            self.vars[abs(x1)].add((x1, x2))
            self.vars[abs(x2)].add((x1, x2))

    def get_assignment(self, x):
        x_index = abs(x) - 1
        return self.sol[x_index]

    def flip_assignment(self, x):
        x_before = self.get_assignment(x)
        x_index = abs(x) - 1
        self.sol[x_index] = not self.sol[x_index]

        for x1, x2 in self.vars[abs(x)]:
            is_sat_before = self.is_true_without_flip(x1, x2, x)
            is_sat_aft = self.is_true(x1, x2)

            if not is_sat_before and is_sat_aft and (x1, x2) in self.unsat_clauses:
                self.unsat_clauses.remove((x1, x2))
            elif is_sat_before and not is_sat_aft:
                self.unsat_clauses.add((x1, x2))

    def is_true(self, x1, x2):
        x1_bool = x1 > 0
        x2_bool = x2 > 0
        return (x1_bool == self.get_assignment(x1) or 
                x2_bool == self.get_assignment(x2))

    def is_true_without_flip(self, x1, x2, flipped_x):
        x1_bool = x1 > 0
        x2_bool = x2 > 0
        if abs(x1) == abs(flipped_x):
            x1_assign = not self.get_assignment(x1)
            x2_assign = self.get_assignment(x2)
        else:
            x1_assign = self.get_assignment(x1)
            x2_assign = not self.get_assignment(x2)

        return (x1_bool == x1_assign or x2_bool == x2_assign)

    def assert_all_true(self, clauses):
        for x1, x2 in clauses:
            assert self.is_true(x1, x2)
        
    def flip_for_unsatisfied(self):
        """For each unsatisfied clause, randomly choose a varible and flip the sign."""
        to_flip = set()
        for x1, x2 in self.unsat_clauses:
            to_flip.add(random.choice([abs(x1), abs(x2)]))

        for x in to_flip:
            self.flip_assignment(x)
        return len(to_flip)


def backtrack(var_cnt, clauses):
    """Solve 2 SAT with backtrack.

    clauses contain list of clauses, each is a tuple
    of the two variables OR'ed together
    """
    sol = Partial_Solution(var_cnt)

    stack = [sol]

    while len(stack) > 0:
        cur_sol = stack.pop(-1)

        if cur_sol.not_satisfiable(clauses):
            continue

        if cur_sol.assigned_values == var_cnt:
            # Satisfiable
            return 'Satisfiable' #cur_sol

        x = cur_sol.get_next_unassigned()
        new_sol_true = cur_sol.get_copy()
        new_sol_true.set_sol(x)
        stack.append(new_sol_true)

        new_sol_false = cur_sol.get_copy()
        new_sol_false.set_sol(-x)
        stack.append(new_sol_false)

    return False


def papadimitrious(var_cnt, clauses):
    """Solve 2 SAT with papadimitrious."""
    print 'Done with initial assignment'
    for i  in xrange(int(math.log(var_cnt, 2))):
        cur_sol = Sol2(var_cnt, clauses)
        last_unsat_clauses = len(clauses)
        unchanged_iters = 0
        for j in xrange(2*var_cnt**2):
            unsat_clauses = cur_sol.flip_for_unsatisfied()
            if abs(last_unsat_clauses - unsat_clauses) > 3:
                last_unsat_clauses = unsat_clauses
                unchanged_iters = 0
            else:
                unchanged_iters += 1
                if unchanged_iters > 100000:
                    break

            print i, j, unchanged_iters, unsat_clauses
            if unsat_clauses == 0:
                cur_sol.assert_all_true(clauses)
                return 'Satisfiable'

    return False
    

def main():
    sol = Partial_Solution(3)
    assert sol.must_false_clause(1, 2) == False
    assert sol.must_false_clause(1, -2) == False

    assert [x for x in sol.unassigned_variables()] == [1, 2, 3]
    assert sol.get_next_unassigned() == 1

    sol.set_sol(1)
    assert sol.assigned_values == 1
    assert [x for x in sol.unassigned_variables()] == [2, 3]
    assert sol.get_next_unassigned() == 2
    sol.set_sol(3)
    assert sol.assigned_values == 2
    assert [x for x in sol.unassigned_variables()] == [2]
    assert sol.get_next_unassigned() == 2

    assert sol.must_false_clause(1, -3) == False
    assert sol.must_false_clause(-1, 3) == False
    assert sol.must_false_clause(-1, -3) == True
    assert sol.must_false_clause(1, 3) == False

    sol.set_sol(-1)
    assert sol.assigned_values == 2
    assert [x for x in sol.unassigned_variables()] == [2]
    sol.set_sol(-3)
    assert sol.assigned_values == 2
    assert [x for x in sol.unassigned_variables()] == [2]

    assert sol.must_false_clause(-1, -3) == False
    assert sol.must_false_clause(1, 1) == True

    cp_sol = sol.get_copy()
    assert cp_sol.assigned_values == sol.assigned_values
    assert ([x for x in cp_sol.unassigned_variables()] ==
            [x for x in cp_sol.unassigned_variables()])
    assert cp_sol.sol == sol.sol

    expression1 = ((1, 2), (-1, -1))
    assert backtrack(2, expression1) == 'Satisfiable'

    sol = Sol2(2, expression1)
    sol.sol[0] = True
    sol.sol[1] = False

    assert sol.is_true(1, 2)
    assert not sol.is_true_without_flip(1, 2, 1)
    assert sol.is_true_without_flip(1, 2, 2)

    assert not sol.is_true(-1, 2)
    assert sol.is_true_without_flip(-1, 2, 1)
    assert sol.is_true_without_flip(-1, 2, 2)

    assert sol.is_true(-1, -2)
    assert sol.is_true_without_flip(-1, -2, 1)
    assert not sol.is_true_without_flip(-1, -2, 2)

    assert sol.is_true(1, -2)
    assert sol.is_true_without_flip(1, -2, 1)
    assert sol.is_true_without_flip(1, -2, 2)

    print '-*'*10
    print sol.sol
    print sol.vars

    from hw6 import read_input
    for i in range(1, 5):
        filename = 'test%s.txt' % i
        variable_cnt, clauses = read_input(filename)
        print '-----(%s) # of Variables %s----------' % (i, variable_cnt)
        print clauses
        assert backtrack(variable_cnt, clauses) == papadimitrious(variable_cnt, clauses)


if __name__ == '__main__':
    main()
