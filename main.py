# ranks in ascending order: 5-14, 1
ranks = list(range(5, 15)) + list([1])
suits = ["R", "G", "Y", "B"]
rook_card = "RK"
points_per_card = {rook_card: 20, 1: 15, 14: 10, 10: 10, 5: 5}

sample_inputs = [
    "Y 1R 12R 7Y 8R 11B",
    "B 12B 1G 7B 14B",
    "G 6G 13G 12G RK 1G 10B",
    "R RK 1R 1G 1B 1Y"
]


def process_trick(trick):
    # assume valid input for now

    # get the winning card
    winning_card = compute_winning_card(trick)

    # get the points captured
    points = compute_trick_points(trick)

    # put together the result, the winning card and the captured points
    return winning_card + " " + str(points) + "p"


def compute_winning_card(trick):
    # get the trump suit and cards played in trick
    trump_suit = get_trump_suit(trick)
    trick_cards = get_trick_cards(trick)

    # if any of the cards played is the Rook, return the Rook
    if rook_card in trick_cards:
        return rook_card

    # first card is the leading card and determines the leading suit of the trick
    leading_card = trick_cards[0]
    leading_suit = get_card_suit(leading_card)
    leading_rank = get_card_rank(leading_card)

    # assume leading card as winning card
    winning_suit = leading_suit
    winning_rank = leading_rank

    # iterate through remaining cards
    for card in trick_cards[1:]:
        card_rank = get_card_rank(card)
        card_suit = get_card_suit(card)
        if is_suit_superior(card_suit, winning_suit, trump_suit):
            winning_suit = card_suit
            winning_rank = card_rank
            continue
        if card_suit == winning_suit and is_rank_superior(card_rank, winning_rank):
            winning_rank = card_rank

    # put together the winning card
    winning_card = str(winning_rank) + winning_suit
    return winning_card


def is_suit_superior(challenging_suit, defending_suit, trump_suit):
    return challenging_suit == trump_suit and defending_suit != trump_suit


def is_rank_superior(challenging_rank, defending_rank):
    return ranks.index(challenging_rank) > ranks.index(defending_rank)


def compute_trick_points(trick):
    trick_cards = get_trick_cards(trick)

    # count and add the points on each card
    points = 0
    for card in trick_cards:
        points += get_card_points(card)

    return points


def get_trump_suit(trick):
    # first character is the initial letter of the trump suit
    return trick[0]


def get_trick_cards(trick):
    # the first character indicates the trump suit
    # parse the remainder of the string as the played cards
    rem_trick = trick[2:]
    return rem_trick.split(' ')


def get_card_rank(card):
    # assuming it is not the Rook card,
    # the rank is in the first 1 or 2 characters, the last being the suit
    return int(card[:-1])


def get_card_suit(card):
    # assuming it is not the Rook card,
    # the suit is the last character of the card
    return card[-1:]


def get_card_points(card):
    # special case: Rook card
    if card == rook_card:
        return points_per_card[rook_card]

    # otherwise get card rank and access points dictionary
    card_rank = get_card_rank(card)
    if card_rank in points_per_card:
        return points_per_card[card_rank]

    # most cards have no points
    return 0


def main():
    for trick in sample_inputs:
        result = process_trick(trick)
        print(trick + " --> " + result)


if __name__ == '__main__':
    main()
