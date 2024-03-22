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
        if get_primary_skill(enemy) == "onepunch":
            if distance <= 2:
                return JUMP_BACKWARD
        for i in enemy_projectiles:
            if get_projectile_type(i) == "hadoken":
                return JUMP_FORWARD
            elif get_projectile_type(i) == "grenade" and abs(get_pos(player)[0] - get_proj_pos(i)[0]) < 3:
                return FORWARD
            elif get_projectile_type(i) == "boomerang" and abs(get_pos(player)[0] - get_proj_pos(i)[0]) == 1:
                return BLOCK
            elif get_projectile_type(i) == "beartrap" and abs(get_pos(player)[0] - get_proj_pos(i)[0]) == 1:
                return JUMP_BACKWARD

        if not primary_on_cooldown(player):
            return PRIMARY
        if not secondary_on_cooldown(player) and get_last_move(player)[1] != (0,1):
            return SECONDARY

        if distance <= 1:
            if not heavy_on_cooldown(player):
                return HEAVY
            return LIGHT

        return BACK

