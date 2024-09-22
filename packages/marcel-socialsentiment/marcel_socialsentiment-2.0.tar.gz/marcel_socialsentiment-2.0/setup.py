from setuptools import setup, find_packages
import codecs
import os
import pandas
import string
import warnings
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



here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
VERSION = '2.0'
DESCRIPTION = 'Library to perform Social Sentiment on Unstructured data'
LONG_DESCRIPTION = 'This library will let get continous scores using SentProp and Densifier Algorithm'


setup(
    name="marcel_socialsentiment",
    version=VERSION,
    author="Marcel Tino",
    author_email="<marceltino92@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['gensim','nltk','numpy','scipy','matplotlib','keras','scikit-learn','tensorflow','pandas'],
    keywords=[])
