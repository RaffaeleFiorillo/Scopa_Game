import random
import itertools


def get_possible_combinations(card_value, table_cards):
	possible_plays = []
	
	# Use filter to get eligible table cards
	eligible_table_cards = [i for i in table_cards if i <= card_value]
	
	for r in range(1, len(eligible_table_cards) + 1):
		for combination in itertools.combinations(eligible_table_cards, r):
			print(f"{r}->{combination}")
			if sum(combination) == card_value:
				possible_plays.append(combination)
	return possible_plays


# returns True if it is possible to use a card to take, otherwise returns False
# in the future, when move hints will be available, this function will be removed for len(get_possible_combinations) > 0
def taking_is_possible(card_value, table_cards):
	# Use filter to get eligible table cards
	eligible_table_cards = [i for i in table_cards if i <= card_value]
	if len(eligible_table_cards) == 0:  # there are no cards that can be taken
		return False
	if card_value in eligible_table_cards:  # there is a card with the same value as the one selected
		return True
	for r in range(2, len(eligible_table_cards) + 1):
		for combination in itertools.combinations(eligible_table_cards, r):
			if sum(combination) == card_value:
				return True
	return False


def test_get_possible_combinations():
	test_cases = [
		([1, 2, 3, 4, 5], 7, [(2, 5), (3, 4), (1, 2, 4)]),
		([2, 4, 6, 8, 10], 6, [(2, 4)]),
		([1, 2, 3, 4, 5], 10, [(1, 2, 3, 4), (1, 4, 5), (2, 3, 5)]),
		([1, 2, 3, 4, 5], 6, [(1, 2, 3), (2, 4), (1, 5)]),
		([1, 2, 3, 4, 5], 9, [(2, 3, 4), (4, 5), (1, 3, 5)]),
	]
	
	for table_cards, card_value, expected_plays in test_cases:
		actual_plays = get_possible_combinations(card_value, table_cards)
		assert expected_plays == [sorted(play) for play in set(actual_plays)], \
			f"Failed for table cards {table_cards}, card value {card_value}. Expected {expected_plays}, but got {actual_plays}"
	
	print("All test cases passed!")


def get_move_points(selected_card, table_cards):
	active_cards = [card for card in table_cards if card.active]
	# scopa: after the player takes, there are no more cards on the table
	is_scopa = len(active_cards) == len(table_cards) and selected_card.number == sum(
		[int(card) for card in active_cards])
	# settebello: if the player takes the seven of Denara
	is_settebello = selected_card.is_settebello or len(list(filter(lambda x: x.is_settebello, active_cards))) == 1
	
	# scopa + settebello
	points = (1 if is_scopa else 0) + (1 if is_settebello else 0)
	# print(f"Scopa: {is_scopa} | Settebello: {is_settebello}")
	return points


def get_index_combinations(lst):
	index_combinations = []
	for r in range(1, len(lst) + 1):
		index_combinations.extend(list(itertools.combinations(range(len(lst)), r)))
	return index_combinations


def generate_all_possible_taking_combinations(hand_cards, table_cards) -> {int: [(int,)]}:
	combinations = {0: [], 1: [], 2: []}
	all_combinations = get_index_combinations(table_cards)
	for i, card in enumerate(hand_cards):
		for combination in all_combinations:
			if taking_is_possible(card.number, [table_cards[c_index].number for c_index in combination]):
				combinations[i].append(combination)
	return combinations


def get_move_value(hand_card, table_cards, cards_to_take):
	move_score = 0
	
	# scopa: after the player takes, there are no more cards on the table
	if len(cards_to_take) == len(table_cards):
		move_score += 2
	# it is possible to do a scopa with the remaining cards
	# elif sum(remaining_cards) <= 10:
	#   (some_weight) * (probability to do a scopa with the remaining cards)
	
	# settebello: if the player takes the seven of Denara (settebello is among cards to take)
	if hand_card.is_settebello or len(list(filter(lambda x: x.is_settebello, cards_to_take))) == 1:
		move_score += 1
	# settebello is on the table, but it is not being taken
	elif len(list(filter(lambda x: x.is_settebello, table_cards))) == 1:
		move_score -= 0.75
	
	# Each Denara card has a value of 0.2
	move_score += sum([0.2 for card in cards_to_take if card.seme == "Denara"])
	
	# Each card with number seven has a value of 0.25
	move_score += sum([0.25 for card in cards_to_take if card.number == 7])
	
	# Each card has a value of 0.1
	move_score += len(cards_to_take) * 0.1


# The goal is to return two dictionaries:
# - The first contains, for every hand-card, all the combinations in which it can be used to take;
# - The second contains, for every hand-card, a list of evaluations with a one-to-one correspondence to the combinations
def get_moves_and_evaluations(hand_cards, table_cards) -> ({int: [(int,)]}, {int: [int]}):
	possible_cards_combinations = generate_all_possible_taking_combinations(hand_cards, table_cards)
	moves_evaluations = {0: [], 1: [], 2: []}
	for i, card in enumerate(hand_cards):
		for cards_indexes_combination in possible_cards_combinations[i]:
			combination = [table_cards[c_index] for c_index in cards_indexes_combination]
			moves_evaluations[i].append(get_move_value(card, table_cards, combination))
	return possible_cards_combinations, moves_evaluations


# The goal is to obtain the index of the hand-card to use and the indexes of the table-cards to take
# The first step is to obtain, for every hand-card, all the combinations in which it can be used to take and at the same
# time the evaluation of that combination (the higher the value, the best that combination is).
# The second step is to obtain the best card to use
# The third step is to obtain the best move for that card
def pick_best_move(hand_cards, table_cards) -> (int, [int]):
	# First step:
	possible_cards_combinations, moves_evaluations = get_moves_and_evaluations(hand_cards, table_cards)
	
	# Second step:
	# get the best move for each card
	best_moves = {0: max(moves_evaluations[0]), 1: max(moves_evaluations[1]), 2: max(moves_evaluations[2])}
	card_to_play_index = None
	# get the index of the best card to play
	if best_moves[0] > best_moves[1]:
		if best_moves[0] > best_moves[2]:
			card_to_play_index = 0
		elif best_moves[0] == best_moves[2]:
			card_to_play_index = random.choice([0, 2])
	elif best_moves[0] == best_moves[1]:
		card_to_play_index = random.choice([0, 1])
	else:
		if best_moves[1] > best_moves[2]:
			card_to_play_index = 1
		elif best_moves[1] == best_moves[2]:
			card_to_play_index = random.choice([1, 2])
		else:
			card_to_play_index = 2
	
	# Third step:
	# get the index of the best evaluation knowing which card is going to be used
	best_evaluation_index = moves_evaluations[card_to_play_index].index(best_moves[card_to_play_index])
	# obtain the index of the move (the index of the combination of table_cards's indexes to take)
	move_index = possible_cards_combinations[card_to_play_index].index(best_evaluation_index)
	# obtain the list of indexes that indicate which table-cards to take
	indexes_of_cards_to_take = possible_cards_combinations[card_to_play_index][move_index]
	return card_to_play_index, indexes_of_cards_to_take
