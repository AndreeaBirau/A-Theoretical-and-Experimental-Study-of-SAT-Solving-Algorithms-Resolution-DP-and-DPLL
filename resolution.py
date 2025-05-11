
import time
import os
import psutil

def read_clauses(file_path):
    with open(file_path, 'r') as f:
        return [sorted(map(int, line.strip().split())) for line in f]

def has_conflicting_literals(clause):
    return any(-literal in clause for literal in clause)

def filter_clauses(clauses):
    return [c for c in clauses if not has_conflicting_literals(c)]

def combine_clauses(clause_a, clause_b):
    resolved = []
    skip_literal = None

    for literal in clause_a:
        if -literal in clause_b and skip_literal is None:
            skip_literal = literal
        else:
            resolved.append(literal)

    for literal in clause_b:
        if literal != -skip_literal and literal not in resolved:
            resolved.append(literal)

    if any(-lit in resolved for lit in resolved):
        return None

    return sorted(resolved) if len(resolved) <= max(len(clause_a), len(clause_b)) else None

def satisfiable(clauses):
    while True:
        new_set = []

        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                new_clause = combine_clauses(clauses[i], clauses[j])
                
                if new_clause == []:
                    return False
                if new_clause and new_clause not in clauses and new_clause not in new_set:
                    new_set.append(new_clause)

        if not new_set:
            return True

        clauses.extend(new_set)

def main():
    start_time = time.time()

    input_file = "./clauses.cnf"
    clauses = read_clauses(input_file)
    clauses = filter_clauses(clauses)

    result = "SATISFIABLE" if satisfiable(clauses) else "UNSATISFIABLE"
    print(f"The clauses are {result}")

    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss
    print(f"Memory used: {memory_usage}B ({memory_usage / (1024**2):.2f} MB)")

    elapsed_time = time.time() - start_time
    print(f"Execution time: {elapsed_time:.3f} seconds")

if __name__ == "__main__":
    main()

