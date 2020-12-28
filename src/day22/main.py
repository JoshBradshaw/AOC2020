from collections import deque, defaultdict
from copy import copy
import fileinput
from enum import Enum


def crab_combat(player1_deck, player2_deck):
    p1_deque = deque(player1_deck)
    p2_deque = deque(player2_deck)

    while len(p1_deque) > 0 and len(p2_deque) > 0:
        tp1, tp2 = p1_deque.popleft(), p2_deque.popleft()
        if tp1 > tp2:
            p1_deque.extend([tp1, tp2])
        else:
            p2_deque.extend([tp2, tp1])

    winning_deck = p1_deque if len(p1_deque) > 0 else p2_deque
    return sum(ii * n for ii, n in enumerate(reversed(winning_deck), start=1))


class GameOutcomes(Enum):
    Player1Win = 0
    Player2Win = 1


past_game_states = defaultdict(set)
game_id = 0


def get_game_id():
    global game_id
    game_id += 1
    return game_id


def recursive_crab_combat(p1_deque, p2_deque, game_id):
    n_round = 0
    while len(p1_deque) > 0 and len(p2_deque) > 0:
        game_configuration = encode_game_configurations(p1_deque, p2_deque)
        if game_configuration in past_game_states[game_id]:
            return GameOutcomes.Player1Win
        else:
            past_game_states[game_id].add(game_configuration)

        tp1, tp2 = p1_deque.popleft(), p2_deque.popleft()

        if tp1 <= len(p1_deque) and tp2 <= len(p2_deque):
            if recursive_crab_combat(deque(list(copy(p1_deque))[:tp1]), deque(list(copy(p2_deque))[:tp2]),
                                     get_game_id()) is GameOutcomes.Player1Win:
                p1_deque.extend([tp1, tp2])
            else:
                p2_deque.extend([tp2, tp1])
        elif tp1 >= tp2:
            p1_deque.extend([tp1, tp2])
        else:
            p2_deque.extend([tp2, tp1])

        n_round += 1

    if game_id == 0:
        winning_deck = p1_deque if len(p1_deque) > 0 else p2_deque
        print(winning_deck)
        print(sum(ii * n for ii, n in enumerate(reversed(winning_deck), start=1)))

    if len(p1_deque) > 0:
        return GameOutcomes.Player1Win
    else:
        return GameOutcomes.Player2Win


def encode_game_configurations(p1_deck, p2_deck):
    p1_deck_str = ",".join(str(n) for n in p1_deck)
    p2_deck_str = ",".join(str(n) for n in p2_deck)

    return f"P1 {p1_deck_str} P2 {p2_deck_str}"


def parse(input_stream):
    player1_deck = []
    player2_deck = []
    decks = iter([player1_deck, player2_deck])

    deck = next(decks)
    for line in input_stream:
        if line.strip() and line[0].isdigit():
            deck.append(int(line.strip()))
        if not line.strip():
            deck = next(decks)
    return player1_deck, player2_deck


p1_deck, p2_deck = parse(fileinput.input())
print(crab_combat(p1_deck, p2_deck))
print(recursive_crab_combat(deque(p1_deck), deque(p2_deck), game_id))
