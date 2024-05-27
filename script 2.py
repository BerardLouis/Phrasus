import codecs # module pour gérer l'encodage
fichier = "txtpropre.conllu" # fichier annoté avec UDPipe
with codecs.open(fichier,"r","utf-8") as f: #ouvir le fichier pour la lecture
    texte = f.readlines() # lire ligne par ligne
phrases = [] # liste des phrases
ph = []  # liste des lignes d'une phrase
for line in texte: # pour chaque ligne du document annoté 
    line = line.strip() # supprimer les blancs
    if len(line) > 0 and not line.startswith("#"): # si la ligne non-vide et ne commence pas par #
        # l.11-14: bonus1
        cols = line.split("\t")
        if cols[3] == "AUX" and cols[7] in ["cop", "aux:caus"]:
            cols[3] = "VERB"
        line = "\t".join(cols)
        ph.append(line) # ajouter la ligne à la liste
    elif len(line) == 0: # autrement si la ligne vide
        phrases.append(ph)  # ajouter la phrase à la liste
        ph = []  # commencer la nouvelle phrase

# liste des phrases sélectionnées
selection = []
for P in phrases:  # pour chaque phrase
    # limiter la taille des phrases à analyser
    if len(P) > 3 and len(P) < 10: 
        verbal = False
        # BONUS2: variable prep + l.33-36 + condition prep l.41
        prep = False
        # pour chaque ligne (=mot) de la phrase
        for line in P:
            # couper la ligne en colonnes
            cols = line.split("\t")
            # si il y a des prépositions contractées, ignorer la phrase
            if "-" in cols[0]:
                prep = True
                # on n'analyse plus d'autres lignes (=mots) de la phrase
                break 
            # si le verbe est l'élement principal       # s'il est conjugué
            if cols[3] == "VERB" and cols[7] == "root": # and "VerbForm=Fin" in cols[5]: # si la racine de la phrase est un verbe (conjugué)
                verbal = True
        # s'il n'y a pas de prépositions contractées, le verbe principal est conjugué
        if verbal == True and prep == False:
            # si le dernier mot n'est pas un déterminant ou conjonction
            if not P[-1].split("\t")[3] in ["DET", "CCONJ", "SCONJ"]:
                # ajouter la phrase à la liste
                selection.append(P)

# sauvegarder les phrases dans un fichier
with codecs.open("selection.txt", "w", 'utf8') as h: 
    for s in selection:
        # ligne par ligne
        for l in s:
            h.write(l+"\n")
        # ligne vide pour séparer les phrases
        h.write("\n")
        
print("Le fichier avec les phrases séléctionnées pour le jeu à été crée")
