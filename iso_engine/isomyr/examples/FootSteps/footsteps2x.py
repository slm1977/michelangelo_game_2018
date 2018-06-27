import os
import pygame
from pygame import (K_DOWN, K_LEFT, K_RETURN,
                    K_RIGHT, K_SPACE, K_UP, K_l, K_x, K_z)

from isomyr.config import Keys
from isomyr.engine import Engine
from isomyr.event import HourChangeEvent
from isomyr.handler import HourChangeSubscriber
from isomyr.objects.portal import Portal
from isomyr.skin import AnimatedSkin, DirectedAnimatedSkin, Skin
from isomyr.sound import CyclicSound
from isomyr.util.loaders import ImageLoader, SoundLoader
from isomyr.thing import MovableThing, PhysicalThing, PortableThing, FallableThing
from isomyr.world.calendar import SPEED_04, TimeChange
from isomyr.world.world import worldFactory

from custom_characters import SuperJumpingPlayer, MinutesChangeSubscriber, AutoMovableThing

dirname = os.path.dirname(__file__)


class InfoEvent(HourChangeEvent):
    """
    A custom event class for the grandfather clock in this example.
    """

    player = None
    def getMessage(self, hour):
        count = hour % 12

        info = "%s) Posizione del player %s" % (count,str(self.player.location))
        return info


# Set the custom keys for the game.
custom_keys = Keys(
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
imageLoader = ImageLoader(basedir=dirname, transparency=(255, 255, 255))
soundLoader = SoundLoader(basedir=dirname)



def play_bg_music(file = 'bg_music.mp3'):
    #pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    #pygame.event.wait()

def setupWorld():
    """
    Create the world, the scenes that can be visited, the objects in the
    scenes, and the player.
    """
    # Create the world.
    world = worldFactory(name="Clock World")

    play_bg_music()
    # Create the scene.
    livingRoom = world.addScene("The Living Room")
    livingRoom.setSkin(
        Skin(imageLoader.load("livingroom2x.png")))

    # Create the player and set his animated skin.

    myPlayer = SuperJumpingPlayer(jump_height=10, name="Ian Curtis", location=[0, 0, 0], size=[14, 14, 50],
        velocityModifier=5)

    InfoEvent.player = myPlayer

    ianCurtis = livingRoom.addPlayer(myPlayer)
    southFacing = imageLoader.load([
        "player/ian_curtis1.png", "player/ian_curtis2.png",
        "player/ian_curtis3.png"])
    eastFacing = imageLoader.load([
        "player/ian_curtis4.png", "player/ian_curtis5.png",
        "player/ian_curtis6.png"])
    playerSkin = DirectedAnimatedSkin(
        southFacing, eastFacing, frameSequence=[0, 2, 2, 1, 1, 2, 2, 0])
    ianCurtis.setSkin(playerSkin)
    walkingSound = CyclicSound(
        frequency=0.25, volume=(0.2, 0.2), sound=soundLoader.load("step.wav"))
    ianCurtis.setWalkSound(walkingSound)

    # Put in ground and walls.
    ground = PhysicalThing(
        "ground", [-1000, -1000, -100], [2000, 2000, 100])
    wall0 = PhysicalThing("wall", [290, 390, 0], [356, 14, 50])


    wall1 = PhysicalThing("wall", [0, 350, -20], [400, 20, 100])
    #wall1.setSkin(Skin(imageLoader.load(["brick.png"])))
    wall2 = PhysicalThing("wall", [0, -20, -20], [180, 20, 100])
    wall3 = PhysicalThing("wall", [-20, 0, -20], [20, 180, 100])

    sofa = AutoMovableThing(
        name="sofa", location=[390,100, 0], size=[39, 66, 30], fixed=False)
    sofa.setSkin(
        Skin(imageLoader.load(["sofa.png"])))

    # Populate the living room.
    #livingRoom.addObjects([
    #    ground, wall0, wall1, wall2, wall3, sofa,
    #   ])

    livingRoom.addObjects([
        ground,  wall1, sofa])

    return world


def run():
    # Create an isomyr engine and start it.
    titlebar = os.path.join(dirname, "titlebar.png")
    engine = Engine(keys=custom_keys, gameSpeed=SPEED_04,
                    displayOffset=[400, 344], sceneSize=(800, 1200),
                    titleFile=titlebar, textAreaPosition=(10, 800),
                    textAreaSize=(800, 400))

    world = setupWorld()
    engine.setStartingWorld(world, welcomeMessage="Benvenuti al nostro strano gioco!")
    time = engine.world.getWorldTime()

    time.setTimeEvent(TimeChange.hour, InfoEvent, MinutesChangeSubscriber())

    lr = world.getScene("The Living Room")
    sofa = lr.getObject("sofa")


    engine.run()




if __name__ == "__main__":
    run()
