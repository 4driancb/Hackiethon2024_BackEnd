# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = TeleportSkill
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

        if not secondary_on_cooldown(player) and distance > 1:
            return SECONDARY
        elif not primary_on_cooldown(player) and distance < 3:
            return PRIMARY

        self.block_heavy_combo(player, enemy)

        if distance == 1:
            return LIGHT

        return FORWARD
    
    def block_heavy_combo(self, player, enemy):
        player_x, player_y = get_pos(player)
        enemy_x, enemy_y = get_pos(enemy)

        if player_y == enemy_y and abs(player_x - enemy_x) == 1:
            if get_past_move(enemy, 1) == LIGHT:
                if get_past_move(enemy, 2) == LIGHT:
                    return BLOCK
                else:
                    return NOMOVE
            else:
                return NOMOVE
        return NOMOVE

    def winning_strategy(self, player, enemy, primary, secondary):
        # Check if any skill is available and use it wisely
        if not primary_on_cooldown(player) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= prim_range(player):
            return primary
        elif not secondary_on_cooldown(player) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= seco_range(player):
            return secondary
        elif not heavy_on_cooldown(player) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= 1:
            return HEAVY

        # Defensive strategy if low on health or enemy is too close
        if get_hp(player) < 20 or abs(get_pos(player)[0] - get_pos(enemy)[0]) < 2:
            # Block if enemy is close and likely to attack
            if abs(get_pos(player)[0] - get_pos(enemy)[0]) == 1:
                return BLOCK
            # Move away from the enemy if possible
            elif get_pos(player)[0] < get_pos(enemy)[0]:
                return BACK
            else:
                return FORWARD

        # Offensive strategy if player has more health
        if get_hp(player) > get_hp(enemy):
            # Close in on the enemy if not in attack range
            if abs(get_pos(player)[0] - get_pos(enemy)[0]) > 1:
                if get_pos(player)[0] < get_pos(enemy)[0]:
                    return FORWARD
                else:
                    return BACK
            # Use light attack if close and other attacks are on cooldown
            else:
                return LIGHT

        # Default to light attack if nothing else is applicable
        return LIGHT

