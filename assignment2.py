import json
from itertools import combinations, chain
import sys
import os
import time


class AF:
    def __init__(self, arguments, attacks):
        self.arguments = list(arguments)
        self.attacks = attacks

    def get_arguments(self):
        return self.arguments

    def get_attacks(self):
        return self.attacks

    # Only looks at the sets containing one or two elements (for now)
    def cf(self):
        cf_set = []
        subsets = get_subsets(self.arguments)
        for subset in subsets:
            if not has_conflicts(subset, self.attacks):
                cf_set.append(list(subset))
        return cf_set

    def adm(self):
        adm_set = []
        for S in self.cf():
            defended = characteristic_operator(S, self.arguments, self.attacks)
            if set(S) <= set(defended):
                adm_set.append(S)
        return adm_set

    def pref(self):
        pref_set = []
        admissible = self.adm()
        for S in admissible:
            ok = True
            for T in admissible:
                if S != T and set(S) <= set(T):
                    ok = False
            if ok and S not in pref_set:
                pref_set.append(S)
        return pref_set

    def grd(self):
        S = []
        new_arguments = self.arguments.copy()
        new_attacks = self.attacks.copy()
        while True:
            new_S = grd_step1(S, new_arguments, new_attacks)
            if S == new_S:
                return [S]
            new_arguments, new_attacks = grd_step2(new_S, new_arguments, new_attacks)

    def comp(self):
        comp_set = []
        for S in self.cf():
            S = list(S)
            if characteristic_operator(S, self.arguments, self.attacks) == S:
                comp_set.append(S)
        return comp_set

    def stb(self):
        stb_set = []
        for S in self.cf():
            A = self.arguments.copy()
            for s in S:
                if s in A:
                    A.remove(s)
            there_exists = True
            for a in A:
                if not any([b, a] in self.attacks for b in S):
                    there_exists = False
            if there_exists:
                stb_set.append(S)
        return stb_set


def grd_step1(S, arguments, attacks):
    for arg in arguments:
        attacked = False
        for atc in attacks:
            if atc[1] == arg:
                attacked = True
        if not attacked:
            S.append(arg)
    return S


def grd_step2(S, arguments, attacks):
    for a in S:
        for atc in attacks:
            if atc[1] == a:
                attacks.remove(atc)
                arguments.remove(atc[0])
        arguments.remove(a)
    return arguments, attacks


def is_defended(a, S, attacks):
    for atc in attacks:
        if atc[1] == a:
            b = atc[0]
            if not any([c, b] in attacks for c in S):
                return False
    return True


def characteristic_operator(S, arguments, attacks):
    defended = []
    for arg in arguments:
        if is_defended(arg, S, attacks):
            defended.append(arg)
    return defended


def has_conflicts(S, attacks):
    for a in S:
        for b in S:
            if [a, b] in attacks or [b, a] in attacks:
                return True
    return False


def get_subsets(in_set):
    s = list(in_set)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


def is_acceptable(a, F, semantic):

    # print(f'TEST {file_name} {argument}')
    # start_time = time.time()
    cf = F.cf()
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time cf: {elapsed_time} seconds")

    # start_time = time.time()
    adm = F.adm()
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time adm: {elapsed_time} seconds")
    #
    # start_time = time.time()
    pref = F.pref()
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time pref: {elapsed_time} seconds")

    # start_time = time.time()
    grd = F.grd()
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time grd: {elapsed_time} seconds")

    # start_time = time.time()
    comp = F.comp()
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time comp: {elapsed_time} seconds")

    # start_time = time.time()
    stb = F.stb()
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time stb: {elapsed_time} seconds")

    print("cf: " + str(cf))
    print("adm: " + str(adm))
    print("pref: " + str(pref))
    print("grd: " + str(grd))
    print("comp: " + str(comp))
    print("stb: " + str(stb))

    # acceptables = F.cf()
    # acceptables.extend(x for x in F.adm() if x not in acceptables)
    # acceptables.extend(x for x in F.pref() if x not in acceptables)
    # acceptables.extend(x for x in F.grd() if x not in acceptables)
    # acceptables.extend(x for x in F.comp() if x not in acceptables)
    # acceptables.extend(x for x in F.stb() if x not in acceptables)
    # print("acceptables: " + str(acceptables))

    if semantic in locals():
        for x in locals()[semantic]:
            if a[0] in x:
                return f"Argument {a[0]} is accepted under semantics {semantic}"
        return f"Argument {a[0]} is not accepted under semantics {semantic}"
    else:
        return "Invalid semantic"

if __name__ == "__main__":
    file_name = sys.argv[1]
    argument = sys.argv[2]
    semantic = sys.argv[3]

    # Check if 3 arguments are given
    if len(sys.argv) < 3:
        print("Usage: python assignment2.py AF_FILE AF_ARGUMENT SEMANTIC \n"
              "Possible semantics: cf, adm, pref, grf, comp, stb")
        sys.exit(1)

    if os.path.exists(file_name) == False:
        print("ERROR: AF_FILE cannot be found.")
        sys.exit(1)

    argument = [argument]

    f = open(file_name)
    data = json.load(f)
    f.close()

    args = data["Arguments"]
    atcs = data["Attack Relations"]

    F = AF(args, atcs)
    arg = argument
    print(is_acceptable(argument, F, semantic))


