# importar librerias

from keras import models
from keras import layers
from keras import optimizers

import numpy as np
from .utils import *  # importado desde alpha-zero-general


## se debe de volver a definir igual que en el notebook
class RedNeuronal():
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        # ------Neural Net Architecture------

        # entradas
        self.input_boards = layers.Input(shape=(self.board_x, self.board_y))    # s: batch_size x board_x x board_y

        # reshape ya que las capas convolucionales esperan un tensor de 4 dimensiones
        x_image = layers.Reshape((self.board_x, self.board_y, 1))(self.input_boards)                # batch_size  x board_x x board_y x 1

        # Convolutional
        h_conv1 = layers.Conv2D(16, 3, padding='same', activation='relu')(x_image)        # batch_size  x board_x x board_y x num_channels
        h_conv2 = layers.Conv2D(32, 3, padding='same', activation='relu')(h_conv1)        # batch_size  x board_x x board_y x num_channels
        h_conv3 = layers.Conv2D(64, 3, padding='same', activation='relu')(h_conv2)       # batch_size  x (board_x) x (board_y) x num_channels
        # h_conv4 = layers.Conv2D(64, 3, padding='valid', activation='relu')(h_conv3)       # batch_size  x (board_x-2) x (board_y-2) x num_channels

        # FC layers
        h_conv4_flat = layers.Flatten()(h_conv3)  # las capas dense esperan un tensor de 2 dimensiones
        s_fc1 = layers.Dropout(args.dropout)(layers.Dense(512, activation='relu')(h_conv4_flat)) # batch_size x 1024
        s_fc2 = layers.Dropout(args.dropout)(layers.Dense(256, activation='relu')(s_fc1))        # batch_size x 1024

        # salidas, necesitamos 2 para la funcion de perdida
        self.pi = layers.Dense(self.action_size, activation='softmax', name='pi')(s_fc2)   # batch_size x self.action_size
        self.v = layers.Dense(1, activation='tanh', name='v')(s_fc2)                    # batch_size x 1

        # Modelo
        self.model = models.Model(inputs=self.input_boards, outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=optimizers.Adam(args.lr))



from .MCTS import MCTS

from .TicTacToeGame import TicTacToeGame
from .netwrapper import ClaseRedNeuronal as NNet



g = TicTacToeGame(3)
net_args = dotdict({
        'lr': 0.001,
        'dropout': 0.3,
        'epochs': 10,
        'batch_size': 64,
        'cuda': False,
        'num_channels': 512,
    })

game = TicTacToeGame(3)
nnet = RedNeuronal(game, net_args)

x, y = game.getBoardSize()
n1 = NNet(nnet, x, y, game.getActionSize(), net_args)
n1.load_checkpoint('./ttoe/ai','best.h5')

args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})

mcts1 = MCTS(g, n1, args1)
ai_player = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

