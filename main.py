import math
import os

all_str = set()
AA = {}

type_helice = {"1": "D-alpha", "2": "D-omega", "3": "D-pi", "4": "D-gamma", "5": "D-310",
       "6": "G-alpha", "7": "G-omega", "8": "G-alpha", "9": "27-ribbon", "10": "Polyproline"}
type_feuillet = {"-1": "anti-parallele", "0": "debut", "1": "parallele"}

with open("AA.txt", "r") as fil:
    for ligne in fil:
        ligne = ligne.replace('\n', '').split(";")
        AA[ligne[1]] = list(map(float, ligne[2:]))

with open("colonnes.txt", 'r') as fil:
    colonnes = fil.readline()
    dic_col = {col: "" if col in ["Structure", "Type", "Sequence"] else 0 for col in colonnes.split(",")}

for sid in os.listdir("Sequence"):
    sid = sid[:-4]
    with open(f"Sequence/{sid}.txt", "r") as fil:
        fil.readline()
        seq = fil.readline()
    with open(f"Structure secondaire/{sid}.txt", "r") as fil:
        for ligne in fil:
            ligne = ligne.split(";")
            debut, fin = 0, 0
            signe, hydro = 0, 0
            if ligne[0] == "HELIX" and len(ligne) == 11 and ligne[4] == "A":
                dic_col["Structure"] = ligne[0]
                debut, fin = int(ligne[5]), int(ligne[8])
                dic_col["Type"] = type_helice[ligne[-2]]
            elif ligne[0] == "SHEET" and len(ligne) == 19 and ligne[5] == "A":
                dic_col["Structure"] = ligne[0]
                debut, fin = int(ligne[6]), int(ligne[9])
                dic_col["Type"] = type_feuillet[ligne[10]]
            if debut < fin and debut < len(seq) and fin < len(seq):
                dic_col["Sequence"] = seq[debut-1:fin-1]
                for acide_amine in seq[debut-1:fin-1]:
                    for i, var in zip(range(len(dic_col.keys())), dic_col.keys()):
                        if type(dic_col[var]) == str:
                            pass
                        elif var == "Taille":
                            dic_col["Taille"] = fin-debut
                        else:
                            dic_col[var] += AA[acide_amine][i]
                for var in dic_col.keys():
                    if type(dic_col[var]) != str and var != "Taille":
                        dic_col[var] = round(dic_col[var] / (fin - debut), 4)
                all_str = all_str.union([dic_col.values()])
            dic_col = {col: 1 if col in ["helice", "feuillet"] else 0 for col in colonnes.split(",")}

with open("structure_secondaire.csv", "w") as filout:
    texte = f"{colonnes}\n"
    for stru in all_str:
        texte += ",".join(list(map(str, stru))) + "\n"
    filout.write(texte)
