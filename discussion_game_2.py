import json
import sys
import os
import random

class AF:
    def __init__(self, given_argument, attack_relations):
        self.proponent_argument = given_argument
        self.opponent_argument = None
        self.relevant_attacks_opponent = []
        self.attack_relations = attack_relations

        self.opponents_used_arguments = []
        self.proponents_used_arguments = []
        self.proponents_used_arguments.append(given_argument)

        self.possible_attacks_opponent = []
        self.possible_attacks_proponent = []

    def print_game_rules(self):
        print('Note: Give your argument in the form of a digit i.e. 0. \n'
              'GAME RULES\n'
              '1. The opponent can only choose arguments that attack another argument previously outputted by the proponent. \n'
              'The attacked arguments can be from the previous round, but also from an earlier round. \n'
              '2. The proponent always has to answer with an argument that attacks the argument that the opponent selected in the directly preceding round. \n'
              '3. The opponent is not allowed to use the same argument twice. (The proponent however can.) \n \n'
              'WINNER RULES \n'
              '1. If the opponent uses an argument previously used by the proponent, then the opponent wins (because he has shown that the proponent contradicts itself). \n'
              '2. If the proponent uses an argument previously used by the opponent, then the opponent wins (for similar reasons as in the previous point). \n'
              '3. If the proponent is unable to make a move, then the opponent wins. \n'
              '4. If the opponent has no choices left, then the proponent wins. \n \n'
              'THE GAME BEGINS\n')

    def fill_relevant_attacks_opponent(self):
        # print('test')
        self.relevant_attacks_opponent = []
        for attack in self.attack_relations:
            # FORWARD
            # if self.proponent_argument == attack[0]:  # Check which attacks state that the given argument is attacked
            #     if attack[1] not in self.relevant_attacks_opponent:
            #         self.relevant_attacks_opponent.append(attack[1])
            # BACKWARD
            if self.proponent_argument == attack[1]:
                if attack[0] not in self.relevant_attacks_opponent:
                    self.relevant_attacks_opponent.append(attack[0])

    def calculate_possible_attacks_opponent(self):
        self.possible_attacks_opponent = []
        self.possible_attacks_opponent = [element for element in self.relevant_attacks_opponent if element not in self.opponents_used_arguments]
        return self.possible_attacks_opponent

    def print_opponent_attack_info(self):
        print(f'Valid attacks: {self.relevant_attacks_opponent}')
        print(f'Already used attacks: {self.opponents_used_arguments}')
        print(f'Possible attacks: {self.possible_attacks_opponent} \n')


    def check_opponent_no_choices(self):
        if len(self.possible_attacks_opponent) == 0:
            print('WINNER RULE 1: The opponent has no choices left, as all relevant attacks have already been used, '
                  'therefore THE PROPONENT WINS!')
            return True

    def prompt_argument_opponent(self):
        while True:
            self.opponent_argument = input('Select opponents (out) argument: ')
            print('')

            if self.opponent_argument not in self.relevant_attacks_opponent:
                print('The input that you gave is not an (out) argument for the given argument.'
                      'Please provide a new argument \n')
            else:
                break

    # GAME RULE 3
    def check_opponent_argument_double_use(self):
        while True:
            if self.opponent_argument not in self.opponents_used_arguments:
                self.opponents_used_arguments.append(self.opponent_argument)
                break
            else: # GAME RULE 3
                print(f'The opponent already used this argument.')
                self.opponent_argument = input(f'Choose from {self.possible_attacks_opponent}: ')

    def winner_rule_1(self):
        # WINNER RULE 1
        if self.opponent_argument in self.proponents_used_arguments:
            print('WINNER RULE 1: The proponent already used this argument, therefore THE OPPONENT WINS!')
            return True

    def print_opponent_attack(self):
        print(f'O: The proponents argument is "in" because "{self.opponent_argument}" is out.')

    def calculate_possible_proponent_attacks(self):
        # CHECK THE USER INPUT
        self.possible_attacks_proponent = []

         # GAME RULE 2
        for attack in self.attack_relations:
            # # FORWARD
            # if self.opponent_argument == attack[0]: # Check which attacks state that the given argument is attacked
            #     self.possible_attacks_proponent.append(attack[1])
            # BACKWARD
            if self.opponent_argument == attack[1]:
                self.possible_attacks_proponent.append(attack[0])

    def winner_rule3(self):
        if len(self.possible_attacks_proponent) == 0:
            print('WINNER RULE 3: The proponent cannot make a move, therefore THE OPPONENT WINS!')
            return True

    def pick_and_print_proponent_attack(self):
        self.proponent_argument = random.choice(self.possible_attacks_proponent)

        # For the print of possible arguments to attack
        if self.proponent_argument not in self.proponents_used_arguments:
            self.proponents_used_arguments.append(self.proponent_argument)

        print(f'P: The opponents argument is "out" because "{self.proponent_argument}" is in. \n')

    def winner_rule2(self):
        if self.proponent_argument in self.opponents_used_arguments:
            print(f'WINNER RULE 2: The opponent already used this argument, therefore THE OPPONENT WINS!')
            return True

    def pick_opponent_argument(self):
        while True:
            # GAME RULE 1
            chosen_argument_to_attack = input(f'Select argument opponent wants to attack: {self.proponents_used_arguments}: ')
            print('\n')
            if chosen_argument_to_attack not in self.proponents_used_arguments:
                print('The given argument is not part of the options.')
            else:
                self.proponent_argument = chosen_argument_to_attack
                break

    def winner_rule4(self):
        if len(self.relevant_attacks_opponent) == 0:
            print('WINNER RULE 4: The opponent has no choices left, therefore THE PROPONENT WINS!')
            return True

