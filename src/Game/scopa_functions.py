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
		assert expected_plays == [sorted(play) for play in set(actual_plays)],\
			f"Failed for table cards {table_cards}, card value {card_value}. Expected {expected_plays}, but got {actual_plays}"

	print("All test cases passed!")


# test_get_possible_combinations()
