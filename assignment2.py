import json
import random
from itertools import combinations, chain

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
    S = []
    arguments = list(arguments.keys())

    def step1(S, arguments, attacks):
        for arg in arguments:
            attacked = False
            for atc in attacks:
                if atc[1] == arg:
                    attacked = True
            if not attacked:
                S.append(arg)
        return S

    def step2(S, arguments, attacks):
        for a in S:
            for atc in attacks:
                if atc[1] == a:
                    attacks.remove(atc)
                    arguments.remove(atc[0])
            arguments.remove(a)
        return arguments, attacks

    while True:
        new_S = step1(S, arguments, attacks)
        if S == new_S:
            return S
        arguments, attacks = step2(new_S, arguments, attacks)


"""
Didn't know that an algorithm was given in the slides but this is a complete search
"""
# def grd(arguments, attacks):
#     grd_set = []
#     subsets = get_subsets(arguments.keys())
#     for S in subsets:
#         if characteristic_operator(S, arguments, attacks) == S:
#             lfp_possible = True
#             for S_prime in subsets:
#                 if characteristic_operator(S_prime, arguments, attacks) == S_prime:
#                     if not set(S) <= set(S_prime):
#                         lfp_possible = False
#                         break
#             if lfp_possible:
#                 grd_set.append(S)
#     return grd_set


def comp(arguments, attacks):
    comp_set = []
    for S in get_subsets(arguments.keys()):
        if characteristic_operator(S, arguments, attacks) == S:
            comp_set.append(S)
    return comp_set


def stb(arguments, attacks):
    stb_set = []
    for S in cf(arguments, attacks):
        A = arguments
        A.remove(S)
        there_exists = True
        for a in A:
            if not any(conflicts(b, a, attacks) for b in S):
                there_exists = False
        if there_exists:
            stb_set.append(S)


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


def get_subsets(in_set):
    s = list(in_set)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


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




