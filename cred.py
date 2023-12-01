import json
import sys
import os
from io import StringIO
import random

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python cred.py AF ARGUMENT")
        sys.exit(1)

    AF = str(sys.argv[1])
    Argument = sys.argv[2]
    
    if os.path.exists(AF) == False:
        print("ERROR: AF cannot be found.")
        sys.exit(1)

    
    
    with open(AF, "r") as read_file:
        data = json.load(read_file)

    arguments = data["Arguments"]
    #print(arguments)
    attack_relations = data["Attack Relations"]

    if not Argument in arguments:
        print("ERROR: Argument not in AF")
        sys.exit
    grounded = False
    cred = True
    attacks= []
    while cred == True: 
        # check if Argument is attacking itself 
        for relation in attack_relations:
            print(relation)
            if Argument in relation[1] and Argument in relation[0]:
                cred = False
                print(Argument ,"is not contained in a credible extension of F")
                break

            #check if Argument is is contained in at least one adm-extension of F
            elif Argument in relation[1]:
                attacks.append(relation[0])
        print(attacks)
        #checks if its grounded, so not attacked by anything
        if not attacks:
            grounded = True
            print(Argument," is contained in an extension of F")
            break
        #checks if attacks can all be defended
        attacks_copy =attacks.copy()
        for relation in attack_relations:
            removed_flag = False
            for attack in attacks_copy:
                if attack in relation[1]:
                    attacks.remove(attack)
                    removed_flag = True
            if removed_flag:
                break
        if attacks:
            cred = False
            print(Argument," is not contained in a credible extensions of F, because it is not defended against ", attacks)
            break
        else: 
            print(Argument, " is contained in an extension of F")
            break

        #Evaluate the grounded extension of AF
            #check if argument in the preferred set of AF
            #check id argument is in the grounded set of AF
        # else: 
        #     if not grounded: 


        


    

