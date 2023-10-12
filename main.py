import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

import Equadif as eq
from Affichage import *
from Dichotomie import *


## Fonction principale du jeu

def main():
    pygame.init()
    pygame.display.set_mode((0, 0), OPENGL|DOUBLEBUF)   # Crée une fenêtre OpenGL en plein écran, active le double buffering
    pygame.mixer.init()

    ballon= pygame.mixer.Sound("ballon_frappes.wav")
    siflet=pygame.mixer.Sound("siflet.wav")
    #bruit_fond=pygame.mixer.Sound("Bruit_fond.mp3")
    butson=pygame.mixer.Sound("but.wav")
    #hueeson=pygame.mixer.Sound("Huee.mp3")
    #bruit_fond.set_volume(0.3)

    glEnable(GL_DEPTH_TEST) # Permet d'éviter certaines erreurs d'affichage liées à la profonduer des objets dans l'espace 3D

    info=pygame.display.Info()
    gluPerspective(45.0,info.current_w/info.current_h,0.01,200.0)   # Initialise la matrice avec le champ de vision (45°), le ratio, la distance minimale visible et la distance maximale visible

    initAffichage() # Initialise les textures et les paramètres d'affichage
    initialiserSkyBox() # Textures de la skybox

    x0=randint(-10,10)  # Position initiale sur l'axe x de la balle
    z0=randint(-7,0)    # Position initiale sur l'axe z de la balle
    v0=15   # Norme de la vitesse initiale
    w=0     # Vitesse de rotation de la balle
    angleCam=np.arctan(x0/(25-np.abs(z0)))*180/np.pi    # Angle de la balle par rapport au centre du but
    alphaxzc=-angleCam # On oriente le tir vers le centre du but
    alphayc=0   # Angle sur le plpan vertical


    ## Animation du début
    #bruit_fond.play(loops=-1, maxtime=0, fade_ms=0)
    glPushMatrix()  # On enregistre la matrice 3D avant de se déplacer dans le monde
    # Rotation de 10° selon l'axe x par rapport au ballon, pour avoir une vue plus haute
    glTranslatef(0,0 ,-DISTANCE_CAMERA_BALLON)  # On se déplace dans le monde 3D vers les coordonnées du ballon
    glRotatef(10,1,0,0)     # Rotation de 10°
    glTranslatef(0,0 ,-(-DISTANCE_CAMERA_BALLON))   # On revient à la position initiale

    glTranslatef(-15, -5, -30) # On déplace le terrain à la position initiale de l'animation
    glTranslatef(0,0 ,-DISTANCE_CAMERA_BALLON)
    glRotatef(90,0,-1,0)  # rotation pour avoir une vue du terrain
    glTranslatef(0,0 ,-(-DISTANCE_CAMERA_BALLON))
    angle=0     # Angle de l'animation
    x,y,z=0,0,0 # Position dans l'espace 3D au cours de l'animation
    pygame.key.set_repeat(150, 50)
    clock=pygame.time.Clock()   # Horloge de pygame pour gérer les FPS
    for i in range(FPS):    # On veut que l'animation dure 1s
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)    # Réinitialiser la vue (nettoie le color buffer et le depth buffer)
        x+=30/FPS # On rapproche le terrain
        y+=5/FPS
        z-=15/FPS
        angle+=(90-angleCam)/FPS    # Angle de rotation du terrain

        glPushMatrix()
        glTranslatef(x,y,z)
        glTranslatef(0,0 ,-DISTANCE_CAMERA_BALLON)
        glRotatef(angle,0,1,0)
        glTranslatef(0,0 ,-(-DISTANCE_CAMERA_BALLON))

        # Affichage des éléments
        afficherSkybox()

        dessinerBalle(0,0,0,0)
        dessinerMarquage(x0,0,z0)
        dessinerSol(x0,0,z0)

        dessinerBut(x0,0,z0)
        dessinerMur(angleCam,x0,0,z0)
        glPopMatrix()


        pygame.display.flip() # Actualise l'affichage

        if i==0:
            pygame.time.delay(3000) # Attendre 1 seconde si passage dans la 1ère boucle

        clock.tick(FPS)     # Gestion des FPS par pygame
    glPopMatrix()   # On charge la matrice enregistrée plus haut pour revenir à la position initiale, car on s'est déplacé pour afficher les objets aux coordonnées voulues

    ## Le joueur choisit la vitesse et les angles initiaux du tir


    escape=False

    siflet.play()

    while not escape:
        glPushMatrix()
        glTranslatef(0,0 ,-DISTANCE_CAMERA_BALLON)
        glRotatef(10,1,0,0)  # Nouvelle rotation de 10° par rapport au ballon
        glRotatef(angleCam,0,-1,0)
        glTranslatef(0,0 ,-(-DISTANCE_CAMERA_BALLON))

        pygame.event.clear()    # Supprime les événements antérieurs
        choixParametres = True
        texteParams=["Choisissez l'angle de tir avec les flèches directionnelles,", "la vitesse initiale du tir avec + et -,",
                    "et la vitesse de rotation avec * et /", "Appuyez sur espace pour tirer"]
        clock=pygame.time.Clock()

        while choixParametres:
            event=pygame.event.poll()   # Gestion des événements avec pygame
            if event.type==KEYDOWN:
                if event.key==pygame.K_UP:
                    if alphayc < 60:
                        alphayc+=0.5
                elif event.key==pygame.K_DOWN:
                    if alphayc > 0:
                        alphayc-=0.5
                elif event.key==pygame.K_RIGHT:
                    if alphaxzc < -angleCam+90:
                        alphaxzc+=0.5
                elif event.key==pygame.K_LEFT:
                    if alphaxzc > -angleCam-90:
                        alphaxzc-=0.5
                elif event.key==pygame.K_KP_PLUS:
                    if v0<30:
                        v0+=1
                elif event.key==pygame.K_KP_MINUS:
                    if v0>10:
                        v0-=1
                elif event.key==pygame.K_KP_MULTIPLY:
                    if w < 60:
                        w+=2
                elif event.key==pygame.K_KP_DIVIDE:
                    if w > -60:
                        w-=2
                elif event.key==K_SPACE:
                    choixParametres=False
                elif event.key==K_ESCAPE:
                    escape=True
                    break


            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)    # Réinitialise l'affichage

            # Affichage des objets
            afficherSkybox()
            dessinerBalle(0,0,0,w)
            dessinerSol(x0,0,z0)
            dessinerMarquage(x0,0,z0)
            dessinerFleche(alphaxzc, alphayc, v0)

            dessinerBut(x0,0,z0)
            dessinerMur(angleCam,x0,0,z0)

            # for i in range(len(texteParams)):
            #     dessinerTexte(info.current_w/2, info.current_h/3-64*i, texteParams[i], 255, 255, 255)

            pygame.display.flip() # Actualise l'affichage

            clock.tick(FPS)

        if escape:  break

        ## Animation du tir

        v0+=randint(-5,5)/100*v0    # Variation de 5% de la norme de la vitesse initiale
        eq.init(0,0,0,v0,alphayc*np.pi/180, alphaxzc*np.pi/180, w) # Initialise l'équation avec les paramètres initiaux
        vect=eq.euler(eq.fvitesse, eq.vect0, eq.t)  # Résoud l'équation
        but=collisions(x0, z0, vect, alphaxzc, angleCam)

        zbut =-25-z0+2*RAYON_POTEAUX+RAYON_BALLE
        xfinal,yfinal,iBut = dichoto(zbut,vect,AXE_Z)
        x,y,z=vect[:,0],vect[:,2],vect[:,4] # On récupère la position du ballon en fonction du temps

        ballon.play()
        TI=pygame.time.get_ticks()  # Début du tir

        clock=pygame.time.Clock()
        for k in range(len(x)):
            event = pygame.event.poll()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                break

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            afficherSkybox()
            dessinerBalle(x[k],y[k] ,z[k], w)   # Affiche la balle avec les positions venant de la résolution de l'équation différentielle
            dessinerSol(x0,0,z0)
            dessinerMarquage(x0,0,z0)

            dessinerBut(x0,0,z0)
            dessinerMur(angleCam,x0,0,z0)

            if k>=iBut:
                texteBut=""
                if not but:
                    texteBut="RATÉ !"
                    #if k==iBut:
                        #hueeson.play()
                else:
                    texteBut="BUT !"
                    if k==iBut:
                        butson.play()
                dessinerTexte(info.current_w/2, info.current_h/4, texteBut, 255, 255, 255)

            pygame.display.flip()
            clock.tick(FPS)

        clock=pygame.time.Clock()

        if but:
            for k in range(len(x)):
                glPushMatrix()
                glTranslate(-x[k], -y[k], -z[k])
                glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

                afficherSkybox()
                dessinerBalle(x[k],y[k] ,z[k], w)   # Affiche la balle avec les positions venant de la résolution de l'équation différentielle
                dessinerSol(x0,0,z0)
                dessinerMarquage(x0,0,z0)

                dessinerBut(x0,0,z0)
                dessinerMur(angleCam,x0,0,z0)

                dessinerTexte(info.current_w/2, info.current_h/4, "Replay", 255, 0, 0)

                pygame.display.flip()
                clock.tick(FPS)
                glPopMatrix()
        glPopMatrix()

        x0=randint(-10,10)  # Position initiale sur l'axe x de la balle
        z0=randint(-7,0)    # Position initiale sur l'axe z de la balle
        v0=15   # Norme de la vitesse initiale
        w=0     # Vitesse de rotation de la balle
        angleCam=np.arctan(x0/(25-np.abs(z0)))*180/np.pi    # Angle de la balle par rapport au centre du but
        alphaxzc=-angleCam # On oriente le tir vers le centre du but
        alphayc=0   # Angle sur le plpan vertical

        TF=pygame.time.get_ticks()  # Fin du tir
        print("Durée du tir :", (TF-TI)/1000, "s")


    pygame.quit()

main()