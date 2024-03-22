# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = OnePunchSkill
SECONDARY_SKILL = Hadoken

# constants, for easier move return
# movements
JUMP = ("move", (0, 1))
FORWARD = ("move", (1, 0))
BACK = ("move", (-1, 0))
JUMP_FORWARD = ("move", (1, 1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)


# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL

    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary

    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        player_pos = get_pos(player)
        enemy_pos = get_pos(enemy)
        distance = abs(player_pos[0] - enemy_pos[0])

        if distance >= 6:
            return FORWARD
        
        if not secondary_on_cooldown(player):
            return SECONDARY
        
        if get_block_status(player) > 0:
            return BLOCK
        
        if get_stun_duration(player) > 0:
            return NOMOVE
        
        if get_stun_duration(enemy) > 0 and distance <= 1:
            return LIGHT
        
        if get_hp(player) < 30 and distance > 2:
            if not primary_on_cooldown(player):
                return PRIMARY
        
        if not primary_on_cooldown(player) and distance == 1:
            return PRIMARY
        
        if distance <= 1:
            if not heavy_on_cooldown(player):
                return HEAVY
            return LIGHT
        
        if player_pos[0] < enemy_pos[0]:
            return FORWARD
        elif player_pos[0] > enemy_pos[0]:
            return BACK
        
        return NOMOVE