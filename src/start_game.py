import os,pygame

from pygame import (K_DOWN, K_LEFT, K_RETURN,
                    K_RIGHT, K_SPACE, K_UP, K_l, K_x, K_z,K_e)

import worlds_setup,basic
import widgets,random,sys
from isomyr.config import Keys
from custom import Super_engine,Win

import time
print "starting game..."
time.sleep(2)




dirname = os.path.dirname(__file__)
pygame.init()

#in-game settings and music
music = True
menu_music = "custom_stuff/musica_menu.mp3"
game_music = "custom_stuff/ultimate_game_song.mp3"


#while cicle and menu
play = True
menu = True
gandalf = pygame.USEREVENT +2
pygame.time.set_timer(gandalf,1000)
pos_gandalf = (random.randint(10,400),300)
bottone_musica = widgets.Bottone_musicaON
info_render = True
info = pygame.image.load("custom_stuff/comandi.png")

pygame.mixer.music.load("custom_stuff/musica_menu.mp3")
pygame.mixer.music.play(-1)

#other screen option
my_screen = pygame.display.set_mode((600,600))#pygame.Surface((300,600))
menu_sfondo = pygame.image.load("custom_stuff/gandalf_funny.png")
posizClic = (0,0)

# Set the custom keys for the game.
customKeys = Keys(
    left=K_LEFT,
    right=K_RIGHT,
    up=K_UP,
    down=K_DOWN,
    jump=K_SPACE,
    pick_up=K_z,
    drop=K_x,
    examine=K_l,
    using=K_RETURN)


# An image loader that lets us run the tutorial anywhere the isomyr library
# can be imported (i.e., you don"t have to be in the same directory as the
# tutorial to run it).
#imageLoader = ImageLoader(basedir=dirname, transparency=(255, 255, 255))





def run():
    # Create an isomyr engine and start it.
    titlebar = os.path.join(dirname, "titlebar.png")
    engine = Super_engine(keys=customKeys, displayOffset=[200, 172],
                          sceneSize=(600, 800), titleFile=titlebar,
                          textAreaPosition=(10, 380), textAreaSize=(380, 230))

    world = worlds_setup.setupWorld(engine)
    engine.setStartingWorld(world, welcomeMessage="benvenuti alla demo del MICHELANGELO GAME!")
    engine.run()

while play:
    while not menu:
        run()

    while menu:
        Pmouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                posizClic = Pmouse
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == gandalf:
                pos_gandalf =(random.randint(10,400),random.randint(30,400))
        #RENDER
        if not info_render:
            my_screen.blit(menu_sfondo,pos_gandalf)
            widgets.scritta(widgets.BottoneS, my_screen)
            widgets.scritta(widgets.BottoneE_menu, my_screen)
            clicked_exit = widgets.check_click(widgets.BottoneE_menu, posizClic)
            clicked_start = widgets.check_click(widgets.BottoneS,posizClic)
            clicked_music = widgets.check_click(widgets.Bottone_musicaON,posizClic)
            # check button
            if clicked_start:
                menu = False
                pygame.mixer.music.stop()
                if music:
                    pygame.mixer.music.load(game_music)
                    pygame.mixer.music.play(-1)
                posizClic = (0,0)
            if clicked_exit:
                sys.exit()
            if clicked_music:
                if music:
                    music = False
                    pygame.mixer.music.stop()
                    bottone_musica = widgets.Bottone_musicaOF
                else:
                    music = True
                    pygame.mixer.music.load(menu_music)
                    pygame.mixer.music.play(-1)
                    bottone_musica = widgets.Bottone_musicaON
                posizClic = (0,0)
            widgets.scritta(bottone_musica,my_screen)

        else:
            my_screen.blit(info, (50,50))
            if widgets.check_click(widgets.Bottone_exit,posizClic):
                info_render = False
                my_screen.fill(basic.BLUE)
        pygame.display.flip()