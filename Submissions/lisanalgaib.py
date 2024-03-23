# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN
import random


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
SECONDARY_SKILL = Grenade

#constants, for easier move return
#movements
JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
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
        self.list_char = [];
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):

        if get_secondary_skill(enemy) == "hadoken" or get_secondary_skill(enemy) == "boomerang":
            player_pos = get_pos(player)
            enemy_pos = get_pos(enemy)

            distance_x = abs(get_pos(player)[0] - get_pos(enemy)[0])
            distance_y = abs(get_pos(player)[1] - get_pos(enemy)[1])
            distance = abs(player_pos[0] - enemy_pos[0])

            if get_last_move(enemy) is not None:
                if get_last_move(enemy)[0] == "onepunch":
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

            # if get_last_move(player) is not None:
            #     if get_last_move(player)[0] == 'grenade':
            #         return SECONDARY
            #
            if not secondary_on_cooldown(player):
                return SECONDARY

            if not primary_on_cooldown(player) and distance_x <= 2:
                return PRIMARY

            if get_stun_duration(enemy) > 0 and distance <= 1:
                return LIGHT

            if distance <= 1:
                if not heavy_on_cooldown(player):
                    return HEAVY
                return LIGHT

            if get_last_move(player) is not None:
                if not secondary_on_cooldown(player) and not get_last_move(player) == JUMP:  # player not jumping
                    if distance_x != 1:
                        return SECONDARY
                    return LIGHT

            if distance > 2:
                return FORWARD

            return BACK
        else:
            #watermelon
            distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
            # projectile
            for i in enemy_projectiles:
                if get_projectile_type(i) == "hadoken":
                    return JUMP_FORWARD
                elif (get_projectile_type(i) == "grenade") and (abs(get_pos(player)[0] - get_proj_pos(i)[0]) < 4):
                    if not get_primary_cooldown(player):
                        return PRIMARY
                    else:
                        return BACK
                elif (get_projectile_type(i) == "boomerang") and abs(get_pos(player)[0] - get_proj_pos(i)[0]) == 2:
                    print(abs(get_pos(player)[0] - get_proj_pos(i)[0]))
                    return JUMP
                elif get_projectile_type(i) == "beartrap" and abs(get_pos(player)[0] - get_proj_pos(i)[0]) == 1:
                    return JUMP_BACKWARD

            if get_last_move(enemy) is not None:
                if get_last_move(enemy)[0] == "dash_attack" and distance < 5:
                    return BLOCK
                if get_last_move(enemy)[0] == "onepunch" and distance < 2:
                    return JUMP_BACKWARD
                if get_last_move(enemy)[0] == "uppercut" and distance < 2:
                    return BLOCK

            if distance <= 1:
                if not heavy_on_cooldown(player):
                    return HEAVY
                return LIGHT

            if (not primary_on_cooldown(player)) and (distance <= 2):
                return PRIMARY

            if distance < 7:
                if not secondary_on_cooldown(player):
                    return SECONDARY

            if distance > 2:
                return FORWARD

            return BACK

