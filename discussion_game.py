import json
import sys
import os
import random

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

# START GAME
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

is_dictionary = isinstance(arguments, dict)
if is_dictionary == False:
    arguments = {key: "" for key in arguments}

print(f'P: "{given_argument}" is in. \n')

relevant_attacks_opponent = []
for attack in attack_relations:
    # FORWARD
    if given_argument == attack[0]:  # Check which attacks state that the given argument is attacked
        if attack[1] not in relevant_attacks_opponent:
            relevant_attacks_opponent.append(attack[1])
    # BACKWARD
    if given_argument == attack[1]:
        if attack[0] not in relevant_attacks_opponent:
            relevant_attacks_opponent.append(attack[0])

opponents_used_arguments = []
proponents_used_arguments = []
proponents_used_arguments.append(given_argument)
proponent_argument = given_argument

possible_attacks_opponent = [element for element in relevant_attacks_opponent if element not in opponents_used_arguments]

# GAME LOOP
while True:
    # relevant_attacks_opponent_ = list(set(relevant_attacks_opponent))

    print(f'Valid attacks: {relevant_attacks_opponent}')
    print(f'Already used attacks: {opponents_used_arguments}')
    print(f'Possible attacks: {possible_attacks_opponent} \n')

    # Returns true if all relevant attacks have already been used
    check_arguments_left = all(elem in opponents_used_arguments for elem in relevant_attacks_opponent)

    if check_arguments_left == True:  # GAME RULE 3 and WINNER RULE 4
        print('The opponent has no choices left, as all relevant attacks have already been used, '
              'therefore THE PROPONENT WINS!')
        exit(1)

    while True:
        user_input = input('Select opponents (out) argument: ')
        print('')

        if user_input not in relevant_attacks_opponent:
            print('The input that you gave is not an (out) argument for the given argument.'
                  'Please provide a new argument \n')
        else:
            break

    while True:
        if user_input not in opponents_used_arguments:
            opponents_used_arguments.append(user_input)
            break
        else: # GAME RULE 3
            print(f'The opponent already used this argument.')
            user_input = input(f'Choose from {possible_attacks_opponent}: ')

    # WINNER RULE 1
    if user_input in proponents_used_arguments:
        print('The proponent already used this argument, therefore THE OPPONENT WINS!')
        break

    # print(f'O: The proponents argument is "in" because "{user_input}: {arguments[user_input]}" is out.')
    print(f'O: The proponents argument is "in" because "{user_input}" is out.')

    # CHECK THE USER INPUT
    possible_proponent_attacks = []

     # GAME RULE 2
    for attack in attack_relations:
        if user_input == attack[0]: # Check which attacks state that the given argument is attacked
            possible_proponent_attacks.append(attack[1])
        if user_input == attack[1]:
            possible_proponent_attacks.append(attack[0])

    # WINNER RULE 3
    if len(possible_proponent_attacks) == 0:
        print('The proponent cannot make a move, therefore THE OPPONENT WINS!')
        break

    proponent_attack = random.choice(possible_proponent_attacks)

    # For the print of possible arguments to attack
    if proponent_attack not in proponents_used_arguments:
        proponents_used_arguments.append(proponent_attack)

    # print(f'P: The opponents argument is out because "{proponent_attack}: {arguments[proponent_attack]}" is in. \n')
    print(f'P: The opponents argument is "out" because "{proponent_attack}" is in. \n')

    # WINNER RULE 2
    if proponent_attack in opponents_used_arguments:
        print(f'The opponent already used this argument, therefore THE OPPONENT WINS!')
        break

    # All possible arguments to attack
    # argument_to_attack = random.choice(proponents_used_arguments)

    while True:
        # GAME RULE 1
        chosen_argument_to_attack = input(f'Select argument opponent wants to attack: {proponents_used_arguments}: ')
        print('\n')
        if chosen_argument_to_attack not in proponents_used_arguments:
            print('The given argument is not part of the options.')
        else:
            proponent_attack = chosen_argument_to_attack
            break

    relevant_attacks_opponent = []
    for attack in attack_relations:
        if chosen_argument_to_attack == attack[1]:  # Check which attacks state that the given argument is attacked
            if attack[0] not in relevant_attacks_opponent:
                relevant_attacks_opponent.append(attack[0])
        if chosen_argument_to_attack == attack[0]:
            if attack[1] not in relevant_attacks_opponent:
                relevant_attacks_opponent.append(attack[1])

    possible_attacks_opponent = [element for element in relevant_attacks_opponent if element not in opponents_used_arguments]

    # WINNER RULE 4
    if len(relevant_attacks_opponent) == 0:
        print('The opponent has no choices left, therefore THE PROPONENT WINS!')
        break