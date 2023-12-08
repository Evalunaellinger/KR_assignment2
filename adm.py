import json
import sys
import os
defended = True
def is_admissible(argument, attacks):
    if not attacks[argument]:
        return True
    else:
        Argument = argument
        for attacker in attacks[argument]:
            print(argument, "is attacked by", attacker)
            if not attacks[attacker]:
                print(Argument, "can't be defended against", attacker)
                return False
            else:
                for defender in attacks[attacker]:
                    print(defender, "defends", argument, "against", attacker)
                    if not is_admissible(defender, attacks):
                        defended = False
                    else: 
                        defended = True
                        Defender = defender
                if defended == False:
                    return False
                else:
                    print(argument, "is admissible because", attacker, "is defended against by ", Defender)
        return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cred.py AF ARGUMENT")
        sys.exit(1)

    AF = str(sys.argv[1])
    Argument = sys.argv[2]

    if not os.path.exists(AF):
        print("ERROR: AF cannot be found.")
        sys.exit(1)

    with open(AF, "r") as read_file:
        data = json.load(read_file)

    arguments = data["Arguments"]
    attack_relations = data["Attack Relations"]
    if Argument not in arguments:
        print("ERROR: Argument not in AF")
        sys.exit(1)

    attacks = {}
    for argument in arguments:
        attacks[argument] = list()

    for relation in attack_relations:
        if relation[0] not in attacks[relation[1]]:
            attacks[relation[1]].append(relation[0])
    print(attacks)

    if is_admissible(Argument, attacks):
        print(Argument, "is admissible.")
    else:
        print(Argument, "is not admissible.")