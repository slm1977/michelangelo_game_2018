import basic
from isomyr.engine import *
import pygame
import sys
from custom_thing import Win,Locked_portal

win = Win(4000,pygame.image.load("custom_stuff/credits_videogame.png"), music="custom_stuff/Soviet union.mp3")

class Super_engine(Engine):

    def setStartingWorld(self, world, time=None, welcomeMessage=""):
        super(Super_engine, self).setStartingWorld(world, time, welcomeMessage)
        stanza_2 = self.world.getScene("stanza cicciona")
        self.portal = stanza_2.getObject("win_door")
        self.portal.set_view(self.view)

    def playerControl(self, objectList, surface, player):
        """
        Checks for key presses and quit events from the player.

        objectList: The group of objects in the players scene: list of
            object_3d class or subclass
        player: The avatar being used for the player: Avatar class
        surface: The area of the surface to draw into from the pygame window:
            surface class

        kquit: returns 1 if quit event occurs: integer
        """
        # Check movement keys based on direct access to the keyboard state.
        keys = pygame.key.get_pressed()
        # XXX Maybe put this in an event handler too...
        # Checks for the direction keys: up down left right.
        if (keys[self.keys.up] is 1 or
            keys[self.keys.down] is 1 or
            keys[self.keys.left] is 1 or
            keys[self.keys.right] is 1):
            if keys[self.keys.up] is 1:
                player.updatePosition([-1 * player.velocityModifier, 0, 0])
            if keys[self.keys.down] is 1:
                player.updatePosition([1 * player.velocityModifier, 0, 0])
            if keys[self.keys.left] is 1:
                player.updatePosition([0, 1 * player.velocityModifier, 0])
            if keys[self.keys.right] is 1:
                player.updatePosition([0, -1 * player.velocityModifier, 0])
        # If no direction key is pressed then stop the player.
        else:
            player.stop()
        # Check for the Jump key.
        if keys[self.keys.jump] is 1:
            player.jump()
        kquit = 0

        # Check other keys and window close/QUIT based on the event queue
        # system.
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT +3:
                win.credits()
            # Check for a quit program action caused by the window close and
            # Control-C keypress.
            if event.type is pygame.QUIT:
                kquit = 2
                sys.exit()
            # XXX Add a "keydown" function that all this logic can live in.
            # Check for a quit game action.
            elif event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                kquit = 2
                sys.exit()
            # XXX Add an event for the logic entailed here in the examine
            # check.
            elif event.type is pygame.KEYDOWN and event.key == pygame.K_e:
                self.examineting = True
            elif event.type is pygame.KEYUP and event.key == pygame.K_e:
                self.examineting = False
            # Check for the examine key.
            elif (event.type is pygame.KEYDOWN and event.key == self.keys.examine):
                # If the player is carrying an object then show its examine
                # images.
                is_examinable = isinstance(
                    player.inventory[player.using],
                    ExaminableSkin)
                if len(player.inventory) > 0 and is_examinable:
                     self.examine(objectList, player, surface)
            # Check for pick up key.
            elif (event.type is pygame.KEYDOWN and event.key == self.keys.pick_up):
                notify(PlayerPickUpItemEvent(player))
            # Check for the drop key.
            elif event.type is pygame.KEYDOWN and event.key == self.keys.drop:
                notify(PlayerDropItemEvent(player))
            # Check for the using key.
            elif event.type is pygame.KEYDOWN and event.key == self.keys.using:
                if len(player.inventory) > 0:
                    item = player.inventory[player.using]
                    #print item
                    notify(PlayerUsingItemEvent(item, player))

        return kquit

    def get_examin(self):
        return self.examineting
    def get_view(self):
        return self.view

    # XXX Move this out of the engine and into a suitably abstracted perception
    # object, or player-environment interaction object.
