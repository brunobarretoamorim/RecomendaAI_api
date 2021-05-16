import pandas as pd
import pickle
import random
import sys
from werkzeug.exceptions import HTTPException, BadRequest

class NumeroRespostaIncorreta(HTTPException):
    code = 506
    name = "Numero de respostas incorretas"
    description = 'O valor de competencias informado está incorreto, lembre que são necessários 30 competencias para análise'


class MateriaInvalida(HTTPException):
    code = 507
    name = "Materia invalida"
    description = 'As materias validas são: [CH, CN, LC, MT]'

class ErroCarregarModelo(HTTPException):
    code = 508
    name = "Erro ao carregar modelo"
    description = 'Ocorreu um erro ao carregar o modelo, se o problema persistir favor contatar o administrador'


def carregaBase(materia, respostas = [], *args):

    if materia == ('MT'):
        try:
            modelo = open("modelos/modelo_recsys_mt","rb")
            df = pd.read_parquet("dataset/erroshabilidadesmt_grp.parquet")
        except:
            raise ErroCarregarModelo()
    elif materia == 'CN':
        try:
            modelo = open('modelos/modelo_recsys_cn','rb')
            df = pd.read_parquet('dataset/erroshabilidadescn_grp.parquet')
        except:
            raise ErroCarregarModelo()

    elif materia == 'CH':
        try:
            modelo = open('modelos/modelo_recsys_ch','rb')
            df = pd.read_parquet('dataset/erroshabilidadesch_grp.parquet')
        except:
            raise ErroCarregarModelo()
    elif materia == 'LC':
            try:
                modelo = open('modelos/modelo_recsys_lc','rb')
                df = pd.read_parquet('dataset/erroshabilidadeslc_grp.parquet')
            except:
                raise ErroCarregarModelo()
    else:
        raise MateriaInvalida()

    try:
        lm_new = pickle.load(modelo)
        modelo.close()
        a = pd.DataFrame(respostas).T
        _,index = lm_new.kneighbors(a)
        df_filtrado = df.iloc[index[0]]
        return df_filtrado
    except:
        return "erro"
        #raise Exception()
        #raise NumeroRespostaIncorreta()
        

def retornaHabilidades(x):
    try:
        habilidades_erros = {}
        valores = []
        habilidades = []
        for coluna in x.columns:
            moda = int(x[coluna].mode())
            if moda >= 1:
                habilidades_erros[coluna] = moda
                #valores.append(moda)
                #habilidades.append(coluna)
        return habilidades_erros#(valores,habilidades)
    except:
        return print("Máteria invalida")


def main(materia, respostas):
    df_filtrado = carregaBase(materia, respostas)
    habilidades_dc = retornaHabilidades(df_filtrado)

    return habilidades_dc

