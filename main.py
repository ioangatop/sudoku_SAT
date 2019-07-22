import read_files, split, simplify, time

rules_before_split, literals_dict_before_split, truth_values_before_split = {}, {}, {}
split_choice, neg_literal = [], []

# SDKS
# easy_sdk = "sdks/1000_sudokus.txt"
# hard_sdk = 'sdks/damnhard.sdk.txt'
# sdk_rules = "sdks/sudoku-rules.txt"
# sudokus = read_files.read_sudokus_file(hard_sdk)
# truth_values = sudokus[27]
# rules = read_files.read_DIMACS_file(sdk_rules)
# rules, literals_dict = read_files.init_database(rules)

# SAT
file = 'sudoku2.txt'
DIMACS = read_files.read_DIMACS_file(file)
rules, literals_dict, truth_values = read_files.init_database(DIMACS)

# Choose heuristic: 0 = Basic DPLL (random), 1 = Jeroslow-Wang method, 2 = MOMs method
which_method = 0

print('============ SAT Solver =============')
print_heuristic = ['Basic DPLL (random)', 'Jeroslow-Wang method ', 'MOMs method']
print('    Heuristic: ', print_heuristic[which_method])
print('=====================================\n')

old_clauses_count = len(rules)
back_track_count = 0
split_count = 0
done = False
problem_start_time = time.time()

while done == False:
    back_track = False
    # Simplify
    rules, literals_dict, truth_values, split_choice, neg_literal, \
    rules_before_split, literals_dict_before_split, truth_values_before_split, back_track = \
        simplify.simplify(rules, literals_dict, truth_values, split_choice, neg_literal,
                          rules_before_split, literals_dict_before_split, truth_values_before_split,back_track)
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

    elif old_clauses_count == new_clauses_count and back_track == False:
        # Split
        split_count += 1
        rules, literals_dict, truth_values, split_choice, neg_literal, \
        rules_before_split, literals_dict_before_split, truth_values_before_split = \
            split.split(rules, literals_dict, truth_values, split_choice, neg_literal,
                        rules_before_split, literals_dict_before_split, truth_values_before_split, which_method)
    old_clauses_count = new_clauses_count