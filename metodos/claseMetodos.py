# -*- coding: utf-8 -*-import io
import codecs
import io
import re
import nltk
import numpy as np
from nltk.tokenize import sent_tokenize
import unicodedata
from HTMLParser import HTMLParser
import networkx

from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class claseMetodos:

    def leerArchivo(self, rutaArchivo):
        archivo = io.open(rutaArchivo, "r", encoding="utf-8")
        text = archivo.read()
        archivo.close()

        return text

    def leerArchivo2(self, rutaArchivo):
        text2 = ""

        # archivo = codecs.open(rutaArchivo,"r", encoding='utf-8')
        archivo = io.open(rutaArchivo, "r", encoding="utf-8")
        print archivo.read()

    def similitudCoseno(self):
        print "hola mundo"

    def resumidorTextRank(self):
        print "hola mundo"

    def reumir(self, text):
        res = summarize(text, ratio=0.1)

        print res

        res2 = summarize(text, word_count=100)

        print res2

        print(keywords(ratio=0.1))

    def parse_document(self, document):
        document = re.sub('\n', ' ', document)

        if isinstance(document, str):
            document = document
        elif isinstance(document, unicode):
            return unicodedata.normalize('NFKD', document).encode('ascii', 'ignore')
        else:
            raise ValueError('Document is not string or unicode!')

        document = document.strip()
        sentences = nltk.sent_tokenize(document)
        sentences = [sentence.strip() for sentence in sentences]
        #return sentences

    html_parser = HTMLParser()

    def unescape_html(parser, text):
        return parser.unescape(text)

    # def normalize_corpus(self, corpus, lemmatize=True, tokenize=False):
    #     normalized_corpus = []
    #
    #     for text in corpus:
    #         text = html_parser.unescape(text)
    #         text = expand_contractions(text, CONTRACTION_MAP)
    #         if lemmatize:
    #             text = lemmatize_text(text)
    #         else:
    #             text = text.lower()
    #             text = remove_special_characters(text)
    #             text = remove_stopwords(text)
    #         if tokenize:
    #             text = tokenize_text(text)
    #             normalized_corpus.append(text)
    #         else:
    #             normalized_corpus.append(text)
    #
    #     return normalized_corpus

    def build_feature_matrix(self, documents, feature_type='frequency', ngram_range=(1, 1), min_df=0.0, max_df=1.0):

        feature_type = feature_type.lower().strip()
        #feature_type = feature_type.lower()

        if feature_type == 'binary':
            vectorizer = CountVectorizer(binary=True, min_df=min_df, max_df=max_df, ngram_range=ngram_range)
        elif feature_type == 'frequency':
            vectorizer = CountVectorizer(binary=False, min_df=min_df, max_df=max_df, ngram_range=ngram_range)
        elif feature_type == 'tfidf':
            vectorizer = TfidfVectorizer(min_df=min_df, max_df=max_df, ngram_range=ngram_range)
        else:
            raise Exception("Wrong feature type entered. Possible values:'binary', 'frequency','tfidf'")

        feature_matrix = vectorizer.fit_transform(documents).astype(float)

        #print(vectorizer.get_feature_names())
        #print(feature_matrix.toarray())
        #print ("caracteristicas: ", feature_matrix.shape)

        #train_data_features_res = feature_matrix.toarray()

        #self.mostrarLascaracteristicas(vectorizer, train_data_features_res)

        return vectorizer, feature_matrix

    def mostrarLascaracteristicas(self, Elemtovectorizer, train_data_featuresTmp):
        # Take a look at the words in the vocabulary  Now that the Bag of Words
        # model is trained, let's look at the vocabulary:
        vocab = Elemtovectorizer.get_feature_names()
        print (vocab)

        # If you're interested, you can also print the counts of each word in the vocabulary:
        # Sum up the counts of each vocabulary word
        dist = np.sum(train_data_featuresTmp, axis=0)
        # For each, print the vocabulary word and the number of times it
        # appears in the training set

        for tag, count in zip(vocab, dist):
            print (count, tag)

        print (train_data_featuresTmp.shape)

    def tokenizarTexto(self, textoAResumir):
        #print("hola mundo...")

        listaDeSentencias = []
        listaDeSentencias = sent_tokenize(textoAResumir)

        # listaDeSentencias = [y for x in listaDeSentencias for y in x ]

        #print(listaDeSentencias)

        return listaDeSentencias

    # matriz similitud
    def obtenerMatrizDeSimilitud(self, feature_matrix):

        # construct the document similarity matrix
        similarity_matrix = (feature_matrix * feature_matrix.T)

        #print np.round(similarity_matrix.todense(), 2)

        return similarity_matrix

    def obtenerGrafoDeSimilitud(self, similarity_matrix):

        similarity_graph = networkx.from_scipy_sparse_matrix(similarity_matrix)
        # view the similarity graph
        # networkx.draw_networkx(similarity_graph)

        return similarity_graph

    def algoritmoPageRankPorNumeroSentencias(self, similarity_graph, num_sentences, sentenciasDelTexto):

        scores = networkx.pagerank(similarity_graph)
        ranked_sentences = sorted(((score, index) for index, score in scores.items()), reverse=True)

        # print ranked_sentences
        for elmento in ranked_sentences:
            print elmento

        top_sentence_indices = [ranked_sentences[index][1] for index in range(num_sentences)]
        top_sentence_indices.sort()

        for index in top_sentence_indices:
            print sentenciasDelTexto[index]

    def algoritmoPageRankPorNumeroPalabras(self, similarity_graph, num_palabras, sentenciasDelTexto):

        scores = networkx.pagerank(similarity_graph)
        ranked_sentences = sorted(((score, index) for index, score in scores.items()), reverse=True)

        #print ranked_sentences
        #for elmento in ranked_sentences:
        #    print elmento

        ranked_sentences.sort(reverse=True)

        numP = 0

        resumen = ""
        for i in range(0, len(ranked_sentences)):
            #para mostrar la desde la sentencia mas importante hasta la menos importante
            #print sentenciasDelTexto[ranked_sentences[i][1]]

            if numP <= num_palabras:
                # print "numPal: " +  str(len(sentenciasDelTexto[ranked_sentences[i][1]].split(" ")))
                #print sentenciasDelTexto[ranked_sentences[i][1]]
                numP = numP + len(sentenciasDelTexto[ranked_sentences[i][1]].split(" "))
                resumen = resumen + sentenciasDelTexto[ranked_sentences[i][1]]


        return resumen

        # numpal = 0
        # for index in ranked_sentences:
        #     if numpal <= num_palabras:
        #         print sentenciasDelTexto[index]
        #         numpal = numpal + len(sentenciasDelTexto[index])

    def obtenerMatrizDeSimilitud2(self, sentencias, feature_matrix):

        # construct the document similarity matrix
        similarity_matrix = np.zeros([len(sentencias), len(sentencias)])

        print(similarity_matrix)

        for i in range(len(sentencias)):
            for j in range(len(sentencias)):
                if i != j:
                    similarity_matrix = \
                    cosine_similarity(feature_matrix[i].reshape(1, 100), feature_matrix[j].reshape(1, 100))[0, 0]

        print(similarity_matrix)
        return similarity_matrix

    def textRank(self, textoAResumir):
        print("hola mundo ")
