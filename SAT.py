import read_files, split, simplify, pretty_print, check_sudoku
import time, sys


def solve(heuristic, file):
    start = time.time()
    heuristics = {
        1: "Basic DPLL -- Random",
        2: "Jeroslow-Wang",
        3: "MOMs"
    }
    print('')
    print('=============== SAT Solver ================')
    print("Solving using {} heuristic".format(heuristics[int(heuristic)]))
    print('...\n')

    which_method = int(heuristic)

    rules = read_files.read_DIMACS_file(file)
    rules, literals_dict, truth_values = read_files.init_database(rules)
    rules_before_split, literals_dict_before_split, truth_values_before_split = {}, {}, {}
    split_choice, neg_literal = [], []
    old_clauses_count = len(rules)
    back_track_count = 0
    split_count = 0
    done = False
    problem_start_time = time.time()

    while done == False:
        back_track = False
        # Simplify
        rules, literals_dict, truth_values, split_choice, neg_literal, \
        rules_before_split, literals_dict_before_split, truth_values_before_split, back_track, file = \
            simplify.simplify(rules, literals_dict, truth_values, split_choice, neg_literal,
                              rules_before_split, literals_dict_before_split, truth_values_before_split, back_track, file)
        new_clauses_count = len(rules)
        if back_track:
            back_track_count += 1

        if new_clauses_count == 0:

            print('The problem has a solution -- SAT')
            print("Solved in {0:.2f}s".format(time.time() - problem_start_time))
            print("Number of splits: {}".format(split_count))
            print("Number of backtracks: {}".format(back_track_count))
            print('The solution can be found at the file: {}.out'.format(str(file)))
            print('')
            done = True
            with open("{}.out".format(file),'w') as f:
                f.write("p cnf {} {}\n".format(len(truth_values), len(truth_values)))
                for truth in truth_values:
                    f.write("{} 0\n".format(truth))


        elif old_clauses_count == new_clauses_count and back_track == False:
            split_count += 1
            # Split
            rules, literals_dict, truth_values, split_choice, neg_literal, \
            rules_before_split, literals_dict_before_split, truth_values_before_split = \
                split.split(rules, literals_dict, truth_values, split_choice, neg_literal,
                            rules_before_split, literals_dict_before_split, truth_values_before_split, which_method)
        old_clauses_count = new_clauses_count

heuristic = sys.argv[1][2]
file = sys.argv[2]
solve(heuristic,file)