# -*- coding: utf-8 -*-
import sys
import io

from metodos.claseMetodos import claseMetodos
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords


#Plain text parsers since we are parsing through text


from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer



if __name__ == '__main__':
    rutaArchivo = "C:\Users\Caren\Desktop\utilierias_archivos\Desarrollos\Python\TextRank\TextoFuente11.txt"
    #rutaArchivo = "C:/Users/Caren/Desktop/utilierias_archivos/Desarrollos/pruevasTesis/6.-CTR/textos fuente sin formatear/extracciondeCaracteristicas.txt"
    obj = claseMetodos()
    #obj2 = ManejodeArchivos(ruta,"utf-8")

    #apertura del archivo
    with open(rutaArchivo, "r"  ) as archivo:
        texto = archivo.read()

    #archicoResumenTRM = io.open("C:/Users/Caren/Desktop/utilierias_archivos/Desarrollos/pruevasTesis/6.-CTR\RESUMGENTR/RATextRankM10_.txt", "w", encoding="utf-8")
    #archicoResumenTRG = io.open("C:/Users/Caren/Desktop/utilierias_archivos/Desarrollos/pruevasTesis/6.-CTR\RESUMGENTR/RATextRankG10_.txt", "w", encoding="utf-8")
    #print texto

    RATextRankM = io.open("RATextRankM.txt", "w", encoding="utf-8")
    RATextRankG = io.open("RATextRankG.txt", "w", encoding="utf-8")

    #formato del texto
    texto = unicode(texto, errors='ignore')

    #eliminacion de saltos de linea
    textoLimpio = obj.parse_document(texto)
    #print textoLimpio

    sentenciasDelTexto = obj.tokenizarTexto(textoLimpio)
    #print sentenciasDelTexto
                                                                            #binary , frequency , tfidf
    vectorizer, feature_matrix = obj.build_feature_matrix(sentenciasDelTexto, feature_type='tfidf ', ngram_range=(1, 1))
    #print feature_matrix

    similarity_matrix = obj.obtenerMatrizDeSimilitud(feature_matrix)
    #print similarity_matrix

    similarity_graph = obj.obtenerGrafoDeSimilitud(similarity_matrix)

    #num_sentences = 2
    #ranked_sentences = obj.algoritmoPageRankPorNumeroSentencias(similarity_graph,num_sentences,sentenciasDelTexto)

    print("-----------------------")
    num_palabras = 100

    resumen1 = obj.algoritmoPageRankPorNumeroPalabras(similarity_graph, num_palabras, sentenciasDelTexto)
    print  resumen1
    RATextRankM.write(resumen1)
    #resumen1.write(resumen1)
    print("-----------------------")


    #resumidor de la libreria gensim
    resumen2 = summarize(textoLimpio, word_count=100)
    print resumen2
    RATextRankG.write(resumen2)
    #resumen1.write(str(resumen2).decode("utf-8"))

    RATextRankM.close()
    RATextRankG.close()

    #para sacar palabras clave
    # print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>><"+keywords(str(texto),ratio=0.07))
    # print(resumen)

    #resumidores de la libreria sumy

    # print " funcional en idioma ingles ------------------------------------------------------------------------------------------------------------"
    #
    # parser = PlaintextParser.from_file(rutaArchivo, Tokenizer("english"))
    #
    # sumLexRank = LexRankSummarizer()
    # sumTexRank = TextRankSummarizer()
    # sumLsa     = LsaSummarizer()
    # sumLuhn    = LuhnSummarizer()
    #
    # resumen1 = sumTexRank(parser.document,sentences_count=5)
    # print  resumen1
    # print "------------------------------------------------------------------------------------------------------------"
    # resumen2 = sumLexRank(parser.document, sentences_count=5)
    # print  resumen2
    # print "------------------------------------------------------------------------------------------------------------"
    # resumen3 = sumLsa(parser.document, sentences_count=5)
    # print  resumen3
    # print "------------------------------------------------------------------------------------------------------------"
    # resumen4 = sumLuhn(parser.document, sentences_count=5)
    # print  resumen4