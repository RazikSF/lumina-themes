##----- Importation des modules -----##
from random import randint


##----- Définition des fonctions -----##
def etape(liste):
    """Retire deux nombres au hasard, ajoute leur écart."""
    L = [x for x in liste]
    a = L.pop(randint(0, len(L) - 1))
    b = L.pop(randint(0, len(L) - 1))
    L.append(abs(b - a))
    return L


def partie(n):
    liste = [k for k in range(1, n + 1)]
    while len(liste) > 1:
        liste = etape(liste)
    return liste[0]


def plusieurs_parties(n, nb=10):
    """Fin de parties pour une dizaine de parties."""
    resultats = {"pairs": 0, "impairs": 0}
    for k in range(nb):
        cle = "pairs" if partie(n) % 2 == 0 else "impairs"
        resultats[cle] += 1
    return resultats


##----- Tests et interaction -----##
bilan = plusieurs_parties(2019)
print(f"Sur 10 parties : {bilan['pairs']} fins paires, {bilan['impairs']} impaires.")
assert bilan["pairs"] + bilan["impairs"] == 10, "le total doit valoir 10"
