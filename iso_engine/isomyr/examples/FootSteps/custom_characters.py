

from isomyr.objects.character import Player
from isomyr.handler import TimeChangeSubscriber
from isomyr.thing import FallableThing

class AutoMovableThing(FallableThing):

    def respond(self):
        # Velocity movement: Standard object movement
        if self.location[0]<300:
            self.velocity[0] = 1
        else:
            self.velocity[0] = -1
        super(AutoMovableThing, self).respond()

class SuperJumpingPlayer(Player):

    def __init__(self, jump_height=10,*args, **kwds):
        super(SuperJumpingPlayer, self).__init__(*args, **kwds)
        self.jump_height = jump_height

    def jump(self):
        """Action for the actor to jump."""
        if self.falling is False:
            # Give some altitude (z-direction).
            self.velocity[2] = self.velocity[2] + self.jump_height
            self.falling = True


class MinutesChangeSubscriber(TimeChangeSubscriber):

    def onNotice(self, event):
        min = event.calendar.time.minutes
        text = event.getMessage(min)
        if not text:
            text = "Sono passati %s minuti." % min
        event.player.getView().updateTextArea(text=text)

