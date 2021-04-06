# ranks in ascending order: 5-14, 1
ranks = list(range(5, 15)) + list([1])
suits = ["R", "G", "Y", "B"]
rook_card = "RK"

sample_inputs = [
    "Y 1R 12R 7Y 8R 11B",
    "B 12B 1G 7B 14B",
    "G 6G 13G 12G RK 1G 10B",
    "R RK 1R 1G 1B 1Y"
]


def process_trick(trick):
    # assume valid input for now

    # first character is the initial letter of the trump suit
    trump_suit = trick[0]

    # parse the remainder of the string as the played cards
    rem_trick = trick[2:]
    trick_cards = rem_trick.split(' ')

    # if any of the cards played is the Rook, return the Rook
    if trick_cards.__contains__(rook_card):
        return rook_card

    # first card is the leading card and determines the leading suit of the trick
    leading_card = trick_cards[0]
    leading_suit = leading_card[-1:]
    leading_rank = int(leading_card[:-1])

    # assume leading card as winning card
    winning_suit = leading_suit
    winning_rank = leading_rank
    for card in trick_cards[1:]:
        card_rank = int(card[:-1])
        card_suit = card[-1:]
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
    if challenging_suit == trump_suit and defending_suit != trump_suit:
        return True
    return False


def is_rank_superior(challenging_rank, defending_rank):
    return ranks.index(challenging_rank) > ranks.index(defending_rank)


def main():
    for sample in sample_inputs:
        winning_card = process_trick(sample)
        print(sample + " --> " + winning_card)


if __name__ == '__main__':
    main()
