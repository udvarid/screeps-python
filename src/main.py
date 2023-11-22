import harvester
# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
from defs import *

# These are currently required for Transcrypt in order to use the following names in JavaScript.
# Without the 'noalias' pragma, each of the following would be translated into something like 'py_Infinity' or
#  'py_keys' in the output file.
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def main():
    """
    Main game logic loop.
    """

    # Run each creep
    creeps = Object.keys(Game.creeps)
    for name in creeps:
        creep = Game.creeps[name]
        harvester.run_harvester(creep)


    # Run each spawn
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        if not spawn.spawning:
            # Get the number of our creeps in the room.
            num_creeps = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName)
            if num_creeps < 8 and spawn.room.energyCapacityAvailable >= 250:
                spawn.createCreep([WORK, CARRY, MOVE, MOVE])

    for name in Object.keys(Memory.creeps):
        if not creeps.includes(name):
            del Memory.creeps[name]


module.exports.loop = main
