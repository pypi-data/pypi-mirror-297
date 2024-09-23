from importlib.metadata import version

from .blackjack import Card, Dealer, GameMaster, Player, main

__all__ = ["Card", "Dealer", "GameMaster", "Player", "main"]
__version__ = version(__package__)
