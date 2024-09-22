import gensim.downloader as api
from nltk.corpus import stopwords
import numpy as np
from scipy import sparse
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
from keras import backend as K
from keras.optimizers import Adam, Optimizer
from keras.regularizers import Regularizer
from keras.constraints import Constraint
from sklearn import preprocessing
from tensorflow.keras import backend as K
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Lambda, Input, multiply, add
from tensorflow.keras.optimizers import Optimizer
from tensorflow.keras.regularizers import Regularizer
from tensorflow.keras.constraints import Constraint
from tensorflow.keras.initializers import Identity
import tensorflow as tf
import nltk
from tensorflow.keras.optimizers import SGD
import pandas as pd

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from gensim.models import Phrases
from gensim.models.phrases import Phraser

    


def load_model(model):
    model=api.load(model)
    return model

def prep_custom_data(text,model):
    text = text.lower()
    new_text = sent_tokenize(text)
    tokenized_sentences = [word_tokenize(sentence) for sentence in new_text]
    
    # Train bigram model
    bigram = Phrases(tokenized_sentences, min_count=1, threshold=2)
    bigram_phraser = Phraser(bigram)
    
    # Apply bigram model
    bigram_sentences = [bigram_phraser[sentence] for sentence in tokenized_sentences]
    
    total_tokens = []
    for i in bigram_sentences:
        for j in i:
            total_tokens.append(j)
    
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    final_tokens = [w for w in total_tokens if not w.lower() in stop_words]
    
    special_words= [word for word in final_tokens if "_" in word]
    processed_data=[]
    for elem in final_tokens:
        processed_data.append(elem)
    
    # Define the punctuation to remove
    punctuation_to_remove = {",", "."}
    
    # Remove punctuation tokens
    processed_data = [word for word in processed_data if word not in punctuation_to_remove]
    
    filtered_words = [word for word in processed_data if word in model.key_to_index]
    embeddings = np.array([model[word] for word in filtered_words])
    words = filtered_words
    word_to_index = {word: idx for idx, word in enumerate(filtered_words)}
    return embeddings,words,word_to_index
        
#==================================================================



def prep_seed_words(positive_seeds,negative_seeds,word_to_index,model):
    positive_seeds = [element.lower() for element in positive_seeds]
    negative_seeds = [element.lower() for element in negative_seeds]
    
    # Identify missing positive seeds
    missing_positive_seeds = [word for word in positive_seeds if word not in word_to_index]
    # Identify missing negative seeds
    missing_negative_seeds = [word for word in negative_seeds if word not in word_to_index]
    
    positive_seeds = [word for word in positive_seeds if word in word_to_index]
    negative_seeds = [word for word in negative_seeds if word in word_to_index]
    
    # Print out missing seeds
    if missing_positive_seeds:
        print(f"Missing positive seeds: {missing_positive_seeds}")
    if missing_negative_seeds:
        print(f"Missing negative seeds: {missing_negative_seeds}")
    # If there are missing seeds, raise an error
    if missing_positive_seeds or missing_negative_seeds:
        print("Some seed words are not in the vocabulary.")

    # For each missing seed word, find similar words in the vocabulary
    for word in missing_positive_seeds + missing_negative_seeds:
        if word in model:
            similar_words = model.most_similar(word, topn=10)
            print(f"Words similar to '{word}': {[w for w, _ in similar_words]}")
        else:
            print(f"Word '{word}' is not in the model vocabulary. Cannot find similar words.")
            
    overall_missing_seeds=missing_negative_seeds+missing_positive_seeds
    if overall_missing_seeds is None:
        overall_missing_seeds.insert("No issues with the seeds") 
        overall_missing_seeds
    return overall_missing_seeds




def similarity_matrix(embeddings, arccos=False, similarity_power=1, nn=25, **kwargs):
    """
    Constructs a similarity matrix from embeddings.
    nn argument controls the degree.
    """
    def make_knn(vec, nn=nn):
        vec[vec < vec[np.argsort(vec)[-nn]]] = 0
        return vec
    L = embeddings.dot(embeddings.T)
    if sparse.issparse(L):
        L = L.todense()
    if arccos:
        L = np.arccos(np.clip(-L, -1, 1)) / np.pi
    else:
        L += 1
    np.fill_diagonal(L, 0)
    L = np.apply_along_axis(make_knn, 1, L)
    return L ** similarity_power

