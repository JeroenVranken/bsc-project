
class ModelSettings:
    def __init__(self):
        self.activation = 'linear'
        self.lossType = 'mean_squared_error'
        self.hiddenNodes = 512
        self.depth = 3
        self.dropoutAmount = 0.2
        self.l1Amount = 0.01
        self.l2Amount = 0
        self.sequence_size = 32
        self.N_values = 128
        self.N_epochs = 1
        self.filename = ''
        self.resolution = 8
        self.step = 1
        self.batch_size = 240
        # self.directoryPath = '/home/jvranken/Disklavier/only_classical'
        self.trainingset = 'Moonlight_Sonata'
        self.directoryPath = '/home/jvranken/single/moonlight'
        self.convertVelocity = False
        self.smoothDifference = 4
        self.optimizer = 'rmsprop'
        self.generate_length = 256
        self.modelType = 'conv'
        self.genres = False
        self.jazzPath = '/home/jvranken/Disklavier/only_jazz'
        self.classicPath = '/home/jvranken/Disklavier/only_classical'
        self.generateGenre = 'jazz'
    #
    # def perimeter(self):
    #     return 2 * self.x + 2 * self.y
    #
    # def describe(self, text):
    #     self.description = text
    #
    # def authorName(self, text):
    #     self.author = text
    #
    # def scaleSize(self, scale):
    #     self.x = self.x * scale
    #     self.y = self.y * scale