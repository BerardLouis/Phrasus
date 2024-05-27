from bs4 import BeautifulSoup #importer les modules
import codecs  
import os
import re
start = "transcriptions/" #le nom du dossier où sont les fichiers audios
files = []

with codecs.open("cphrasesp.txt", "w", "utf-8") as f: #création fichier où notre corpus va être écrit

    for fd in os.listdir(start):
        if os.path.isfile(os.path.join(start,fd)):
            files.append(os.path.join(start,fd))

    for file in files:
        print(file + "\n") #va ajouter le nom de chaque fichier qui va etre annalysé dans la console
        with codecs.open(file, "r", "utf8") as fi: # ouvir le fichier et
            document = fi.read() # le lire en entier

        bs = BeautifulSoup(document, features='xml') #lit le fichier en arbre xml, sans les intentations

        tours = bs.findAll("tour") #va trouver tous les éléments "tour"

        for t in tours:
            for elt in t.find_all(["rire", "repetition", "lang", "souffle", "reprise", "amorce", "incomprehensible", "inspiration", "sifflement", "begaiement", "toux", "tousse", "chuchotement"]):
                elt.extract() #extrait les disfluences énumérées ci-dessus
            mot = t.find_all("motBDL")
            if "nbMots" in t.attrs and len(mot) > 3: #va garder les phrases qui ont plus de 3 mots
                phrase = t.get_text(" ", strip=True)
                if phrase.strip() != "":
                    f.write(phrase + "\n") #va écrire dans le fichier de corpus,les phrases qui ont été sélectionnées

print("Le corpus a été crée dans un fichier texte appelé 'cphrasesp.txt', regardes dans ton dossier")

with codecs.open("cphrasesp.txt", "r", "UTF8") as temp:  #ouvrir le fichier texte test pour le lire, UTF8 = représenter les caractères en particulier, variable temp prépare la lecture 
    corpupuce = temp.readlines() #lire le document ligne par ligne 

contraction = r"[jldstcm]"  #6,7,8 ex d'expressions régulières, toutes les lettres qui sont concernées par les contractions 
voyelle = r"[aàeéèëêâiïîhoôöuùüûy]"  #variable voyelle liste qui définit un caractère, un parmi ceux qui sont énuméré
consonne = r"[^aàeéèëêâiïîhoôöuùüûy]" #^ signfiie la négation 

    # liste de mots à supprimer: à compléter si besoin
exclus = ["euh", "ben", "ouais", "teh", "beh", "oh", "ah bon", "ah", "eh", "hein", "bah","hm", "bon", "ohlala" ]  #

with codecs.open("phrasespropre.txt", "w", "utf-8") as fincorpus:
    for t in corpupuce:
        if 'incompréhensible' not in t:
            t = t.strip()
            # grouper ' avec les mots autour
            t = re.sub(r" ([-']) ", r"\1", t)
            # grouper - avec les mots autour
            #t = re.sub(r" - ", r"-", t)
            # ajouter e elidé devant une consonne
            t = re.sub(r"(\b"+contraction+r")'("+consonne+r")", r"\g<1>e \g<2>", t)
            # découper le texte en mots
            mots = t.split()
            ligne = [] # créer la liste finale de mots
            for mot in mots:
                # si le mot n'est pas exclus et ne se termine pas par
                if not (mot in exclus or mot.endswith("/")):
                    # ajouter le mot à la liste ligne
                    ligne.append(mot)
            # convertir la liste en texte
            t = ' '.join(ligne)
            # supprimer les mots répetés: attention à la notation de groupes dans regex!
            t = re.sub(r"(\s\w+)\1", r"\1", t)
            # si le texte a plus qu'un caractère ou n'est pas vide
            if len(t) > 0:
                # afficher-le
                fincorpus.write(t + "\n")

print("Le corpus a été crée dans un fichier texte appelé 'phrasespropre.txt', regardes dans ton dossier") 