def wordnet_similarity_matrix(words, word_to_index):
    """
    Makes a similarity matrix from WordNet.
    """
    vocab_size = len(words)
    sim_mat = np.zeros((vocab_size, vocab_size))
    words_morphy = {word: wn.morphy(word) for word in words}
    lemmas = {lemma: word for word, lemma in words_morphy.items()}
    for i, word in enumerate(words):
        if words_morphy[word] is None:
            continue
        synonyms = set(chain.from_iterable([syn.lemma_names()
                                            for syn in wn.synsets(words_morphy[word])]))
        for syn_word in synonyms:
            if syn_word in lemmas:
                sim_mat[word_to_index[word], word_to_index[lemmas[syn_word]]] = 1.0
    print(np.sum(sim_mat))
    np.fill_diagonal(sim_mat, 0)
    return sim_mat

def run_iterative(M, r, update_seeds, max_iter=50, epsilon=1e-6, **kwargs):
    for i in range(max_iter):
        last_r = np.array(r)
        r = np.dot(M, r)
        update_seeds(r)
        if np.abs(r - last_r).sum() < epsilon:
            break
    return r

def teleport_set(words, seeds):
    return [i for i, w in enumerate(words) if w in seeds]

def weighted_teleport_set(words, seed_weights):
    return np.array([seed_weights[word] if word in seed_weights else 0.0 for word in words])

def transition_matrix(embeddings, words=None, word_to_index=None, word_net=False, first_order=False, sym=False, trans=False, **kwargs):
    """
    Build a probabilistic transition matrix from word embeddings.
    """
    if word_net:
        if words is None or word_to_index is None:
            raise ValueError("words and word_to_index must be provided when word_net=True")
        L = wordnet_similarity_matrix(words, word_to_index)
    elif not first_order:
        L = similarity_matrix(embeddings, **kwargs)
    else:
        L = embeddings  # Assuming embeddings is the adjacency matrix in first-order case
    if sym:
        Dinv = np.diag([1.0 / np.sqrt(L[i].sum()) if L[i].sum() > 0 else 0 for i in range(L.shape[0])])
        L = Dinv.dot(L).dot(Dinv)
    else:
        Dinv = np.diag([1.0 / L[i].sum() if L[i].sum() > 0 else 0 for i in range(L.shape[0])])
        L = L.dot(Dinv)
    if trans:
        return L.T
    return L

def random_walk(embeddings, words, word_to_index, positive_seeds, negative_seeds, beta=0.9, **kwargs):
    """
    Learns polarity scores via random walks with teleportation to seed sets.
    Main method used in paper.
    """
    def run_random_walk(M, teleport, beta, **kwargs):
        def update_seeds(r):
            r += (1 - beta) * teleport / np.sum(teleport)
        return run_iterative(M * beta, np.ones(M.shape[1]) / M.shape[1], update_seeds, **kwargs)

    if not isinstance(positive_seeds, dict):
        positive_seeds = {word: 1.0 for word in positive_seeds}
        negative_seeds = {word: 1.0 for word in negative_seeds}
    M = transition_matrix(embeddings, words=words, word_to_index=word_to_index, **kwargs)
    rpos = run_random_walk(M, weighted_teleport_set(words, positive_seeds), beta, **kwargs)
    rneg = run_random_walk(M, weighted_teleport_set(words, negative_seeds), beta, **kwargs)
    return {w: rpos[i] / (rpos[i] + rneg[i]) for i, w in enumerate(words)}

def label_propagate_continuous(embeddings, positive_seeds, negative_seeds, **kwargs):
    """
    Learns polarity scores via standard label propagation from seed sets.
    One walk for both labels, continuous non-normalized scores.
    """
    #words = embeddings.iw
    M = transition_matrix(embeddings, **kwargs)
    pos, neg = teleport_set(words, positive_seeds), teleport_set(words, negative_seeds)
    def update_seeds(r):
        r[pos] = 1
        r[neg] = -1
    r = run_iterative(M, np.zeros(M.shape[0]), update_seeds, **kwargs)
    return {w: r[i] for i, w in enumerate(words)}


def load_pickle(fname):
    with open(fname, 'rb') as f:  # Use 'rb' mode for reading binary files
        return pickle.load(f)

def lines(fname):
    with open(fname) as f:
        for line in f:
            yield line


