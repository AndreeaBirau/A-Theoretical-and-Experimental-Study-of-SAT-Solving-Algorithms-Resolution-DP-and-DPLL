import time
import os
import psutil
from Rezolutie import create_matrix_from_file, remove_trivial_clauses, combine_clauses

def contains_unit_clause(clauses):
    return any(len(c) == 1 for c in clauses)

def find_pure_literal(clauses):
    literal_count = {}
    for clause in clauses:
        for literal in clause:
            literal_count[literal] = True
    return next((lit for lit in literal_count if -lit not in literal_count), None)

def clauses_remaining(clauses):
    return len(clauses) > 0

def propagate_unit_clause(clauses):
    unit = next((c[0] for c in clauses if len(c) == 1), None)
    return [
        [lit for lit in clause if lit != -unit]
        for clause in clauses if unit not in clause
    ]

def eliminate_pure_literal(clauses, pure_literal):
    return [c for c in clauses if pure_literal not in c]

def resolve_clauses(clauses):
    new_clauses = []
    for idx, clause1 in enumerate(clauses[:-1]):
        for clause2 in clauses[idx + 1:]:
            resolved = combine_clauses(clause1, clause2)
            if resolved == []:
                return False
            if resolved and resolved not in clauses and resolved not in new_clauses:
                new_clauses.append(resolved)
    if new_clauses:
        clauses.extend(new_clauses)
        return clauses
    return True

def check_satisfiability(clauses):
    while clauses_remaining(clauses):
        while contains_unit_clause(clauses):
            clauses = propagate_unit_clause(clauses)

        if not clauses_remaining(clauses):
            return True

        if [] in clauses:
            return False

        while (pure := find_pure_literal(clauses)) is not None:
            clauses = eliminate_pure_literal(clauses, pure)

        if not clauses_remaining(clauses):
            return True

        clauses = resolve_clauses(clauses)
        if clauses in [True, False]:
            return clauses
    return True

def main():
    start_time = time.time()

    clause_matrix = create_matrix_from_file("./clauses.cnf")
    clause_matrix = remove_trivial_clauses(clause_matrix)

    satisfiability = "SATISFIABLE" if check_satisfiability(clause_matrix) else "UNSATISFIABLE"
    print(f"The clauses are {satisfiability}")

    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss
    print(f"Memory usage: {memory_usage}B")
    print(f"Memory usage: {memory_usage / 1024:.2f}KB")
    print(f"Memory usage: {memory_usage / (1024**2):.2f}MB")
    print(f"Memory usage: {memory_usage / (1024**3):.2f}GB")

    total_time = time.time() - start_time
    print(f"Execution time: {total_time:.3f} seconds")

if __name__ == "__main__":
    main()
