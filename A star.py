# AMIR Abderrahmane
# 171731073307
# M1 IV
from tkinter import *
import numpy as np

app = Tk()

app.title("A Star 8 Puzzel")
app.minsize(725, 745)
app.maxsize(725, 745)

canvas = Canvas(app, width=725, height=745)

nbr_colonnes = 3
nbr_lignes = 3

# On affiche la gris de base
for i in range(nbr_colonnes): #colonnes
    for j in range(nbr_lignes): #lignes
        label1 = Label(app, width="20", height="16", bg="#ee9b00", bd=3, relief=RIDGE)
        label1.grid(row=j, column=i)

# On affiche la gris pour les boutons
for i in range(3, 7): #colonnes
    for j in range(0, 3): #lignes
        label1 = Label(app, width="10", height="10")
        label1.grid(row=j, column=i)

global matrice
matrice = np.zeros((3, 3))
matrice = matrice.astype(int)
global s
global n0
global index

n0 = [1, 2, 3, 8, 0, 4, 7, 6, 5]
index = -1
# s = [1, 2, 3, 8, 0, 4, 7, 6, 5]
# s = [3, 4, 7, 5, 0, 8, 1, 2, 6]
# s = [1, 2, 4, 7, 8, 3, 0, 5, 6]
# s = [1, 2, 3, 5, 8, 6, 0, 4, 7]
s = [3, 8, 4, 0, 6, 2, 1, 7, 5]
k = 0
for i in range(3):
    for j in range(3):
        matrice[i][j] = s[k]
        k = k + 1

# Affichage de la matrice initial
for i in range(3):
    for j in range(3):
        if(matrice[i][j] == 0):
            label1 = Label(app, text="  ", font=("Helvetica", 40), bg="#ee9b00", fg="#7209b7")
            label1.grid(row=i, column=j)
        else:
            label1 = Label(app, text=matrice[i][j], font=("Helvetica", 40), bg="#ee9b00", fg="#7209b7")
            label1.grid(row=i, column=j)


# Bouton de recherche
stat_search_button = Button(app, text="Start search", font=("Helvetica", 20),  bg="#ee9b00", fg="white", command=lambda:aStar(n0))
stat_search_button.grid(row=1, column=4)

# Bouton d'affichage du path
stat_search_button = Button(app, text="Next step", font=("Helvetica", 20),  bg="#ee9b00", fg="white", command=lambda:move_astar())
stat_search_button.grid(row=2, column=4)


# Fonction qui génere les successeurs
def succ(s, cls):
    list = []
    j = 0
    trouve = False
    mat = s[0]
    l = len(mat)
    temp1 = []
    temp2 = []
    temp3 = []
    temp4 = []
    k = 0
    while k < l:
        temp1.append(mat[k])
        temp2.append(mat[k])
        temp3.append(mat[k])
        temp4.append(mat[k])
        k = k + 1

    l = len(mat)
    while j < l and not trouve:
        if mat[j] == 0:
            if (j != 0 and j != 1 and j != 2):  # haut
                t = mat[j - 3]
                temp3[j - 3] = mat[j]
                temp3[j] = t
                list.append(temp3)

            if (j != 6 and j != 7 and j != 8):  # bas
                t = mat[j + 3]
                temp4[j + 3] = mat[j]
                temp4[j] = t
                list.append(temp4)

            if (j != 0 and j != 3 and j != 6):  # gauche
                t = mat[j - 1]
                temp1[j - 1] = mat[j]
                temp1[j] = t
                list.append(temp1)

            if (j != 2 and j != 5 and j != 8):  # droite
                t = mat[j + 1]
                temp2[j + 1] = mat[j]
                temp2[j] = t
                list.append(temp2)

            trouve = True
        j = j + 1
        x = 0

        #enlever les successeurs qui existent dans CLOSED
        while x < (len(list)):
            z = 0
            exist = False
            while (z < len(cls) and not exist):
                if list[x] == cls[z][0]:
                    exist = True
                    list.pop(x)
                z = z + 1
            if(not exist):
                x = x + 1
    return list


# Fonction qui calcule l'heuristique
def heuristique(s, n0):
    h = 0
    l = len(s)
    for i in range(l):
        if s[i] != 0:
            if s[i] != n0[i]:
                h = h + 1
    return h


