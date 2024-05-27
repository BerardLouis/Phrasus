from tkinter import *
from tkinter.messagebox import *
import codecs
import random

### -> Extraction des Phrases et Création des éléments nécéssaires au jeu <- ####
def initialisation():

    global liste_cat_gramm,decompte_essai,liste_propositions,liste_cat_phrase,liste_lemme,nb_essai,deviner,gr
    fichier = "selection.txt" ##lire le fichier avec les phrases annotées choisies
    nb_essai = 7 #Nombre de tentatives autorisées
    liste_cat_gramm = ["ADV" , "INTJ" , "PRON" , "VERB" , "ADJ" , "NOUN" , "CCONJ" , "ADP" , "SCONJ" , "AUX" , "DET" , "NUM" , "PROPN" , "PUNC"]
    decompte_essai = 0
    liste_propositions = []
    with codecs.open(fichier,"r", "utf8") as fscript:
        doc = fscript.readlines()

    phrases = [] ##créer une liste de toutes les phrases
    phrase = {} 
    liste_cat_phrase = []
    liste_lemme = []
    for line in doc:
        line =line.strip() 
        if line != "": # si la ligne n'est pas vide, ajouter le mot dans le dictionnaire "phrase"
            segms= line.split("\t")
            nr = segms[0] # numéro
            word = segms[1] # forme
            cat = segms[3] # catégorie
            phrase[nr] = (word,cat) 
        else: #si la ligne vide, c'est que la phrase suivante commence    
            phrases.append(phrase) # ajouter la phrase terminée à la liste de phrases
            phrase = {} # reinitialiser le dictionnaire de la phrase pour le reremplir avec la phrase suivante

    deviner = random.choice(list(phrases)) #choisir une phrase au hasard
    for i in range(len(deviner)): #Création d'une liste contenant les catégories grammaticales de la phrase
        liste_cat_phrase.append(deviner[str(i+1)][1])
        liste_lemme.append(deviner[str(i+1)][0])
     
    gr = [] ## préparer la grille : un mot par colonne
    for r in range(nb_essai): #On crée autant de ligne qu'il y a d'essais, il faudrait mettre "-1" car on ne compte pas l'éssai numéro 0, mais on doit rajouter une ligne pour les lemmes tout en bas de la grille
        rw = [] #lorsqu'on commence une nouvelle ligne, on reinitialise les infos pour
        for c in range(len(deviner)):
            rw.append("_")
        gr.append(rw)

    window() #Une fois qu'on à défini toutes les variables nécéssaires au jeu, on lance la fonction qui initialise la fenêtre


#Définition de la commande lancé par le bouton langue de chat
def languedechat ():
    global decompte_essai
    showinfo('AH!', "Vous avez donné votre langue au chat. FINITO !!\n\nLa réponse était :\n" + " ".join(liste_lemme).upper() +"\n"+" ".join(liste_cat_phrase).upper()+" \n\nVous avez 0 points!")
    root.destroy() #On ferme la fenêtre actuelle
    initialisation() #On relance une partie


# définir la grille
def make_grid(grille): #On aurait pu définir ces informations directement dans window(), mais comme c'est un élément graphique à part et complexe, nous avons choisi de l'isoler dans sa propre fonction

    root.columnconfigure(0, weight=1)
    root.columnconfigure(len(grille[0])+2, weight=1) #On crée deux colonnes en plus, placées tout à droite et à gauche, qui permettent de centrer la grille horizontalement

    largeur = len(max(grille, key=len))*2 #On ajuste la taille des cellules en fonction de la taille du mot le plus long

    for k in range(len(grille)): 
        for i in range(len(grille[k])):
            if "_" in grille[k][i]: #Si l'élément de la liste des réponse à l'index demandé est " _ " c'est qu'une reponse n'a pas encore été proposée pour cette case, donc elle est vide
                    Label(root, text=''.upper(), width=largeur,
                    height=2, bg="grey", anchor=CENTER).grid(row=k,column=i+1, padx=2,pady=2)

            elif grille[k][i].isupper(): #Si l'élément de la liste à cet index est composé de lettre, c'est qu'une réponse à été proposée

                if grille[k][i]==liste_cat_phrase[i] : #Si la catégorie est à la bonne place
                    label0 =Label(root, text=grille[k][i].upper(), width=largeur,height=2, bg="Green", anchor=CENTER)
                    label0.grid(row=k,column=i+1, padx=2,pady=2)#On affiche la réponse en vert
                    label1 =Label(root, text=liste_lemme[i].upper(), width=largeur,height=2, bg="White", anchor=CENTER)
                    label1.grid(row=len(grille),column=i+1, padx=2,pady=2)#On affiche le lemme en bas de la grille
               
                elif grille[k][i] in liste_cat_phrase:#Si la catégorie est dans la phrase
                    Label(root, text=grille[k][i].upper(), width=largeur,
                    height=2, bg="Yellow", anchor=CENTER).grid(row=k,column=i+1, padx=2,pady=2) #On affiche la réponse en jaune

                else :#Sinon, c'est que la catégorie n'est pas dans la phrase
                    Label(root, text=grille[k][i].upper(), width=largeur,
                      height=2, bg="Grey", anchor=CENTER).grid(row=k,column=i+1, sticky="n", padx=2,pady=2)#On affiche la réponse en gris
                    
    root.update()#On relance la création de la fenêtre


