import pygame, widgets, os, sys,basic
from isomyr.objects.character import Player
from isomyr.thing import FallableThing,PortableThing
from isomyr.objects.portal import Portal
from isomyr.util.loaders import ImageLoader
from isomyr.event import PlayerTouchPortalEvent, notify

dirname = os.path.dirname(__file__)
imageLoader = ImageLoader(basedir=dirname, transparency=(255, 255, 255))

#events

take_key = pygame.USEREVENT + 5
touch_portal = pygame.USEREVENT + 6


class Win:
    """
    class for "credits staff" when you win the game
    """
    def __init__(self,milliseconds,image, music= None):
        self.start_event = pygame.USEREVENT + 3
        self.exit_event = pygame.USEREVENT + 4
        self.mill = milliseconds
        self.sfondo = image
        self.exit = False
        self.music = music

    def start(self):
        """
        make events starts and play epic music
        :return:
        """
        pygame.time.set_timer(self.start_event, self.mill)
        pygame.time.set_timer(self.exit_event, (self.mill*2)+ self.mill/2)
        if self.music != None:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)

    def credits(self):
        """
        credits menu' cicle
        :return:
        """
        esc = False
        self.screen = pygame.display.set_mode((700, 700))
        self.cicle = True
        posizClic = (0,0)
        sfondox,sfondoy = 20,0
        move_y = 0
        exit = False

        #credits main cicle
        while self.cicle:
            #upgrade mouse position
            Pmouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posizClic = Pmouse
                if event.type == self.exit_event:
                    exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        move_y = -15
                    if event.key == pygame.K_UP:
                        move_y = 15
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                        move_y = 0

            # RENDER
            self.screen.fill(basic.BLACK)
            sfondoy += move_y
            self.screen.blit(self.sfondo,(sfondox,sfondoy))
            #if event "exit_event" is passed
            if exit:
                widgets.scritta(widgets.BottoneE, self.screen)
                esc = widgets.check_click(widgets.BottoneE, posizClic)
            # check button
            if esc:
                sys.exit()
            pygame.display.flip()



win = Win(4000,pygame.image.load("custom_stuff/credits_videogame.png"),music="custom_stuff/Soviet union.mp3")

class Talking_NPC(FallableThing):
    """
    an actor that (if examineted) can do something, like talking or dropping items...
    """

    def __init__(self,*args,**kwds):
        super(Talking_NPC, self).__init__(*args, **kwds)
        self.view = None
        self.examinating = False
        self.player_touching = False
        self.talk_text = ""

    def set_view(self,new_view):
        self.view = new_view

    def set_text(self, new_text):
        self.talk_text = new_text
        self.speach = "%s dice--> %s" %(self.name, self.talk_text)

    def eventCollision(self, otherObject, impactSide):
        """
        Redefined collision event handler for falling and touching.
        """
        # When colliding with something on the z axis while falling is on
        if self.view != None:
            if isinstance(otherObject,Super_jumpino_player):
                self.view.updateTextArea(self.speach)



class Super_jumpino_player(Player):
    """
    player class with variable jump_height
    """
    def __init__(self, jump_height, *args, **kwds):
        super(Super_jumpino_player, self).__init__(*args, **kwds)
        self.jump_height = jump_height

    def jump(self):
        """Action for the actor to jump."""
        if self.falling is False:
            # Give some altitude (z-direction).
            self.velocity[2] = self.velocity[2] + self.jump_height
            self.falling = True

class Locked_portal(Portal):
    """
    locked portal class with an "unlock object"
    """
    def __init__(self,toScene=None, toLocation=None, *args, **kwds):
        super(Locked_portal, self).__init__(toScene, toLocation, *args, **kwds)
        # Build the skinned key obj


    def set_view(self,view):
        """
        setting portal text view
        :param view:
        """
        self.view = view
    #def modifiy(self):
    def eventTouch(self, impact, otherObject, impactSide):
        """
        modified touch function with "starting" event
        """
        for event in pygame.event.get():

            if isinstance(otherObject, Player):
                if event.type == take_key:
                    notify(PlayerTouchPortalEvent(otherObject, self))
                    win.start()
                    self.view.updateTextArea("____")
                    self.view.updateTextArea("si prega di perdonare i problema con il teletrasporto")
                    self.view.updateTextArea("____")
                else:
                    self.view.updateTextArea("ti serve una chiave!")

class Win_thing(PortableThing):
    def request_pick_up(self, avatar):
        self.carrier = avatar
        self.pickedup = True
        pygame.time.set_timer(take_key,1)
        return(True)
