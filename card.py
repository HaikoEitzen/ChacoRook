from enum import Enum, auto

# ranks in ascending order
ranks = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 'Rook']
rank_of_rook = ranks[-1]


class Suit(Enum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLACK = auto()
    ROOK = auto()

    @classmethod
    def to_short(cls, suit):
        if type(suit) is not Suit:
            raise ValueError(f'{suit} is not a Valid Suit')
        if suit == Suit.ROOK:
            raise ValueError(f'No short suit representation for Rook')
        initials = {Suit.RED: 'R',
                    Suit.GREEN: 'G',
                    Suit.YELLOW: 'Y',
                    Suit.BLACK: 'B'}
        return initials[suit]


class Card:
    points_per_rank = {'Rook': 20,
                       1: 15,
                       14: 10,
                       10: 10,
                       5: 5}

    def __init__(self, rank, suit):
        if rank not in ranks:
            raise ValueError(f'{rank} is not a valid Rank')
        if type(suit) is not Suit or suit not in Suit:
            raise ValueError(f'{suit} is not a Valid Suit')
        if rank == rank_of_rook and suit != Suit.ROOK or suit == Suit.ROOK and rank != rank_of_rook:
            raise ValueError('If rank or suit is Rook, both need to be Rook')
        self.rank = rank
        self.suit = suit
        self.points = self._get_points()

    def _get_points(self):
        if self.rank in Card.points_per_rank:
            return Card.points_per_rank[self.rank]
        return 0

    def __repr__(self):
        return f'<Card {repr(self.rank)} {repr(self.suit.name)}>'

    def __str__(self):
        if self.rank == rank_of_rook:
            return 'RK'
        return f'{self.rank}{Suit.to_short(self.suit)}'

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


Card.Rook = Card('Rook', Suit.ROOK)
