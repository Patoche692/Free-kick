import numpy as np
from Constantes import *

t=np.linspace(0,2.5,int(FPS*2.5))

## Initialisation
def init(x0, y0, z0, v0, betay, betaxz, wc):    # Initialisation avec les vitesses et les différents angles initiaux
    global vect0, w
    vect0=[x0,v0*np.cos(betay)*np.sin(betaxz),y0,v0*np.sin(betay), z0, -v0*np.cos(betay)*np.cos(betaxz)]#cf formaules de trigo pour calculer les composantes de la vitesse initiale
    w=wc    # Vitesse de rotation du ballon

## Résolution

def fvitesse(vect, t):
    x=vect[0]       # Le vecteur contient les positions et les vitesses
    vx=vect[1]
    y=vect[2]
    vy=vect[3]
    z=vect[4]
    vz=vect[5]
    ax=(-alpha/m)*np.sqrt(vx**2+vy**2+vz**2)*vx+M*vz*w  # On calcule ensuite les accélérations sur les trois
    ay=(-alpha/m)*np.sqrt(vx**2+vy**2+vz**2)*vy-g       # axes en se servant de l'équation différentielle
    az=(-alpha/m)*np.sqrt(vx**2+vy**2+vz**2)*vz+M*vx*w
    return np.array([vx,ax,vy,ay,vz,az], float)      # On retourne la dérivée du vecteur en entrée

def euler(Phi, vect0, t):
    pas=t[len(t)-1]/(len(t)-1)
    vect=np.array([np.zeros(6, float) for j in range(len(t))])
    vect[0]=vect0
    for k in range(len(t)-1):
        vect[k+1]=vect[k]+pas*Phi(vect[k],t[k])     # Résolution de l'équation différentielle

        if vect[k+1][2]<=0:     # Gestion des collisions avec le sol, faite dans cette fonction car beaucoup plus difficile à gérer après
            vect[k+1][2]=0      # On met la position y à 0 (le ballon colle le sol)
            vect[k+1][1]*=COEFF_F_SOL   # On diminue les vitesses suivant z et x
            vect[k+1][5]*=COEFF_F_SOL
            vect[k+1][3]*=-COEFF_REBOND_SOL     # On inverse la vitesse suivant y avec un coefficient
            if vect[k+1][3]<0.6+1.0*(100-FPS)/90:    # Vitesse suivant y très faible, on arrête la balle
                vect[k+1][3]=0
            if np.sqrt(vect[k+1][1]**2+vect[k+1][5]**2) < 1:    # Vitesse horizontale très faible, on arrête la balle
                vect[k+1][1]=0
                vect[k+1][5]=0

    return vect