import pygame
import pygame.freetype
import numpy as np
from random import randint
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Constantes import *

##  Initialisation des textures

def initAffichage():
    global murTexture, balleTexture, herbeTexture, filetTexture, angleBalle, enclosTexture
    angleBalle=0 # angle de rotation du ballon en fonction du temps
    murTexture=lire_texture("Mannequin_mur.png")
    balleTexture=lire_texture("balle_texture.png")
    herbeTexture=lire_texture("texture_herbe.png")
    filetTexture=lire_texture("texture_filet.png")
    enclosTexture=lire_texture("texture_enclos.png")

## Fonctions d'affichage

def dessinerMarquage(x,y,z):
    glEnable(GL_POLYGON_SMOOTH) # Anticrénelage nécessaire pour le marquage
    glPushMatrix()  # On enregistre la matrice 3D avant de se déplacer dans le monde
    glColor3f(1.0,1.0,1.0)  # On choisit une couleur pour afficher le marquage
    glTranslatef(-x,-y,-z-DISTANCE_CAMERA_BALLON)   # On se déplace aux coordonnées du ballon
    glBegin(GL_QUADS)   # Initialisation de l'affichage de quadrilatères
    for vert in MARQUAGE_COORDONNEES:
        glVertex3fv(vert)   # On lie les vertices avec glvertex3fv
    glEnd()
    glPopMatrix()   # On charge la matrice enregistrée plus haut pour revenir à la position initiale, car on s'est déplacé pour afficher le marquage aux coordonnées voulues
    glDisable(GL_POLYGON_SMOOTH)    # On enlève l'anti-crénelage qui peut causer des bugs avec les textures

