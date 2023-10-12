import numpy as np
from Constantes import *
import Equadif as eq


## Fonction de dichotomie servant à détecter quand la balle arrive au niveau du but ou d'un objet

def dichoto(coord, vect, axe):
    coordRel=vect[:,axe]-coord
    a=0
    b=len(vect)-1
    if b==a:    return (vect[:,0][b],vect[:,2][b], b)    # Tableau avec un seul élément
    while b!=a+1:
        c=int((a+b)/2)
        if coordRel[a]*coordRel[c]>0:
            a=c
        else :
            b=c
    if abs(coordRel[a])>abs(coordRel[b]):
        return(vect[:,0][b],vect[:,2][b], b) #position de la balle selon x et y lorsqu'elle est au niveau de l'objet selon l'axe spécifié
    else:
        return(vect[:,0][a], vect[:,2][a], a)

## Fonction regroupant toute les collisions sauf celles avec le sol

def collisions(x0, z0, vect, alphaxz, angleBalle):
    ## Avec le mur
    zRelMur=-9.15
    angleRelCoord=-np.arctan(vect[:,0][1:]/vect[:,4][1:])*180/np.pi+angleBalle # Angle du changement de repère, donc angle entre l'axe z (du monde 3D) et l'axe balle-centre du but
    vectRelMur=np.copy(vect)    # Copie du vecteur initial, qui va servir de vecteur dans le nouveau repère

    vectRelMur[:,4][1:]=-np.sqrt(vect[:,4][1:]**2+vect[:,0][1:]**2)*np.cos(angleRelCoord[:]*np.pi/180)  # Changement de repère suivant z (le Mur est orienté dans l'axe balle-but)
    vectRelMur[:,0][1:]=np.sqrt(vect[:,4][1:]**2+vect[:,0][1:]**2)*np.sin(angleRelCoord[:]*np.pi/180)   # Changement de repère suivant x
    xRelMur, yRelMur, iMur=dichoto(zRelMur, vectRelMur, AXE_Z)

    if vectRelMur[:,4][iMur] - zRelMur < 20/FPS and yRelMur < 1.75 and xRelMur >= -1 and xRelMur <= 1:  # Condition de collision
        vectRelMur[:,4][iMur]=zRelMur+RAYON_BALLE
        vectRelMur[:,4][iMur:]-=(1+COEFF_REBOND_SURFACE)*(vectRelMur[:,4][iMur:]-vectRelMur[:,4][iMur]) # Rebond suivant z du nouveau repère

        nalpha=np.zeros(len(vectRelMur[:,4][iMur:]))
        for i in range(iMur, iMur + len(nalpha)):   # Angle du retour dans l'ancien repère
            nalpha[i-iMur]=signstrict(vectRelMur[:,0][i])*np.arccos(-vectRelMur[:,4][i]/np.sqrt(vectRelMur[:,0][i]**2 + vectRelMur[:,4][i]**2))*180/np.pi

        vect[:,4][iMur:]=-np.sqrt(vectRelMur[:,4][iMur:]**2+vectRelMur[:,0][iMur:]**2)*np.cos((nalpha-angleBalle)*np.pi/180) #Calcul des nouvelles coordonnées dans l'ancien repère
        vect[:,0][iMur:]=np.sqrt(vectRelMur[:,4][iMur:]**2+vectRelMur[:,0][iMur:]**2)*np.sin((nalpha-angleBalle)*np.pi/180) # Suivant x
        return RATE

    ## Avec la partie du filet du haut du but
    zBut=-25-z0+RAYON_BALLE
    xBut, yBut, iBut = dichoto(zBut, vect, AXE_Z)
    vectRelBut=vect[iBut:]
    yFilet=2.34
    xFileth, yFileth, iFileth=dichoto(yFilet, vectRelBut, AXE_Y)
    iFileth+=iBut

    if vect[:,3][iFileth] < 0 and vect[:,0][iFileth]+x0 > -3.66 and vect[:,0][iFileth]+x0 < 3.66 and vect[:,4][iFileth]+z0 > -27 and vect[:,4][iFileth]+z0 < -25+2*RAYON_POTEAUX+2*RAYON_BALLE:
        vect[:,3][iFileth]*=-COEFF_REBOND_SOL
        nvect0 = vect[iFileth]
        vect[iFileth:]=eq.euler(eq.fvitesse, nvect0, eq.t)[:len(vect)-iFileth]  # On est obligé de recalculer la nouvelle trajectoire

    ## Avec la partie du filet à gauche du but
    xFiletg=-3.66-x0
    xFiletg, yFiletg, iFletg=dichoto(xFiletg, vect, AXE_X)
    if vect[:,4][iFletg] > -27-z0-(vect[:,4][iFletg-1]-vect[:,4][iFletg]) and vect[:,4][iFletg] < -25-z0+2*RAYON_POTEAUX+RAYON_BALLE and yFiletg < 2.44:
        if vect[:,1][iFletg] < 0:
            vect[:,0][iFletg]=xFiletg
        vect[:,4][iFletg:]=vect[:,4][iFletg] + COEFF_REBOND_FILET*(vect[:,4][iFletg:]-vect[:,4][iFletg])
        vect[:,0][iFletg:]=vect[:,0][iFletg] - COEFF_REBOND_FILET*(vect[:,0][iFletg:]-vect[:,0][iFletg])

    ## Avec la partie du filet à droite du but
    xFiletd=3.66-x0
    xFiletd, yFiletd, iFletd=dichoto(xFiletd, vect, AXE_X)
    if vect[:,4][iFletd] > -27-z0-(vect[:,4][iFletd-1]-vect[:,4][iFletd]) and vect[:,4][iFletd] < -25-z0+2*RAYON_POTEAUX+RAYON_BALLE and yFiletd < 2.44:
        if vect[:,1][iFletg] > 0:
            vect[:,0][iFletd]=xFiletd
        vect[:,4][iFletd:]=vect[:,4][iFletd] + COEFF_REBOND_FILET*(vect[:,4][iFletd:]-vect[:,4][iFletd])
        vect[:,0][iFletd:]=vect[:,0][iFletd] - COEFF_REBOND_FILET*(vect[:,0][iFletd:]-vect[:,0][iFletd])

    ## Avec la partie du filet au fond du but
    zFiletf=-27-z0+RAYON_BALLE                  # Filet du fond
    xFiletf, yFiletf, iFletf=dichoto(zFiletf, vect, AXE_Z)
    if vect[:,4][iFletf]-zFiletf < 20/FPS and  yFiletf < 2.34 and xFiletf+x0 > -3.66-abs(vect[:,0][iFletf-1]-vect[:,0][iFletf]) and xFiletf+x0 < 3.66+abs(vect[:,0][iFletf-1]-vect[:,0][iFletf]):
        vect[:,4][iFletf]=-27-z0+RAYON_BALLE
        vect[:,4][iFletf:]-=(vect[:,4][iFletf:]-vect[:,4][iFletf])
        vect[:,0][iFletf:]-=(vect[:,0][iFletf:]-vect[:,0][iFletf])

    ## Avec l'enclos (muret du fond)
    zEnclos=-50-z0
    xEnclos, yEnclos, iEnclos=dichoto(zEnclos, vect, AXE_Z)
    if abs(vect[:,4][iEnclos]-zEnclos) < 20/FPS and yEnclos < 1.9 and xEnclos > -50 and xEnclos < 50:
        vect[:,4][iEnclos:]-=(1+COEFF_REBOND_SURFACE)*(vect[:,4][iEnclos:]-vect[:,4][iEnclos])

    di=len(vect)-1
    if vect[:,4][di]-zBut<0 and vect[:,4][di]-zBut>=-2 and vect[:,0][di]>=-3.66-x0 and vect[:,0][di]<=3.66-x0 and vect[:,2][di]<2.44:
        return BUT

    return RATE

def signstrict(a):
    if a<0:
        return -1
    return 1
