# This file performs a word embedding on base 36 representation of noteOn/Off events at each tick. Each of these base 36
# numbers is analogous to a word in a sentence of a document (here, the document is the song). This word embedding can
# be used to downsample the orginal size of our training data as well as show relationships between the melody and
# accompaniment tracks which will aid the Encoder-Decoder LSTM

import gensim.models
from gensim.models import word2vec
import multiprocessing

cores = multiprocessing.cpu_count()  # to be used to speed up running this neural network
assert gensim.models.word2vec.FAST_VERSION > -1, "This will be painfully slow otherwise"


# Uses a base 36 vector of note events to create a word embedding in word2vec
def sequenceEncoder(noteEvents):
    global model
    model = word2vec.Word2Vec(noteEvents, size=100, window=10, min_count=100, sample=1e-3, iter=10, workers=cores)
    model.train(noteEvents, total_examples=noteEvents.shape[0], epochs=10)

    return model
