from rest_framework import serializers
import numpy as np
from ttoe.ai import play

class TMoveSerializer(serializers.Serializer):
    move = serializers.RegexField(regex=r'^[XO-]{9}$')

    def create(self, validated_data):
        # transform the data that comes in the form X-O----- to a list of lists of 1, -1 and 0
        board = [[1 if c == 'X' else -1 if c == 'O' else 0 for c in validated_data['move'][i:i+3]] for i in range(0, 9, 3)]
        # get the move from the AI
        move = play.ai_player(np.array(board))

        # the move is just a number from 0 to 8, we just turn that index of the validated_data['move'] to X
        move = validated_data['move'][:move] + 'X' + validated_data['move'][move+1:]
        print('predicted move: ', move)

        validated_data['move'] = move
        return validated_data