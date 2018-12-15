import gensim.models
from gensim.models import word2vec
from tempfile import mkstemp  # for saving the model
import multiprocessing

cores = multiprocessing.cpu_count()
assert gensim.models.word2vec.FAST_VERSION > -1, "This will be painfully slow otherwise"


# Converts a base36 matrix into a Word2Vec encoded matrix
def sequenceEncoder(matrix, chords):
    model = word2vec.Word2Vec(matrix, size=100, window=500, min_count=100,
                              sample=1e-3, iter=50, workers=cores)
    model.train(chords, total_examples=matrix.shape[0], total_words=1, epochs=10)

    fs, temp_path = mkstemp("gensim_temp")  # creates a temp file

    model.save(temp_path)  # save the model

    return model

#  may want to consider using jupyter notebook here instead
