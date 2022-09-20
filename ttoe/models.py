from django.db import models

# Create your models here.
class Game(models.Model):
    """Model representing a game of Tic-Tac-Toe"""
    board = models.CharField(max_length=9)
    winner = models.CharField(max_length=1)
    def __str__(self):
        return f'Game {self.game_id} - {self.board} - {self.winner}'