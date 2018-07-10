import pygame
import basic

#scritte e
#variabili bottoni
#           X    Y     larghez.  scritta    colore scritta,   colore sfondo     stacco
BottoneS = [(250,500), (100, 50), "START", basic.BLUE,          basic.RED,         [20,13]]
BottoneE = [(300,650 ), (100, 50), "ESCI", basic.BLACK,         basic.VERDE_ACQUA, [20,13]]
BottoneE_menu = [(50,500 ), (100, 50), "ESCI", basic.BLACK,     basic.RED,         [20,13]]
Bottone_exit = [(487, 50), (50,55)]
Bottone_musicaON = [(450,500 ), (110, 50), "musica ON", basic.BLUE,  basic.GREY,    [5,13]]
Bottone_musicaOF = [(450,500 ), (110, 50), "musica OF", basic.BLUE,  basic.GREY,    [5,13]]

# funzione riquadro con all'interno una scritta
def scritta(skin, surface):
    """
    renderize the widgets
    :param skin: what would be renderized on the screen (position,color etc...)
    :param surface: where the widgets will be renderized
    """
    posizione = skin[0]
    larghezza = skin[1]
    testo = skin[2]
    colore_sfondo = skin[4]
    stacco = skin[5]
    pygame.draw.rect(surface, colore_sfondo, [posizione[0], posizione[1], larghezza[0], larghezza[1]])
    Bfont = pygame.font.SysFont('Calibri', larghezza[1] / 2, True, False)
    scritta = Bfont.render(testo, True, skin[3])
    surface.blit(scritta, (posizione[0] + stacco[0], posizione[1] + stacco[1]))


# controllo se la posizione del "click" rientra nei contorni del quadrato
def check_click(bottone, PosizClic):
    """
    check if the mouse clicked the widgets
    :param bottone: which botton you want to check
    :param PosizClic: the position of the click
    :return:
    """
    #bottone [0][0/1] sono posizione x e y del bottone
    if PosizClic[0] >= bottone[0][0] and PosizClic[0] <= bottone[0][0] + bottone[1][0] and PosizClic[1] >= \
            bottone[0][1] and PosizClic[1] <= bottone[0][1] + bottone[1][1]:
        return True
    else:
        return False
#menu



