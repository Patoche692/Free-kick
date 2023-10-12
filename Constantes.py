 ## CONSTANTES


alpha=5e-3 # coeff de frottements
g=9.81 # m.s^-2
m=0.420 # masse de la balle
M=5e-3  # coefficient de l'effet de la balle, lié aux caractéristiques de la balle
FPS=60  # FPS
DISTANCE_CAMERA_BALLON = 2.5 # Distance entre le point de vue du joueur et la ballon en mètres
RAYON_POTEAUX=0.05
RAYON_BALLE=0.1
COEFF_F_SOL=0.99
COEFF_REBOND_SOL=0.6
COEFF_REBOND_SURFACE=0.6
COEFF_REBOND_FILET=0.2

BUT=True
RATE=False

AXE_X=0
AXE_Y=2
AXE_Z=4

## COORDONNEES DES OBJETS DANS L'ESPACE 3D

SOL_COORDONNEES = (     # coordonnées du terrain (herbe)
    (50, -0.1, 50), (50, -0.1, -50),
    (-50, -0.1, -50), (-50, -0.1, 50))

ENCLOS_COORDONNEES = (      # coordonnees de l'enclos
    (-50, -0.1, -50), (50, -0.1, -50),
    (50, 1.9, -50), (-50, 1.9, -50),
    (-50, -0.1, 50), (-50, -0.1, -50),
    (-50, 1.9, -50), (-50, 1.9, 50),
    (50, -0.1, 50), (50, -0.1, -50),
    (50, 1.9, -50), (50, 1.9, 50))

MUR_COORDONNEES = (     # coordonnees des joueurs
    (-1,-0.1,0), (1,-0.1,0),
    (1,1.75,0), (-1,1.75,0)
    )

FILET_COORDONNEES = (       # coordonnées du filet
    (-3.66,2.34,-0.05),(3.66,2.34,-0.05),
    (3.66,2.34,-2), (-3.66,2.34,-2),
    (-3.66,-0.1,-2), (3.66,-0.1,-2),
    (3.66,-0.1,-0.05), (-3.66,-0.1,-0.05))

FLECHE_COORDONNEES_TRONC = (   # tronc de la fleche
    (-0.05,0,0),(0.05,0,0),
    (0.05,0,-10),(-0.05,0,-10)
    )
FLECHE_COORDONNEES_TETE = (     # tete de la fleche
    (-0.3,0,-10),(0.3,0,-10),(0,0,-15)
    )
MARQUAGE_COORDONNEES = (    # lignes blanches du terrain
    (-34,-0.095,-25), (34,-0.095,-25),
    (34,-0.095,-25+0.2), (-34,-0.095,-25+0.2),

    (-34,-0.095,-25), (-34,-0.095,80),
    (-34+0.2,-0.095,80), (-34+0.2,-0.095,-25),

    (34,-0.095,-25), (34,-0.095,80),
    (34-0.2,-0.095,80), (34-0.2,-0.095,-25),

    (-20.15,-0.095,-25), (-20.15,-0.095,-8.5),
    (-20.15+0.2,-0.095,-8.5), (-20.15+0.2,-0.095,-25),

    (20.15,-0.095,-25), (20.15,-0.095,-8.5),
    (20.15-0.2,-0.095,-8.5), (20.15-0.2,-0.095,-25),

    (-20.15,-0.095,-8.5), (20.15,-0.095,-8.5),
    (20.15,-0.095,-8.5-0.2), (-20.15,-0.095,-8.5-0.2),

    (-9.16,-0.095,-25), (-9.16,-0.095,-19.5),
    (-9.16+0.2,-0.095,-19.5), (-9.16+0.2,-0.095,-25),

    (9.16,-0.095,-25), (9.16,-0.095,-19.5),
    (9.16-0.2,-0.095,-19.5), (9.16-0.2,-0.095,-25),

    (-9.16,-0.095,-19.5), (9.16,-0.095,-19.5),
    (9.16,-0.095,-19.5-0.2), (-9.16,-0.095,-19.5-0.2))