def dessinerFleche(alphaxzc, alphayc, v0):
    glPushMatrix()
    glTranslatef(0,-0.090,-DISTANCE_CAMERA_BALLON)
    glRotatef(alphaxzc, 0,-1,0) # Rotation sur le plan horizontal
    glRotatef(alphayc, 1,0,0)   # Rotation sur le plan vertical
    glColor3f((v0-10)/20,1-(v0-10)/20,0) # La couleur change en fonction de la vitesse (vert->rouge)

    for i in range(int(v0//10+1)):   # Boucle pour afficher une fleche qui grandit avec la vitesse initiale
        if i!=0 and i!=v0//10:
            glTranslatef(0,0,-10)
        elif i!=0:
            glTranslatef(0,0,-(v0%10))
        glBegin(GL_QUADS)
        for vert in FLECHE_COORDONNEES_TRONC:
            glVertex3fv(vert)   # On lie les vertices
        glEnd()

    glBegin(GL_TRIANGLES)   # On veut dessiner un triangle : la tête de la flèche

    for vert in FLECHE_COORDONNEES_TETE: # Affichage de la tête
        glVertex3fv(vert)
    glEnd()
    glPopMatrix()

def dessinerBalle(x,y,z,w):
    global angleBalle # On récupère l'angle du ballon initialisé au début
    glPushMatrix()
    glTranslatef(x,y,z-DISTANCE_CAMERA_BALLON)
    angleBalle+=w/FPS*180/np.pi # On augmente l'angle en fonction de la vitesse de rotation et du framerate
    glRotatef(angleBalle,0,1,0)

    glEnable(GL_TEXTURE_2D)  # On veut appliquer une texture (2D) sur la balle

    sphere = gluNewQuadric()    #
    glColor3f(1,1,1)
    gluQuadricDrawStyle(sphere, GLU_FILL)
    glBindTexture(GL_TEXTURE_2D, balleTexture)  # On choisit la texture 2D : texture de la balle


    gluQuadricTexture(sphere, GL_TRUE)
    gluSphere(sphere,0.1, 32, 32)   # Dessine la sphère

    glDisable(GL_TEXTURE_2D)

    glPopMatrix()

def dessinerSol(x,y,z):
    glPushMatrix()
    glTranslatef(-x,-y,-z-DISTANCE_CAMERA_BALLON)
    glColor3f(1,1,1)
    glEnable(GL_TEXTURE_2D)     # Affichage de l'herbe, avec les mêmes fonctions que plus haut
    glBindTexture(GL_TEXTURE_2D, herbeTexture)
    glBegin(GL_QUADS)
    glTexCoord2f(50,50)
    glVertex3fv(SOL_COORDONNEES[0])
    glTexCoord2f(50,0)
    glVertex3fv(SOL_COORDONNEES[1])
    glTexCoord2f(0,0)
    glVertex3fv(SOL_COORDONNEES[2])
    glTexCoord2f(0,50)
    glVertex3fv(SOL_COORDONNEES[3])
    glEnd()
    glDisable(GL_TEXTURE_2D)

    glEnable(GL_TEXTURE_2D)     # Affichage de l'enclos
    glBindTexture(GL_TEXTURE_2D, enclosTexture)
    glBegin(GL_QUADS)
    glTexCoord2f(0,0)
    glVertex3fv(ENCLOS_COORDONNEES[0])
    glTexCoord2f(25,0)
    glVertex3fv(ENCLOS_COORDONNEES[1])
    glTexCoord2f(25,0.5)
    glVertex3fv(ENCLOS_COORDONNEES[2])
    glTexCoord2f(0,0.5)
    glVertex3fv(ENCLOS_COORDONNEES[3])
    glTexCoord2f(0,0)
    glVertex3fv(ENCLOS_COORDONNEES[4])
    glTexCoord2f(25,0)
    glVertex3fv(ENCLOS_COORDONNEES[5])
    glTexCoord2f(25,0.5)
    glVertex3fv(ENCLOS_COORDONNEES[6])
    glTexCoord2f(0,0.5)
    glVertex3fv(ENCLOS_COORDONNEES[7])
    glTexCoord2f(0,0)
    glVertex3fv(ENCLOS_COORDONNEES[8])
    glTexCoord2f(25,0)
    glVertex3fv(ENCLOS_COORDONNEES[9])
    glTexCoord2f(25,0.5)
    glVertex3fv(ENCLOS_COORDONNEES[10])
    glTexCoord2f(0,0.5)
    glVertex3fv(ENCLOS_COORDONNEES[11])
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def dessinerBut(x,y,z):
    poteaux = gluNewQuadric()
    glColor3f(1.0,1.0,1.0)

    glPushMatrix()  # Poteau de droite
    glTranslatef(3.66-x,-y-0.1,-25-z-DISTANCE_CAMERA_BALLON+0.05)
    glRotatef(-90,1,0,0)
    gluCylinder(poteaux,0.05,0.05,2.44,32,32)
    glPopMatrix()

    glPushMatrix()  # Poteau de gauche
    glTranslatef(-3.66-x,-y-0.1,-25-z-DISTANCE_CAMERA_BALLON+0.05)
    glRotatef(-90,1,0,0)
    gluCylinder(poteaux,0.05,0.05,2.44,32,32)
    glPopMatrix()

    glPushMatrix()  # Barre transversale
    glTranslatef(3.71-x,2.44-y-0.1,-25-z-DISTANCE_CAMERA_BALLON+0.05)
    glRotatef(-90,0,1,0)
    gluCylinder(poteaux,0.05,0.05,7.42,32,32)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-x,-y-0.1,-z-25-DISTANCE_CAMERA_BALLON+0.05)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)  # On veut que la texture appliquée au filet ait un filtre de transparence (pour pouvoir voir entre les mailles du filet)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   # On choisit la fonction OpenGL de transparence
    glBindTexture(GL_TEXTURE_2D, filetTexture)
    glBegin(GL_QUADS)

    glTexCoord2f(0,0)   # Rectangle supérieur
    glVertex3fv(FILET_COORDONNEES[0])
    glTexCoord2f(4.5,0)
    glVertex3fv(FILET_COORDONNEES[1])
    glTexCoord2f(4.5,1.2)
    glVertex3fv(FILET_COORDONNEES[2])
    glTexCoord2f(0,1.2)
    glVertex3fv(FILET_COORDONNEES[3])

    glTexCoord2f(0,0)   # Rectangle du fond
    glVertex3fv(FILET_COORDONNEES[2])
    glTexCoord2f(4.5,0)
    glVertex3fv(FILET_COORDONNEES[3])
    glTexCoord2f(4.5,1.5)
    glVertex3fv(FILET_COORDONNEES[4])
    glTexCoord2f(0,1.5)
    glVertex3fv(FILET_COORDONNEES[5])

    glTexCoord2f(0,0)   # rectangle de droite
    glVertex3fv(FILET_COORDONNEES[1])
    glTexCoord2f(1.2,0)
    glVertex3fv(FILET_COORDONNEES[2])
    glTexCoord2f(1.2,1.5)
    glVertex3fv(FILET_COORDONNEES[5])
    glTexCoord2f(0,1.5)
    glVertex3fv(FILET_COORDONNEES[6])

    glTexCoord2f(0,0)   # rectangle de gauche
    glVertex3fv(FILET_COORDONNEES[0])
    glTexCoord2f(1.2,0)
    glVertex3fv(FILET_COORDONNEES[3])
    glTexCoord2f(1.2,1.5)
    glVertex3fv(FILET_COORDONNEES[4])
    glTexCoord2f(0,1.5)
    glVertex3fv(FILET_COORDONNEES[7])

    glEnd()
    glDisable(GL_BLEND) # On enlève le filtre alpha
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def dessinerMur(angleCam,x,y,z):
    glPushMatrix()

    glColor3f(1.0,1.0,1.0)
    glTranslatef(0,0,-DISTANCE_CAMERA_BALLON)
    glRotatef(angleCam,0,1,0)   # On effectue une rotation de l'angle de la camera pour que le mur soit orienté face au ballon
    glTranslatef(0,0,-9.15) # On recule de 9.15 m par rapport au ballon (cf énoncé)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)   # Transparence
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   # Fonction de transparence
    glBindTexture(GL_TEXTURE_2D, murTexture)
    glBegin(GL_QUADS)

    glTexCoord2f(-2,0) # Rectangle du mur
    glVertex3fv(MUR_COORDONNEES[0])
    glTexCoord2f(2,0)
    glVertex3fv(MUR_COORDONNEES[1])
    glTexCoord2f(2,1)
    glVertex3fv(MUR_COORDONNEES[2])
    glTexCoord2f(-2,1)
    glVertex3fv(MUR_COORDONNEES[3])

    glEnd()
    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)

    glPopMatrix()