class Embedding:
    """
    Base class for all embeddings. SGNS can be directly instantiated with it.
    """

    def __init__(self, vecs, vocab, normalize=True, **kwargs):
        self.m = vecs  # The NumPy array of embeddings
        self.dim = self.m.shape[1]  # Dimension of each embedding
        self.iw = vocab  # List of words in vocabulary
        self.wi = {w: i for i, w in enumerate(self.iw)}  # Word to index mapping
        if normalize:
            self.normalize()

    def __getitem__(self, key):
        if self.oov(key):
            raise KeyError(f"Word '{key}' is out of vocabulary.")
        return self.represent(key)

    def oov(self, w):
        return w not in self.wi

    def represent(self, w):
        if w in self.wi:
            return self.m[self.wi[w]]
        else:
            return np.zeros(self.dim)  # Return zero vector for out-of-vocabulary words

    def __iter__(self):
        return self.iw.__iter__()

    def __contains__(self, key):
        return not self.oov(key)

    @classmethod
    def load(cls, path, normalize=True, add_context=True, **kwargs):
        mat = np.load(path + "-w.npy")
        if add_context:
            mat += np.load(path + "-c.npy")
        iw = load_pickle(path + "-vocab.pkl")
        return cls(mat, iw, normalize) 

    def get_subembed(self, word_list, **kwargs):
        word_list = [word for word in word_list if not self.oov(word)]
        keep_indices = [self.wi[word] for word in word_list]
        return Embedding(self.m[keep_indices, :], word_list, normalize=False)

    def reindex(self, word_list, **kwargs):
        new_mat = np.empty((len(word_list), self.m.shape[1]))
        valid_words = set(self.iw)
        for i, word in enumerate(word_list):
            if word in valid_words:
                new_mat[i, :] = self.represent(word)
            else:
                new_mat[i, :] = 0 
        return Embedding(new_mat, word_list, normalize=False)

    def get_neighbourhood_embed(self, w, n=1000):
        neighbours = self.closest(w, n=n)
        keep_indices = [self.wi[neighbour] for _, neighbour in neighbours] 
        new_mat = self.m[keep_indices, :]
        return Embedding(new_mat, [neighbour for _, neighbour in neighbours]) 

    def normalize(self):
        preprocessing.normalize(self.m, copy=False)

    def oov(self, w):
        return not (w in self.wi)

    def represent(self, w):
        if w in self.wi:
            return self.m[self.wi[w], :]
        else:
            print("OOV: ", w)
            return np.zeros(self.dim)

    def similarity(self, w1, w2):
        """
        Assumes the vectors have been normalized.
        """
        sim = self.represent(w1).dot(self.represent(w2))
        return sim

    def closest(self, w, n=10):
        """
        Assumes the vectors have been normalized.
        """
        scores = self.m.dot(self.represent(w))
        return heapq.nlargest(n, zip(scores, self.iw))
    

class SVDEmbedding(Embedding):
    """
    SVD embeddings.
    Enables controlling the weighted exponent of the eigenvalue matrix (eig).
    Context embeddings can be created with "transpose".
    """
    
    def __init__(self, path, normalize=True, eig=0.0, **kwargs):
        ut = np.load(path + '-u.npy')
        s = np.load(path + '-s.npy')
        vocabfile = path + '-vocab.pkl'
        self.iw = load_pickle(vocabfile)
        self.wi = {w:i for i, w in enumerate(self.iw)}
 
        if eig == 0.0:
            self.m = ut
        elif eig == 1.0:
            self.m = s * ut
        else:
            self.m = np.power(s, eig) * ut

        self.dim = self.m.shape[1]

        if normalize:
            self.normalize()

class GigaEmbedding(Embedding):
    def __init__(self, path, words, dim=300, normalize=True, **kwargs):
        seen = []
        vs = {}
        for line in lines(path):
            split = line.split()
            w = split[0]
            if w in words:
                seen.append(w)
                vs[w] = np.array(map(float, split[1:]), dtype='float32')
        self.iw = seen
        self.wi = {w:i for i,w in enumerate(self.iw)}
        self.m = np.vstack(vs[w] for w in self.iw)
        if normalize:
            self.normalize()