# Fonction qui retourn l'état avec un f minimum
def minimum(s):
    f = s[0][1] + s[0][2]
    min_s = s[0][0]
    min_h = s[0][1]
    min_g = s[0][2]
    l = len(s)
    for i in range(1, l):
        if s[i][1] + s[i][2] < f:
            min_g = s[i][2]
            min_s = s[i][0]
            min_h = s[i][1]
            f = s[i][1] + s[i][2]
    list_min_succ = []
    for i in range(l):
        if s[i][1] + s[i][2] == f:
            list_min_succ.append((s[i][0], s[i][1], s[i][2]))

    return list_min_succ


# Fonction de l'algorithme A*
def aStar(n0):
    s = []
    for i in range(len(matrice)):
        for j in range(len(matrice)):
            s.append(matrice[i][j])
    print("Etat initial\n", matrice)

    open = []
    closed = []
    succ_s = []
    succ_sh = []
    list_min_s = []
    found = False
    final_node = []
    parents = {}
    j = 0
    # print("n0", n0)
    if (s == n0):
        print("Trouvé !\n")
        label1 = Label(app, text="Found !", font=("Helvetica", 40), fg="green")
        label1.grid(row=0, column=4)
        found = True
    else:
        h = heuristique(s, n0)
        op = (s, h, 0)  # initialement g = 0
        open.append(op)
        x = len(s)
        while (open and not found):
            list_min_s = minimum(open)
            min = list_min_s.pop()
            print("noeud min", min)
            i = 0
            while i < len(open):  # recherche du min dans open
                k = (open[i][0], open[i][1], open[i][2])
                if (k == min):
                    j = i
                    i = len(open)
                i = i + 1
            # print("poped", open[j])
            open.pop(j)  # pop le min du open
            closed.append(min)  # add min to closed

            if (min[0] == n0):
                print("Trouvé !!\n")
                label1 = Label(app, text="Found !", font=("Helvetica", 40), fg="green")
                label1.grid(row=0, column=4)
                found = True
                final_node = min[0]
                break
            else:
                # print("succ min", succ(min))
                if (succ(min, closed)):  # calcul des sucssesseurs du min
                    succ_s = succ(min, closed)
                    # print("succ_s", succ_s)
                    succ_sh = []
                    for i in succ_s:  # calcule de H pour chaque succ
                        h = heuristique(i, n0)
                        op = (i, h, min[2] + 1)
                        succ_sh.append(op)

                    for i in succ_sh:  # associer a chaque succ son parent
                        parents[str(i[0])] = str(min[0])

                        if i[0] == n0:
                            print("Trouvé !!!")
                            label1 = Label(app, text="Found !", font=("Helvetica", 40), fg="green")
                            label1.grid(row=0, column=4)
                            found = True
                            final_node = i[0]
                            break
                    # print("les succ", succ_sh)

                    x = 0
                    while x < (len(succ_sh)):
                        z = 0
                        exist = False
                        while (z < len(open) and not exist):
                            if succ_sh[x][0] == open[z][0]:
                                exist = True
                                saved_z = z
                            z = z + 1

                        if (not exist):  # si le succ n'est pas dans open
                            # print("add succ to open", succ_sh[x])
                            exist = False
                            n = 0
                            #vérifier si succ est dans COSED ou pas
                            while (n < len(closed) and not exist):
                                if succ_sh[x][0] == closed[n][0]:
                                    exist = True
                                    saved_n = n
                                n = n + 1
                            if (not exist): #si succ n'est pas dans OPEN et CLOSED
                                open.append(succ_sh[x])  # mettre le succ dans open

                        else:  # si le succ est dans open
                            if ((open[saved_z][1] + open[saved_z][2]) > (succ_sh[x][1] + succ_sh[x][2])):  # si f du nv succ < au succ dans open
                                open.pop(saved_z)  # pop le succ
                                open.append(succ_sh[x])  # add le nv succ avec un f plus petit
                                parents[str(open[saved_z][0])] = str(min[0])  # MAJ du parent du nv succ
                            else:
                                if ((open[saved_z][1] + open[saved_z][2]) == (succ_sh[x][1] + succ_sh[x][2])): # si ils ont le mm f
                                    if (open[saved_z][1] > succ_sh[x][1]): #prendre celui avec un h minimum
                                        open.pop(saved_z)  # pop le succ
                                        open.append(succ_sh[x])  # add le nv succ avec un f plus petit
                                        parents[str(open[saved_z][0])] = str(min[0])  # MAJ du parent du nv succ
                        x = x + 1

                    exist = False
                    m = 0
                    while m < (len(succ_sh)):
                        n = 0
                        while (n < len(closed) and not exist):
                            if succ_sh[m][0] == closed[n][0]:
                                exist = True
                                saved_n = n
                            n = n + 1
                        if (exist):  # si succ est dans closed
                            if ((closed[saved_n][1] + closed[saved_n][2]) > (succ_sh[m][1] + succ_sh[m][2])):
                                closed.pop(saved_n)
                                open.append(closed[saved_n])
                                parents[str(closed[saved_n][0])] = str(min[0])
                            else:
                                if ((closed[saved_n][1] + closed[saved_n][2]) == (succ_sh[m][1] + succ_sh[m][2])):
                                    if (closed[saved_n][1] > succ_sh[x][1]):
                                        closed.pop(saved_n)
                                        open.append(succ_sh[m])
                                        parents[str(closed[saved_n][0])] = min[0]
                        m = m + 1

            print("open", open)
            print("closed", (closed))

        if (found):
            lien = []
            fn = final_node
            lien.append(fn)
            c = 0
            while final_node != str(s):
                for cle, val in parents.items():
                    if cle == str(final_node):
                        lien.append(val)
                        final_node = val
                        break

            chemin = lien[::-1]
            cpt = 0
            for x in chemin:
                print(x)
                cpt += 1
            print("Noeuds visités", len(closed))
            print("Nombre de déplacement:", cpt-1)

            global k_list_list
            k_list_list = []
            for k in chemin:
                k_list = []
                for d in range(len(k)):
                    if (k[d] == '1' or k[d] == '2' or k[d] == '3' or k[d] == '4' or k[d] == '5' or k[d] == '6' or k[d] == '7' or k[d] == '8' or k[d] == '0'):
                        k_list.append(int(k[d]))
                k_list_list.append(k_list)

            final = []
            final = chemin.pop()
            k_list_list.append(final)


