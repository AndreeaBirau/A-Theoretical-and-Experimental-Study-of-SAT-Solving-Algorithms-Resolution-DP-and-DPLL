import time
import os
import psutil
from Rezolutie import create_matrix_from_file, remove_trivial_clauses
from collections import Counter
import copy

def identify_split_literal(clauses):
    frequency = Counter()
    for clause in clauses:
        for literal in clause:
            frequency[abs(literal)] += 1
    return frequency.most_common(1)[0][0]

def dpll_satisfiability(clauses):
    while clauses:
        while any(len(clause) == 1 for clause in clauses):
            unit = next(clause[0] for clause in clauses if len(clause) == 1)
            clauses = [
                [lit for lit in clause if lit != -unit]
                for clause in clauses if unit not in clause
            ]

        if not clauses:
            return True
        if [] in clauses:
            return False

        literal_occurrences = {lit for clause in clauses for lit in clause}
        pure_literals = {lit for lit in literal_occurrences if -lit not in literal_occurrences}
        for pure_literal in pure_literals:
            clauses = [clause for clause in clauses if pure_literal not in clause]

        if not clauses:
            return True

        split_literal = identify_split_literal(clauses)
        left_branch = copy.deepcopy(clauses) + [[split_literal]]
        right_branch = copy.deepcopy(clauses) + [[-split_literal]]

        return dpll_satisfiability(left_branch) or dpll_satisfiability(right_branch)

    return True

def main():
    start_time = time.time()

    clause_matrix = create_matrix_from_file("./clauses.cnf")
    clause_matrix = remove_trivial_clauses(clause_matrix)

    is_satisfiable = dpll_satisfiability(clause_matrix)
    print(f"The clauses are {'SATISFIABLE' if is_satisfiable else 'UNSATISFIABLE'}")

    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"Memory consumed: {memory_info.rss}B")
    print(f"Memory consumed: {memory_info.rss / 1024:.2f}KB")
    print(f"Memory consumed: {memory_info.rss / (1024**2):.2f}MB")
    print(f"Memory consumed: {memory_info.rss / (1024**3):.2f}GB")

    elapsed_time = time.time() - start_time
    print(f"Execution time: {elapsed_time:.3f} seconds")

if __name__ == "__main__":
    main()