class SimpleSGD(Optimizer):
    def __init__(self, learning_rate=5.0, momentum=0., decay=0.,
                 nesterov=False, **kwargs):
        super(SimpleSGD, self).__init__(name="SimpleSGD", **kwargs)
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.decay = decay
        self.nesterov = nesterov

    def get_config(self):
        config = super(SimpleSGD, self).get_config()
        config.update({
            'learning_rate': self.learning_rate,
            'momentum': self.momentum,
            'decay': self.decay,
            'nesterov': self.nesterov
        })
        return config

    def _create_slots(self, var_list):
        for var in var_list:
            self.add_slot(var, 'momentum')

    @tf.function
    def _resource_apply_dense(self, grad, var):
        var_dtype = var.dtype.base_dtype
        lr = tf.cast(self.learning_rate, var_dtype)
        mom = tf.cast(self.momentum, var_dtype)

        if self.nesterov:
            # Nesterov accelerated gradient
            m = self.get_slot(var, 'momentum')
            m_t = m.assign(m * mom - lr * grad)
            var.assign_add(m * mom - lr * grad)
        else:
            # Standard momentum
            m = self.get_slot(var, 'momentum')
            m_t = m.assign(m * mom - lr * grad)
            var.assign_add(m_t)
            
class Orthogonal(Constraint):
    def __call__(self, w):
        s, u, v = tf.linalg.svd(w)
        return tf.matmul(u, tf.transpose(v))

    def get_config(self):
        return {}

class OrthogonalRegularizer(Regularizer):
    def __init__(self, strength=0.):
        self.strength = strength

    def __call__(self, x):
        identity = tf.eye(tf.shape(x)[0])
        xxt = tf.matmul(x, x, transpose_b=True)
        return self.strength * tf.reduce_sum(tf.square(xxt - identity))

    def get_config(self):
        return {'strength': self.strength}

def orthogonalize(Q):
    s, u, v = np.linalg.svd(Q)
    return u.dot(v)

class DatasetMinibatchIterator:
    def __init__(self, embeddings, positive_seeds, negative_seeds, batch_size=512, **kwargs):
        self.words, embeddings1, embeddings2, labels = [], [], [], []

        def add_examples(word_pairs, label):
            for w1, w2 in word_pairs:
                embeddings1.append(embeddings[w1])
                embeddings2.append(embeddings[w2])
                labels.append(label)
                self.words.append((w1, w2))

        add_examples(combinations(positive_seeds, 2), 1)
        add_examples(combinations(negative_seeds, 2), 1)
        add_examples(product(positive_seeds, negative_seeds), -1)
        self.e1 = np.vstack(embeddings1)
        self.e2 = np.vstack(embeddings2)
        self.y = np.array(labels)

        self.batch_size = batch_size
        self.n_batches = (self.y.size + self.batch_size - 1) // self.batch_size

    def shuffle(self):
        perm = np.random.permutation(np.arange(self.y.size))
        self.e1, self.e2, self.y, self.words = \
            self.e1[perm], self.e2[perm], self.y[perm], [self.words[i] for i in perm]

    def __iter__(self):
        for i in range(self.n_batches):
            batch = np.arange(i * self.batch_size, min(self.y.size, (i + 1) * self.batch_size))
            yield {
                'embeddings1': self.e1[batch],
                'embeddings2': self.e2[batch],
                'y': self.y[batch][:, np.newaxis]
            }

def get_model(inputdim, outputdim, regularization_strength=0.01, lr=0.0001, cosine=False, **kwargs):
    # Define inputs
    embeddings1_input = Input(shape=(inputdim,), name='embeddings1')
    embeddings2_input = Input(shape=(inputdim,), name='embeddings2')

    # Shared transformation layer with orthogonal constraint
    transformation = Dense(
        inputdim,
        kernel_initializer=Identity(),
        kernel_constraint=Orthogonal(),
        use_bias=False,
        kernel_regularizer=OrthogonalRegularizer(strength=regularization_strength),
        name='transformation'
    )

    # Apply transformation
    transformed1 = transformation(embeddings1_input)
    transformed2 = transformation(embeddings2_input)

    # Project to output dimension
    projected1 = Lambda(lambda x: x[:, :outputdim], name='projected1')(transformed1)
    negprojected2 = Lambda(lambda x: -x[:, :outputdim], name='negprojected2')(transformed2)

    if cosine:
        # Normalize vectors
        normalized1 = Lambda(lambda x: tf.nn.l2_normalize(x, axis=1), name='normalized1')(projected1)
        negnormalized2 = Lambda(lambda x: tf.nn.l2_normalize(x, axis=1), name='negnormalized2')(negprojected2)
        # Element-wise multiplication
        multiplied = multiply([normalized1, negnormalized2], name='multiplied')
        # Sum over the features
        distances = Lambda(lambda x: tf.reduce_sum(x, axis=1, keepdims=True), name='distances')(multiplied)
    else:
        # Sum of squares
        summed = add([projected1, negprojected2], name='summed')
        distances = Lambda(lambda x: tf.sqrt(tf.reduce_sum(tf.square(x), axis=1, keepdims=True)), name='distances')(summed)

    # Define model
    model = Model(inputs=[embeddings1_input, embeddings2_input], outputs=distances)

    # Custom loss function
    def custom_loss(y_true, y_pred):
        return K.mean(y_true * y_pred)

    # Use built-in SGD optimizer
    optimizer = SGD(learning_rate=lr, momentum=0., decay=0., nesterov=False)
    model.compile(loss=custom_loss, optimizer=optimizer)

    return model

