import numpy as np
import os

class ClaseRedNeuronal():
    def __init__(self, nnet, x, y, action_size, args):
        self.args = args

        # cargar la red neuronal
        # self.nnet = RedNeuronal(game, self.args)
        self.nnet = nnet

        # mostrar la arquitectura del modelo
        # print(self.nnet.model.summary())

        # inicializar el juego
        # self.board_x, self.board_y = game.getBoardSize()
        # self.action_size = game.getActionSize()
        self.board_x = x
        self.board_y = y
        self.action_size = action_size

    def train(self, examples):
        input_boards, target_pis, target_vs = list(zip(*examples))

        # imprimir para revisar los datos
        print('input_board', input_boards[0])
        print('target_pis', target_pis[0])
        print('target_vs', target_vs[0])

        # entrenar el modelo en base al historial de partidas
        input_boards = np.asarray(input_boards)
        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)
        self.nnet.model.fit(x = input_boards, y = [target_pis, target_vs], batch_size = self.args.batch_size, epochs = self.args.epochs)

    def predict(self, board):
        """Este método es el que se usa en cada nodo del arbol de búsqueda para obtener las probabilidades de cada acción"""
        # preparing input
        board = board[np.newaxis, :, :]

        # run
        pi, v = self.nnet.model.predict(board, verbose=False)
        return pi[0], v[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        """Requerido por el framework para guardar los modelos que se van generando a lo largo del entrenamiento"""
        # change extension
        filename = filename.split(".")[0] + ".h5"

        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Creando directorio {}".format(folder))
            os.mkdir(folder)
        self.nnet.model.save_weights(filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        """Requerido por la librería para cargar el modelo que se va a usar para jugar"""
        # change extension
        filename = filename.split(".")[0] + ".h5"
        filepath = os.path.join(folder, filename)
        print('buscando en el path', filepath)
        if not os.path.exists(filepath):
            raise("No se encuentra el modelo '{}'".format(filepath))
        self.nnet.model.load_weights(filepath)