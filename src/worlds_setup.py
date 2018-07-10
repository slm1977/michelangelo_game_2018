import os

from isomyr.objects.character import *
from isomyr.objects.portal import Portal
from isomyr.skin import Skin, DirectedAnimatedSkin
from isomyr.util.loaders import ImageLoader
from isomyr.thing import MovableThing, PhysicalThing, PortableThing
from isomyr.world.world import worldFactory
from custom_thing import Talking_NPC,Super_jumpino_player, Locked_portal,Win_thing


dirname = os.path.dirname(__file__)
#setting up the image loader
imageLoader = ImageLoader(basedir=dirname, transparency=(255, 255, 255))
#setup world function
def setupWorld(engine):
    """
    Create the world, the scenes that can be visited, the objects in the
    scenes, and the player.
    """
    # Create the world
    world = worldFactory( name="Dolianova", sceneSize=(800,600))


    # Create the first scene.
    prigione = world.addScene("prigione")
    prigione.setSkin(Skin(imageLoader.load("stanze/prova_prigione.png")))

    # Create the second scene.
    stanza_2 = world.addScene("stanza cicciona")
    stanza_2.setSkin(Skin(imageLoader.load("lounge.png")))

    #victory room
    stanza_vittoria = world.addScene("the room for the famous people")
    stanza_vittoria.setSkin(Skin(imageLoader.load("stanze/prova_stanza3.png")))
    scritta_vittoria = PhysicalThing(name="key", location=[90, 110, 20], size=[30, 100, 50], fixed=False)
    scritta_vittoria.setSkin((Skin(imageLoader.load("custom_stuff/vinto.png"))))

    #create my own modified player
    my_player = Super_jumpino_player(jump_height=8,name="IO COSMICO" , location=[90, 90, 100], size=[14, 14, 50],velocityModifier=3)
    # Create the player and set his animated skin.
    io_cosmico = prigione.addPlayer(player=my_player)
    south_facing = imageLoader.load([
        "player/ian_curtis1.png", "player/ian_curtis2.png",
        "player/ian_curtis3.png"])
    east_facing = imageLoader.load([
        "player/ian_curtis4.png", "player/ian_curtis5.png",
        "player/ian_curtis6.png"])
    io_cosmico.setSkin(
        DirectedAnimatedSkin(south_facing, east_facing,
                             frameSequence=[0, 2, 2, 1, 1, 2, 2, 0]))

    #NPCs
    npc1 = Talking_NPC(name="PRIGIONIERO", location=[120, 120, 0], size=[14, 14, 50])
    npc1.setSkin((Skin(imageLoader.load(["custom_stuff/npc/npc_prigioniero.png"]))))
    npc1.set_view(engine.view)
    npc1.set_text("finalmente ti sei svegliato! Esci di qua!(puoi spostare gli oggetti)")

    npc2 = Talking_NPC(name="INDIVIDUO",location=[120,120,0],size=[14, 14, 50])
    npc2.setSkin((Skin(imageLoader.load(["custom_stuff/npc/npc_standard.png"]))))
    npc2.set_view(engine.view)
    npc2.set_text("sono un individuo casuale come te. Solo che tu devi trovare una chiave, e io no")

    # Build the non-skinned prigione scene objects (we'll re-use these for the
    # lounge scene).
    ground = PhysicalThing("ground", [-1000, -1000, -100], [3000, 3000, 100])
    wall0 = PhysicalThing("wall", [180, 0, -20], [20, 180, 120])
    wall1 = PhysicalThing("wall", [40, 180, -20], [180, 20, 120])
    wall2 = PhysicalThing("wall", [0, -20, -20], [180, 20, 120])
    wall3 = PhysicalThing("wall", [-20, 0, -20], [20, 180, 120])

    # Build the skinned prigione scene objects.
    finestra = Portal(
        name="finestra", location=[65, -10 , 90], size=[35,10, 20], toScene=stanza_2,
        toLocation=[25, 115, 0])

    key = Win_thing(name="chiave nascostina", location=[5, 5, 0], size=[20, 12, 10])
    key.setSkin(Skin(imageLoader.load(["custom_stuff/key.png"])))
    key.text.setPickedUp(("ce l'hai fatta sei un genio!"))
    key.text.setDropped("emh?!?!? Prendimi di nuovo!")
    key.text.setUsed("Non succede niente... E CI CREDO! SONO UNA CHIAVE! Che ti aspettavi?")

    bed = MovableThing(
        name="bed", location=[0, 100, 0], size=[70, 52, 28], fixed=True)
    bed.setSkin(Skin(imageLoader.load(["bed.png"])))

    comodino = PhysicalThing(
        name="comodino", location=[150, 0, 0], size=[10, 10, 25], fixed=False)
    comodino.setSkin(Skin(imageLoader.load("custom_stuff/comodino.png")))


    sofa = PhysicalThing(
        name="sofa", location=[15, 0, 0], size=[39, 66, 37], fixed=False)
    sofa.setSkin(
        Skin(imageLoader.load(["sofa.png"])))
    return_door = Portal(
        name="return door", location=[0, 100, 00], size=[10, 10, 56], toScene=prigione,
        toLocation=[60, 20, 56])

    # Populate the prision (the player has already been added).
    prigione.addObjects([
        ground, wall0, wall1, wall2, wall3, finestra,
        bed, comodino, io_cosmico, npc1])


    # Populate the second room.
    stanza_2.addObjects([
        ground, wall0, wall1, wall2, wall3,
        sofa,npc2,key,return_door
        ])

    win_door = Locked_portal(name="win_door", location=[180, 105, 0], size=[10, 30, 56], toScene=stanza_vittoria, toLocation=[10, 115, 0])
    win_door.setSkin(Skin(imageLoader.load(["door.png"])))

    #adding "win_door" after having initializend it
    stanza_2.addObject(win_door)

    #victory room objets
    stanza_vittoria.addObjects([ground, wall0, wall1, wall2, wall3,scritta_vittoria])

    return world