def dessinerTexte(x, y, text, r, g, b):
    glPushMatrix()
    font = pygame.font.Font(None, 64)
    textSurface = font.render(text, True, (r,g,b,255),(0,0,0,0))

    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2i(int(x-textSurface.get_width()/2),int(y- textSurface.get_height()/2))    # Centrer le texte sur la position (x,y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),GL_RGBA, GL_UNSIGNED_BYTE, textData)
    glPopMatrix()


def afficherSkybox():
    t = 100.0   # Distance em mètres des faces du cube formant la skybox (cubemap) par rapport à la caméra
    glEnable(GL_TEXTURE_CUBE_MAP)   # Texture spéciale : cubemap (gérée par OpenGL)
    glBindTexture(GL_TEXTURE_CUBE_MAP, texid)

    glPushMatrix()
    glTranslatef(0,5,0) # On élève la skybox pour ne pas voir que le ciel
    glRotate(-90, 0,1,0)    # Rotation de 90° pour se mettre dans l'angle de vision de la caméra

    # Pour alléger les calculs, on ne dessine que trois faces de la skybox qui correspondent aux faces qui sont dans le champ de vision de la caméra : z négatif, x positif, et z positif, qui se transforment après la rotation de 90° (voir plus haut) en x négatif, z négatif et x positif

    glBegin(GL_TRIANGLE_STRIP)  # Pour dessiner la skybox (ou cubemap)
    glTexCoord3f(-t,t,t)    # face x négatif
    glVertex3f(-t,-t,-t)
    glTexCoord3f(-t,-t,t)
    glVertex3f(-t,t,-t)
    glTexCoord3f(-t,t,-t)
    glVertex3f(-t,-t,t)
    glTexCoord3f(-t,-t,-t)
    glVertex3f(-t,t,t)
    glEnd()

    glBegin(GL_TRIANGLE_STRIP)  # Face z négatif
    glTexCoord3f(t,t,-t)
    glVertex3f(-t,-t,-t)
    glTexCoord3f(-t,t,-t)
    glVertex3f(t,-t,-t)
    glTexCoord3f(t, -t,-t)
    glVertex3f(-t,t,-t)
    glTexCoord3f(-t,-t,-t)
    glVertex3f(t,t,-t)
    glEnd()

    glBegin(GL_TRIANGLE_STRIP)  # face z positif
    glTexCoord3f(t,t,t)
    glVertex3f(-t,-t,t)
    glTexCoord3f(t,-t,t)
    glVertex3f(-t,t,t)
    glTexCoord3f(-t,t,t)
    glVertex3f(t,-t,t)
    glTexCoord3f(-t,-t,t)
    glVertex3f(t,t,t)
    glEnd()

    glPopMatrix()

    glDisable(GL_TEXTURE_CUBE_MAP)