def apply_embedding_transformation(embeddings, positive_seeds, negative_seeds,
                                   n_epochs=5, n_dim=10, force_orthogonal=False,
                                   plot=False, plot_points=50, plot_seeds=False,
                                   **kwargs):
    print("Preparing to learn embedding transformation")
    dataset = DatasetMinibatchIterator(embeddings, positive_seeds, negative_seeds, **kwargs)
    model = get_model(embeddings.m.shape[1], n_dim, **kwargs)

    print("Learning embedding transformation")
    for epoch in range(n_epochs):
        dataset.shuffle()
        loss = 0
        for i, X in enumerate(dataset):
            embeddings1_batch = X['embeddings1']
            embeddings2_batch = X['embeddings2']
            y_batch = X['y']
            batch_loss = model.train_on_batch([embeddings1_batch, embeddings2_batch], y_batch)
            loss += batch_loss * y_batch.size

            # Get and set weights if force_orthogonal is True
            if force_orthogonal:
                weights = model.get_layer('transformation').get_weights()[0]
                Q = orthogonalize(weights)
                model.get_layer('transformation').set_weights([Q])

        print(f"Epoch {epoch + 1}/{n_epochs}, Loss: {loss / dataset.y.size}")

    # Get the final transformation matrix
    Q = model.get_layer('transformation').get_weights()[0]
    new_mat = embeddings.m.dot(Q)[:, 0:n_dim]

    # [Plotting code remains the same, or can be commented out if not needed]

    return Embedding(new_mat, embeddings.iw, normalize=n_dim != 1)

    
def densify(embeddings, positive_seeds, negative_seeds, 
        transform_method= apply_embedding_transformation, **kwargs):
    """
    Learns polarity scores via orthogonally-regularized projection to one-dimension
    Adapted from: http://arxiv.org/pdf/1602.07572.pdf
    """
    positive_seeds = [element.lower() for element in positive_seeds]
    negative_seeds = [element.lower() for element in negative_seeds]
    
    p_seeds = {word:1.0 for word in positive_seeds}
    n_seeds = {word:1.0 for word in negative_seeds}
    new_embeddings = embeddings
    new_embeddings = apply_embedding_transformation(
            embeddings, p_seeds, n_seeds, n_dim=1,  **kwargs)
    polarities = {w:new_embeddings[w][0] for w in embeddings.iw}
    return polarities



def view_scores(words,sentprop_continous_scores,densify_polarity_scores):
    pol_list=[]
    for word in words:
        pol_list.append([word,sentprop_continous_scores[word]])
    
    sorted_data = sorted(pol_list, key=lambda x: x[1])
    top_5 = sorted_data[-5:]
    bottom_5 = sorted_data[:5]
    
    print("sentprop")
    print("top5 \n",top_5)
    print("bottom5 \n",bottom_5)
    
    den_pol_list=[]
    for word in words:
        den_pol_list.append([word,densify_polarity_scores[word]])

    sorted_data = sorted(den_pol_list, key=lambda x: x[1])
    top_50 = sorted_data[-50:]
    bottom_50 = sorted_data[:50]

    print("densify")
    print("top5 \n",top_50)
    print("bottom5 \n",bottom_50)
    df1 = pd.DataFrame(den_pol_list, columns=['Word', ' Densifier Score'])
    df2 = pd.DataFrame(pol_list, columns=['Word', 'SentProp Score'])
    df_combined = pd.merge(df1, df2, on='Word', how='outer')
    return df_combined