if __name__ == "__main__":
    af_file = sys.argv[1]
    given_argument = sys.argv[2]

    f = open(af_file)
    data = json.load(f)

    arguments = data['Arguments']
    attack_relations = data["Attack Relations"]

    # Check if 3 arguments are given
    if len(sys.argv) < 3:
        print("Usage: python discussion_game.py AF_FILE AF_ARGUMENT")
        sys.exit(1)

    if os.path.exists(af_file) == False:
        print("ERROR: AF_FILE cannot be found.")
        sys.exit(1)

    if given_argument not in arguments:
        print("ERROR: AF_ARGUMENT is not an argument in AF_FILE.\n" 
              "Give the argument as a digit or letter.")
        sys.exit(1)

    is_dictionary = isinstance(arguments, dict)
    if is_dictionary == False:
        arguments = {key: "" for key in arguments}

    AF = AF(given_argument, attack_relations)

    AF.print_game_rules()

    # STARTING ARGUMENT
    print(f'P: "{given_argument}" is in. \n')

    AF.fill_relevant_attacks_opponent()
    AF.calculate_possible_attacks_opponent()

    # GAME LOOP
    while True:
        AF.print_opponent_attack_info() # Prints the possible attacks of the opponent
        if AF.check_opponent_no_choices(): # Proponent wins if the opponent has already used all the possible attacks
            break
        AF.prompt_argument_opponent() # Prompts the opponent for an attacking argument
        AF.check_opponent_argument_double_use() # Checks GAME RULE 3: the opponent cannot use an argument twice
        if AF.winner_rule_1(): # checks WINNER RULE 1
            break
        AF.print_opponent_attack() # Prints opponent attack
        AF.calculate_possible_proponent_attacks()
        if AF.winner_rule3():
            break
        AF.pick_and_print_proponent_attack()
        if AF.winner_rule2():
            break
        AF.pick_opponent_argument()
        AF.fill_relevant_attacks_opponent()
        AF.calculate_possible_attacks_opponent()
        if AF.winner_rule4():
            break
