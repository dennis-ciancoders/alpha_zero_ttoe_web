from rest_framework import serializers
import numpy as np
from ttoe.ai import play
from ttoe.ai.TicTacToeGame import TicTacToeGame
from ttoe.models import Game

class TMoveSerializer(serializers.Serializer):
    board = serializers.RegexField(regex=r'^[XO-]{9}$')
    move = serializers.IntegerField(read_only=True)
    ended = serializers.BooleanField(read_only=True)
    winner = serializers.CharField(read_only=True)


    def _check_ended(self, board):
        # check if the game ended
        game = TicTacToeGame()
        status = game.getGameEnded(np.array(board), 1)

        # status is 0 if not ended, 1 if player 1 won, -1 if player 1 lost 1e-4 if draw
        winner = '-'
        if status == 1:
            winner = 'X'
        elif status == -1:
            winner = 'O'

        return status, winner

    def create(self, validated_data):
        # transform the data that comes in the form X-O----- to a list of lists of 1, -1 and 0
        board = [[1 if c == 'X' else -1 if c == 'O' else 0 for c in validated_data['board'][i:i+3]] for i in range(0, 9, 3)]

        # first check if the game ended
        status, winner = self._check_ended(board)
        move = -1
        new_board = validated_data['board']

        if status == 0: # game not ended
            # get the move from the AI
            move = play.ai_player(np.array(board))

            # update the board, the move is a number from 0 to 8 but the board is a list of lists
            board[move // 3][move % 3] = 1

            # check if the game ended
            status, winner = self._check_ended(board)

            # the move is just a number from 0 to 8, we just turn that index of the validated_data['board'] to X
            print('current board', validated_data['board'])
            print('predicted move: ', move)
            new_board = validated_data['board'][:move] + 'X' + validated_data['board'][move+1:]
            print('new board', new_board)

        if status != 0: # game ended
            print('----------------game ended----------------')
            print('winner: ', winner)
            print('board: ', board)
            print('------------------------------------------')
            # save the game
            Game.objects.create(board=new_board, winner=winner)


        validated_data['winner'] = winner
        validated_data['ended'] = status != 0
        validated_data['board'] = new_board
        validated_data['move'] = move
        return validated_data