# Fonction qui s'execute à chaque clique du bouton (Next step) et qui affiche les états du path pour retrouver l'état initial
def move_astar():
    global index
    index = index + 1

    if (index < len(k_list_list)):
        i = 0
        j = 0
        for x in k_list_list[index]:
            if (x == 0):
                label1 = Label(app, text="  ", font=("Helvetica", 40), bg="#ee9b00", fg="#7209b7")
                label1.grid(row=i, column=j)
            else:
                label1 = Label(app, text=int(x), font=("Helvetica", 40), bg="#ee9b00", fg="#7209b7")
                label1.grid(row=i, column=j)
            if (j < 2):
                j = j + 1
            else:
                i = i + 1
                j = 0


# Fonction qui permet les deplacements dans la gris pour faire le mélange du départ
def move(event):
    find = False
    i = 0
    coord_vide = ()
    voisins = []
    while i < 3 and not find:
        j = 0
        while j < 3 and not find:
            if matrice[i][j] == 0.0:
                coord_vide = (i, j)
                find = True
            else:
                j = j + 1
        i = i + 1

    gauche = (coord_vide[0], coord_vide[1] - 1)
    droite = (coord_vide[0], coord_vide[1] + 1)
    haut = (coord_vide[0] - 1, coord_vide[1])
    bas = (coord_vide[0] + 1, coord_vide[1])

    if (haut[0] >= 0 and haut[0] <= 3 and haut[1] >= 0 and haut[1] <= 3):
        voisins.append(haut)
    if (bas[0] >= 0 and bas[0] <= 3 and bas[1] >= 0 and bas[1] <= 3):
        voisins.append(bas)
    if (gauche[0] >= 0 and gauche[0] <= 3 and gauche[1] >= 0 and gauche[1] <= 3):
        voisins.append(gauche)
    if (droite[0] >= 0 and droite[0] <= 3 and droite[1] >= 0 and droite[1] <= 3):
        voisins.append(droite)

    i = 0
    coord_value = ()
    find = False
    while i < 3 and not find:
        j = 0
        while j < 3 and not find:
            if matrice[i][j] == int(event.char):
                coord_value = (i, j)
                find = True
                break
            else:
                j = j + 1
        i = i + 1

    if (coord_value in voisins):
        matrice[coord_vide[0]][coord_vide[1]] = int(event.char)
        matrice[coord_value[0]][coord_value[1]] = 0

        # Déplacer la valeur vers la case vide
        label1 = Label(app, text=int(event.char), font=("Helvetica", 40),  bg="#ee9b00", fg="#7209b7")
        label1.grid(row=coord_vide[0], column=coord_vide[1])
        # La case vide devient l'encinne case de la valeur choisi
        label2 = Label(app, text="  ", font=("Helvetica", 40),  bg="#ee9b00", fg="#7209b7")
        label2.grid(row=coord_value[0], column=coord_value[1])


app.bind('<Any-KeyPress>', move)


app.mainloop()