from rest_framework import serializers
import numpy as np
from ttoe.ai import play

class TMoveSerializer(serializers.Serializer):
    board = serializers.RegexField(regex=r'^[XO-]{9}$')
    move = serializers.IntegerField(read_only=True)


    def create(self, validated_data):
        # transform the data that comes in the form X-O----- to a list of lists of 1, -1 and 0
        board = [[1 if c == 'X' else -1 if c == 'O' else 0 for c in validated_data['board'][i:i+3]] for i in range(0, 9, 3)]
        # get the move from the AI
        move = play.ai_player(np.array(board))

        # the move is just a number from 0 to 8, we just turn that index of the validated_data['board'] to X
        print('current board', validated_data['board'])
        print('predicted move: ', move)

        new_board = validated_data['board'][:move] + 'X' + validated_data['board'][move+1:]
        print('new board', new_board)

        validated_data['board'] = new_board
        validated_data['move'] = move
        return validated_data