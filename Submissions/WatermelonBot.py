# Testing PR request#3
# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
SECONDARY_SKILL = Grenade

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
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])

        # projectile blok
        for i in enemy_projectiles:
            proj_dist = abs(get_pos(player)[0] - get_proj_pos(i)[0])
            if proj_dist == 1:
                if get_projectile_type(i) is not Grenade:
                    return BLOCK

        if get_last_move(enemy) == LIGHT or get_last_move(enemy) == HEAVY:
            if distance == 1:
                if get_last_move(player) is not BLOCK:
                    return BLOCK
        elif get_stun_duration(enemy) and distance == 1:
            return LIGHT

        #cum nd go
        if (distance <= 2) and (not get_primary_cooldown(player)):
            return PRIMARY
        if (distance < 6) and (not get_secondary_cooldown(player)):
            if get_last_move(enemy) == FORWARD:
                return SECONDARY


        while distance < 6:
            return BACK

        return FORWARD