#définir réponse en lien avec l'action du bouton
def reponseSimple():
    global gr, deviner, decompte_essai, nb_essai, liste_cat_gramm, liste_propositions

    X = champ.get().upper()  # Recupération de la proposition du joueur puis l'afficher dans la grille en majuscule.
    champ.delete(0,END) #suppression du texte présent dans la boîte de dialogue

    decompte_essai+=1 #On rajoute un essai au décompte
    if decompte_essai == nb_essai : #Si la personne a utilisé tout ses essai: on calcule son score
        score = 0
        cat_verte=0
        cat_jaune=0 #Avant de calculer le score, on reinitialise les variables
        for i in range(len(X.split())):
            if X.split()[i] == liste_cat_gramm[i]:
                score+=2
                cat_verte+=1 #Pour chaque catégorie bien placée, on ajoute 2 points
            elif X.split()[i] in liste_cat_gramm:
                score+=1
                cat_jaune+=1 #Pour chaque catégorie mal placée, on ajoute 1 point

        showinfo("Dommage !","Il n'y a plus d'essais..\n\nLa réponse était " + str(liste_lemme) + "! \n\nVous avez "+str(score)+" points!\n\n"
                 +str(cat_verte)+" catégories bien placées pour "+str(cat_verte*2)+" points !\n"
                 +str(cat_jaune)+" catégories mal placées pour "+str(cat_jaune)+"points !")
        root.destroy() #fermer la fenetre
 
    if len(deviner) != len(X.split()) or any(item not in liste_cat_gramm for item in X.split()) :  # Si la proposition n'est pas de la bonne longueur ou contient un élément qui n'est pas une catégories valide
        gr[decompte_essai-1] = "X"*len(deviner) #On remplace la ligne de la grille par des X
        showinfo("Erreur", "Tu n'as pas proposé le bon nombre de catégories et/ou tu as écrit un chiffre\nRecommence")
        make_grid(gr)
        Label2.config(text =" Quelles catégories proposez-vous?\nEcrivez-les:\n(N'oubliez pas les espaces)")
        root.update()

    elif X.split() in liste_propositions : #Si la personne a déjà fait cette proposition:
        gr[decompte_essai-1] = "X"*len(deviner)  #On remplace la ligne de la grille par des X
        showinfo("Erreur","Tu as déjà entré cette proposition !")
        make_grid(gr)
        Label2.config(text =" Quelles catégories proposez-vous?\nEcrivez-les:\n(N'oubliez pas les espaces)")
        root.update()

    else: #Si la réponse a passé les tests précédents, c'est quelle est valide
        liste_propositions.append(X.split()) #On garde en mémoire la réponse qui vient d'être faite
        gr[decompte_essai-1] = X.split()  # Mise à jour de la grille.
        make_grid(gr)
        if X == ' '.join(liste_cat_phrase):  # Si la proposition du joueur est identique à la réponse.
            showinfo('Bien joué!', "'Tu as trouvé la bonne réponse :) !\nIl restait encore "+str(nb_essai-decompte_essai)+" essais !'")
            root.destroy()  # Fermeture de la fenêtre, le jeu est terminé.

### -> Interface Graphique <- ####
def window():
    global root,champ,Label2
    root = Tk() # initier la fenêtre principale

    ## champ de saisie
    champ = Entry(root,show='', bg ='white', fg='black')
    champ.place(relx=0.5, rely=0.9, x=10, anchor=CENTER)

    # zone de texte de proposition
    Label2 = Label(root, text = "Quelles catégories voulez-vous proposer?\n(Ecrivez-les en ajoutant des espaces)\n Il y a " + str(len(deviner)) + " catégories",
                font=("calibri","12","bold"), fg="White", bg="grey")
    Label2.place(relx=0.5, rely=0.80, x=10, anchor=CENTER)

    ## bouton validation de réponse
    Bouton = Button(root, text ='Valider', width=8, height=2, fg="black", font="bold", command=reponseSimple)
    Bouton.place(x=50, rely=0.75, anchor=W)
        
    ##bouton langue de chat
    Blanguedechat = Button(root, text ='Langue au chat', width=12, height=2, fg="black", font="bold", command = languedechat)
    Blanguedechat.place(x=50, rely=0.85, anchor=W)

    #zone de texte qui va présenter les catégories qui peuvent être utilisées: 
    Label3 = Label(root, text = "Catégories acceptées:\nADJ (adjectif)\n ADV (adverbe)\n ADP (préposition)\n INTJ (interjection) \n AUX (auxiliaire)\n CCONJ (conjonction coord)\n SCONJ (conjonction sub)\n NOUN (nom)\n PROPN (nom propre)\n PRON (pronom)\n VERB (verbe)\n DET (déterminant)\n NUM (numéral)",
                font=("calibri","11","bold"), fg="White", bg="grey")
    Label3.place(relx=0.85, rely=0.70, anchor=CENTER)

    #zone de texte en bas du jeu
    Label4 = Label(root, text = "Game made by Clémence BEGAY, Louisa BENNADJEMA, Romane HAMON et Louis BÉRARD",
                font=("calibri","11","bold"), fg="White", bg="grey")
    Label4.place(relx=0.5, rely=0.95, anchor=CENTER)

    BRejouer = Button(root, text="Rejouer", width=8, height=2, fg="black", font="bold", command=lambda:[root.destroy(),initialisation()])
    BRejouer.place(x=50, rely=0.65,anchor=W)

    make_grid(gr) #Une fois toutes les infos de la fenêtre définies, on lance la fonction qui crée la grille avant de créer la fenêtre.

    root.title('Phrasus et bouche cousue') # titre de la fenêtre
    root.minsize(800, 650) #taille de la fenêtre
    root.configure(background='grey19') #couleur du fond
    root.resizable(False,False) #la fenêtre s'adapte à la taile de la grille automatiquement, changer la taille de la fenêtre de décentrer les éléments
    root.mainloop() # boucle pour actualiser la fenêtre

initialisation()