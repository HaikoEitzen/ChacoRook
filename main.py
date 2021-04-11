# ranks in ascending order, excluding the Rook
ranks = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1]
# Red, Green, Yellow, Black
suits = ["R", "G", "Y", "B"]
rook_card = "RK"
points_per_card = {
    rook_card: 20,
    1:  15,
    14: 10,
    10: 10,
    5:  5}

# <trump suit> <leading card> [<other played cards>]
sample_tricks = [           # expected winning card and captured points
    "Y 1R 12R 7Y 8R 11B",       # 7Y    15p
    "B 12B 1G 7B 14B",          # 14B   25p
    "G 6G 13G 12G RK 1G 10B",   # RK    45p
    "R RK 1R 1G 1B 1Y",         # RK    80p
    "Y 5G 1R 14B 11R 1B",       # 5G    45p
    "Y 5G 1R 14B 11G 1B",       # 11G   45p
    "Y 5G 1R 14B 11G 1B 10Y",   # 10Y   55p
    "Y 5G 1R 14B 11G 1B 10G"    # 11G   55p
]

# <leading card> [<cards in hand>]
sample_hands = [                # expected playable cards
    "9R 5G 7G 6B 14B 12B 8Y RK",    # 5G 7G 6B 14B 12B 8Y RK
    "10R 5G 7G 6B 14B 12B 8Y 8R",   # 8R
    "5R 5G 7G 6B 14R 12R 8Y RK",    # 14R 12R RK
    "11B 5G 7G 6B 14B 12B 8Y RK",   # 6B 14B 12B RK
    "6Y 5G 7G 6B 14B 12B 8Y RK",    # 8Y RK
    "1Y 5Y 7G 6Y 14B 12B 8Y 10Y",   # 5Y 6Y 8Y 10Y
    "RK 5Y 7G 6Y 14B 12B 8Y 10Y"    # 5Y 7G 6Y 14B 12B 8Y 10Y
]


def process_trick(trick):
    # assume valid input for now

    # get the winning card
    winning_card = compute_winning_card(trick)

    # get the points captured
    points = compute_trick_points(trick)

    # return the winning card and the captured points
    return winning_card, points


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
    winning_card = f'{winning_rank}{winning_suit}'
    return winning_card


def is_suit_superior(challenging_suit, defending_suit, trump_suit):
    # the defending suit is always at least the leading suit
    # so only the trump suit is superior
    return challenging_suit == trump_suit != defending_suit


def is_rank_superior(challenging_rank, defending_rank):
    # ranks list is in ascending order, compare indices
    return ranks.index(challenging_rank) > ranks.index(defending_rank)


def compute_trick_points(trick):
    # count and add the points on each card
    trick_cards = get_trick_cards(trick)
    points = sum(get_card_points(card) for card in trick_cards)
    return points


def get_trump_suit(trick):
    # first character is the initial letter of the trump suit
    return trick[0]


def get_trick_cards(trick):
    # the first character indicates the trump suit
    # parse the remainder of the string as the played cards
    rem_trick = trick[2:]
    return rem_trick.split(' ')


def process_hand_on_turn(hand):
    # assume valid input for now

    leading_card, cards_in_hand = get_leading_card_and_cards_in_hand(hand)

    # special case: leading card is Rook, all cards in hand are playable
    if leading_card is rook_card:
        return cards_in_hand

    # for the next cases, get leading suit
    leading_suit = get_card_suit(leading_card)

    # if no card in hand matches leading suit, all cards are playable
    if not any(get_card_suit(card) == leading_suit for card in cards_in_hand):
        return cards_in_hand

    # if at least one card matches leading suit, return those cards,
    # and always include the Rook if in hand
    playable_cards = \
        (card for card in cards_in_hand if
         get_card_suit(card) == leading_suit or
         card == rook_card)
    return playable_cards


def get_leading_card_and_cards_in_hand(hand):
    # the first card is the leading card
    # all following cards are the cards in player's hand
    cards = hand.split(' ')
    leading_card = cards[0]
    cards_in_hand = cards[1:]
    return leading_card, cards_in_hand


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


def process_sample_tricks():
    for trick in sample_tricks:
        winning_card, points = process_trick(trick)
        print(f'{trick} --> {winning_card} {points}p')


def process_sample_hands():
    for hand in sample_hands:
        playable_cards = process_hand_on_turn(hand)
        playable_cards_string = ' '.join(playable_cards)
        print(f'{hand} --> {playable_cards_string}')


def main():
    print('Tricks')
    process_sample_tricks()
    print('Hands')
    process_sample_hands()


if __name__ == '__main__':
    main()
