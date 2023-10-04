# -*- coding: utf-8 -*-

import pyxel
import random
import time
from random import*

pyxel.init(1200, 690, title="Snake by NaokiP and MaximeR")

DEBUG = False
jeu = {"dir_prov": "up",
       "direction": "up",
       "compteur": 0,     
       "perso_x": 600,
       "perso_y": 330,
       "pomme_x_possible": [k for k in range(0,1200,30)],
       "pomme_y_possible": [k for k in range(0,690,30)],
       "pomme_x": 0,
       "pomme_y": 0,
       "long_serp": 1,
       "past_position": [(600,330)],
       "tete_dir": {"up": 0,
                    "down": 30,
                    "right": 60,
                    "left": 90},
       "chiffre": [(40, 32),(0, 16),(10, 16),(20, 16),(30, 16),(40, 16),(0, 32),(10, 32),(20, 32),(30, 32)],
       "live": True}

jeu["pomme_x"], jeu["pomme_y"] = jeu["pomme_x_possible"][randint(0,39)], jeu["pomme_y_possible"][randint(0,22)]

pyxel.load("images.pyxres")

def direction_change(dir, dir_ref):
    """
    permet de changer la direction du serpent selon
    la valeur d'une directioon réference.
    
    """
    if pyxel.btn(pyxel.KEY_RIGHT):
        if dir_ref != 'left':
            return 'right'
    if pyxel.btn(pyxel.KEY_LEFT):
        if dir_ref != 'right':
            return 'left'
    if pyxel.btn(pyxel.KEY_DOWN):
        if dir_ref != 'up':
            return 'down'
    if pyxel.btn(pyxel.KEY_UP):
        if dir_ref != 'down':
            return 'up'
    return dir



def perso_deplacement(dir,x, y):
    """
    change la valeur de x est y qui correspondent à des coordonné
    selon la direction défini.
    
    """
    if dir == "right":
        if (x < 1170) :
            x = x + 30
        else:
            jeu["live"] = False
    if dir == "left":
        if (x > 0) :
            x = x - 30
        else:
            jeu["live"] = False
    if dir == "down":
        if (y < 660) :
            y = y + 30
        else:
            jeu["live"] = False
    if dir == "up":
        if (y > 0) :
            y = y - 30
        else:
            jeu["live"] = False
    return x, y



def pomme():
    """
    programme pour les actions de la pommes
    
    """
    if jeu["pomme_x"] == jeu["perso_x"] and jeu["pomme_y"] == jeu["perso_y"]:
        jeu["long_serp"] += 1
        jeu["pomme_x"], jeu["pomme_y"] = jeu["pomme_x_possible"][randint(0,39)],  jeu["pomme_y_possible"][randint(0,22)]




def decalage_tab(tab):
    """
    décale les valeurs de tab en écrasant la dernière valeur sauf si
    la longueur du serpent a augmenté.
    
    """
    if len(tab) < jeu["long_serp"]:
        tab.append(tab[len(tab)-1])
    for k in range(len(tab)-1,0,-1):
        tab[k] = tab[k-1]
    
       


def draw():
    """
    
    dessine l'écran du jeu.
    
    """
    pyxel.cls(0)
    
    if jeu["live"] == True:
        pyxel.blt(10, 10, 1, 0, 0, 54, 16)
        pyxel.blt(74, 10, 1, jeu["chiffre"][jeu["long_serp"]//100][0], jeu["chiffre"][jeu["long_serp"]//100][1], 10, 16)
        pyxel.blt(84, 10, 1, jeu["chiffre"][jeu["long_serp"]//10%10][0], jeu["chiffre"][jeu["long_serp"]//10%10][1], 10, 16)
        pyxel.blt(94, 10, 1, jeu["chiffre"][jeu["long_serp"]%10][0], jeu["chiffre"][jeu["long_serp"]%10][1], 10, 16)
        pyxel.blt(jeu["perso_x"], jeu["perso_y"], 0, 30, jeu["tete_dir"][jeu["direction"]], 30, 30)
        pyxel.blt(jeu["pomme_x"], jeu["pomme_y"], 0, 0, 0, 30, 30)
        for k in range(len(jeu["past_position"])):
            pyxel.blt(jeu["past_position"][k][0], jeu["past_position"][k][1], 0, 60, 30, 30, 30)
    else:
        pyxel.blt(400, 240, 2, 0, 0,192, 64)
        pyxel.blt(612, 240, 2, 0, 64,192, 64)
        pyxel.blt(550, 350, 1, 0, 0, 54, 16)
        pyxel.blt(614, 350, 1, jeu["chiffre"][jeu["long_serp"]//100][0], jeu["chiffre"][jeu["long_serp"]//100][1], 10, 16)
        pyxel.blt(624, 350, 1, jeu["chiffre"][jeu["long_serp"]//10%10][0], jeu["chiffre"][jeu["long_serp"]//10%10][1], 10, 16)
        pyxel.blt(634, 350, 1, jeu["chiffre"][jeu["long_serp"]%10][0], jeu["chiffre"][jeu["long_serp"]%10][1], 10, 16)


def lifecheck():
    """
    vérifie la colision entre la tete du serpent et sa queue.
    
    """
    for k in range(len(jeu["past_position"])):
        if jeu["past_position"][k] == (jeu["perso_x"], jeu["perso_y"]):
            jeu["live"] = False
                
        

def update():
    """
    permet le déroulement du jeu.
    
    """
    jeu["compteur"] += 1
    pomme()
    jeu["dir_prov"] = direction_change(jeu["dir_prov"], jeu["direction"])
    if jeu["compteur"] % 2 == 0:#augmenter le "2" si la difficulté est trop élevé lors du test
        jeu["direction"] = jeu["dir_prov"]
        decalage_tab(jeu["past_position"])
        jeu["past_position"][0] = (jeu["perso_x"], jeu["perso_y"])
        jeu["perso_x"], jeu["perso_y"] = perso_deplacement(jeu["direction"],jeu["perso_x"], jeu["perso_y"])
        lifecheck()
    if DEBUG:
        print(jeu["dir_prov"], jeu["direction"])


pyxel.run(update, draw)