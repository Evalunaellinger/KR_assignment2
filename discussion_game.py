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
    print("ERROR: AF_ARGUMENT is not an argument in AF_FILE."
          "Give the argument as a digit.")
    sys.exit(1)

# START GAME
print('RULES\n'
      '1. Give your argument in the form of a digit i.e. 0.\n \n'
      'THE GAME BEGINS\n')
print(f'My starting (in) argument states "{given_argument}: {arguments[given_argument]}"')
print('')

relevant_attacks_opponent = []
for attack in attack_relations:
    if given_argument == attack[0]:  # Check which attacks state that the given argument is attacked
        relevant_attacks_opponent.append(attack[1])
# combined_attacks_list = [item for sublist in relevant_attacks_opponent for item in sublist]

opponents_used_arguments = []
proponents_used_arguments = []
proponents_used_arguments.append(given_argument)

proponent_argument = given_argument

# GAME LOOP
while True:
    while True:
        user_input = input('What is your (out) argument: ')

        # if user_input not in combined_attacks_list:
        if user_input not in relevant_attacks_opponent:
            print('The input that you gave is not an (out) argument for the given argument.'
                  'Please provide a new argument \n')
        else:
            break

    # EXIT GAME IF OPPONENT USES ARGUMENT TWICE
    if user_input not in opponents_used_arguments:
        opponents_used_arguments.append(user_input)
    else:
        print('You already used this argument, therefore, YOU LOSE!')
        break

    # EXIT GAME IF OPPONENT USES ARGUMENT OF PROPONENT
    if user_input in proponents_used_arguments:
        print('I already used this argument, therefore YOU WIN!')
        break

    # print(f'You chose to attack "{proponents_arguments_underattack[-1]}: {arguments[proponents_arguments_underattack[-1]]}"')
    print(f'Your attack: you state that my argument is "in" because "{user_input}: {arguments[user_input]}" is out.\n')

    # CHECK THE USER INPUT
    possible_proponent_attacks = []

    for attack in attack_relations:
        if user_input == attack[0]: # Check which attacks state that the given argument is attacked
            possible_proponent_attacks.append(attack[1])

    if len(possible_proponent_attacks) == 0:
        'Your argument leaves me with no attacking arguments left, therefore YOU WIN!'

    proponent_attack = random.choice(possible_proponent_attacks)

    if proponent_attack not in proponents_used_arguments:
        proponents_used_arguments.append(proponent_attack)

    print(f'My attack: Your argument is out because "{proponent_attack}: {arguments[proponent_attack]}" is in. \n')

    if proponent_attack in opponents_used_arguments:
        print(f'You already used this argument, therefore I WIN!')
        break

    # The opponent can only choose arguments that attack another argument previously outputted by the proponent.
    # The attacked arguments can be from the previous round, but also from an earlier round.
    argument_to_attack = random.choice(proponents_used_arguments)

    # relevant_attacks_opponent = []
    for attack in attack_relations:
        if argument_to_attack == attack[1]:  # Check which attacks state that the given argument is attacked
            relevant_attacks_opponent.append(attack[0])

    if len(relevant_attacks_opponent) == 0:
        print('My argument leaves you with no attacking arguments left, therefore I WIN!')

    while True:
        chosen_argument_to_attack = input(f'Which argument do you want to attack? You can chose from {proponents_used_arguments}: ')
        if chosen_argument_to_attack not in proponents_used_arguments:
            print('Your given argument is not part of the options.')
        else:
            proponent_attack = chosen_argument_to_attack
            break




