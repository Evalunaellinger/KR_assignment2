import json
from itertools import combinations, chain

f = open("example-argumentation-framework copy.json")
data = json.load(f)
f.close()

args = data["Arguments"]
atcs = data["Attack Relations"]


class AF:
    def __init__(self, arguments, attacks):
        self.arguments = list(arguments.keys())
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
        for S in get_subsets(self.arguments):
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


def is_acceptable(a, F):
    cf = F.cf()
    adm = F.adm()
    pref = F.pref()
    grd = F.grd()
    comp = F.comp()
    stb = F.stb()

    print("cf: " + str(cf))
    print("adm: " + str(adm))
    print("pref: " + str(pref))
    print("grd: " + str(grd))
    print("comp: " + str(comp))
    print("stb: " + str(stb))

    acceptables = F.cf()
    acceptables.extend(x for x in F.adm() if x not in acceptables)
    acceptables.extend(x for x in F.pref() if x not in acceptables)
    acceptables.extend(x for x in F.grd() if x not in acceptables)
    acceptables.extend(x for x in F.comp() if x not in acceptables)
    acceptables.extend(x for x in F.stb() if x not in acceptables)

    print("acceptables: " + str(acceptables))
    if a in acceptables:
        return True
    else:
        return False


F = AF(args, atcs)
arg = ["a"]
print(is_acceptable(arg, F))


