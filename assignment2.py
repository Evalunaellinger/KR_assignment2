import json
import random
from itertools import combinations

f = open("example-argumentation-framework.json")
data = json.load(f)
f.close()

args = data["Arguments"]
atcs = data["Attack Relations"]


# Only looks at the sets containing one or two elements (for now)
def cf(arguments, attacks):
    cf_set = []
    keys = list(arguments.keys())
    for arg in keys:
        if not have_conflict(arg, arg, attacks):
            cf_set.append(arg)
        others = keys
        others.remove(arg)
        for arg2 in others:
            if not have_conflict(arg, arg2, attacks):
                cf_set.append([arg, arg2])
    return cf_set


def adm(arguments, attacks):
    adm_set = []
    for S in cf(arguments, attacks):
        defended = characteristic_operator(S, arguments, attacks)
        if set(S) <= set(defended):
            adm_set.append(S)
    return adm_set


def pref(arguments, attacks):
    pref_set = []
    admissible = adm(arguments, attacks)
    for S in admissible:
        for T in admissible:
            if S != T and not set(S) <= set(T):
                pref_set.append(S)
    return pref_set


def grd(arguments, attacks):
    pass


def comp(arguments, attacks):
    pass


def stb(arguments, attacks):
    pass


def is_defended(a, S, attacks):
    for atc in attacks:
        if atc[1] == a:
            b = atc[0]
            for c in S:
                if conflicts(c, b, attacks):
                    return True
            return False


def characteristic_operator(S, arguments, attacks):
    defended = []
    for arg in list(arguments.keys()):
        if is_defended(arg, S, attacks):
            defended.append(arg)
    return defended


def conflicts(a, b, attacks):
    for atc in attacks:
        if atc[0] == a and atc[1] == b:
            return True
        else:
            return False


def have_conflict(a, b, attacks):
    for atc in attacks:
        if (atc[0] == a and atc[1] == b) or (atc[0] == b and atc[1] == a):
            return True
        else:
            return False


# def get_sets(arguments):
#     arguments = list(arguments.keys())
#     sets = arguments
#     for i in range(2, len(sets)+1):
#         print(list(combinations(arguments, i)))
#         sets.append(combinations(arguments, i))
#     return sets

# class Game:
#
#     def __init__(self, arguments, attacks):
#         self.arguments = arguments
#         self.attacks = attacks
#         self.args_in = []
#         self.args_out = []
#         self.last_in = None
#         self.last_out = None
#
#     def get_arguments(self):
#         return self.arguments
#
#     def get_attacks(self):
#         return self.attacks
#
#     def get_args_in(self):
#         return self.args_in
#
#     def get_args_out(self):
#         return self.args_out
#
#     def add_in(self, arg):
#         self.args_in.append(arg)
#         self.last_in = arg
#
#     def add_out(self, arg):
#         self.args_out.append(arg)
#         self.last_out = arg
#
#     def has_in(self, arg):
#         if arg in self.args_in:
#             return True
#         else:
#             return False
#
#     def has_out(self, arg):
#         if arg in self.args_out:
#             return True
#         else:
#             return False
#
#
# def first_move(game: Game):
#     arg = random.choice(game.get_arguments().keys())
#     game.add_in(arg)
#
#
# def proponent_move(game: Game):
#     prev_arg = game.last_out
#     for attack in game.get_attacks():
#         # next_arg = None
#         added = False
#         if attack[1] == prev_arg:
#             next_arg = attack[0]
#             if not game.has_in(next_arg) and not game.has_out(next_arg):
#                 game.add_in(next_arg)
#                 added = True
#                 break
#     # Returns true if something has changed and we can continue to the next round
#     return added