## Fonctions de chargement des textures (texture = image appliquée sur une surface OpenGL)

def lire_texture(nomFichier):
    textureSurface = pygame.image.load(nomFichier)  # Charger l'image
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)  # Convertir l'image en texte (pour OpenGL)

    texid = glGenTextures(1)    # Génère une texture avec OpenGL

    glBindTexture(GL_TEXTURE_2D, texid) # On lie la texture qui vient d'être créée pour lui appliquer les transformations plus bas

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)    # Fonction permettant de répéter la texture sur l'axe s si on lui donne des coordonnées > 1
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)    # Répéter la texture sur l'axe t
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) # Méthode d'interpolation de la texture : GL_NEAREST = pixel le plus proche des coordonnées 2D (réduction)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)   # Grossissement
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData) # crée une image 2D en combinant l'image et la texture

    return texid

def initialiserSkyBox():
    global texid
    textureImage=(pygame.image.load("negx.jpg"), pygame.image.load("negz.jpg"), pygame.image.load("posz.jpg"))  # Charger les trois textures entrant dans le champ de vision

    # Convertir les images en texte
    textureData = (pygame.image.tostring(textureImage[0], "RGBA", 1), pygame.image.tostring(textureImage[1], "RGBA", 1), pygame.image.tostring(textureImage[2], "RGBA", 1))

    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_CUBE_MAP, texid)   # On lie la nouvelle texture à une texture de type cubemap

    # Créér une image pour chaque face de la skybox (on est obligé d'initialiser les quatre faces dont on ne se sert pas)
    glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_X, 0, GL_RGBA, textureImage[0].get_width(), textureImage[0].get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData[0])
    glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X, 0, GL_RGBA, textureImage[1].get_width(), textureImage[1].get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData[1])
    glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_Y, 0, GL_RGBA, textureImage[1].get_width(), textureImage[1].get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData[1])
    glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_Y, 0, GL_RGBA, textureImage[1].get_width(), textureImage[1].get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData[1])
    glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_Z, 0, GL_RGBA, textureImage[1].get_width(), textureImage[1].get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData[1])
    glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_Z, 0, GL_RGBA, textureImage[2].get_width(), textureImage[2].get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData[2])

    # Initialiser les paramètres des textures de la skybox
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP)

