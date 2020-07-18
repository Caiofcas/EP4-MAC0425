import pandas as pd
from collections import namedtuple
import re

Exame = namedtuple('Exame', 'nome analito resultado unidade valref data')

# ---- Auxiliary Functions ----------------------


def is_float_try(entry):
    entry.replace(',', '.')
    try:
        float(entry)
        return True
    except ValueError:
        return False


def fix_encoding(string):
    if type(string) != str:
        return string

    return string \
        .replace('ĂĄ', 'á') \
        .replace('ĂŞ', 'ê') \
        .replace('Ăł', 'ó') \
        .replace('ĂŁ', 'ã') \
        .replace('ĂŠ', 'é') \
        .replace('Ă§', 'ç') \
        .replace('Ă', 'í')  \
        .replace('í˘', 'â') \
        .replace('í', 'Ã') \
        .replace('í', 'Á') \
        .replace('í', 'í') \
        .replace('í­', 'í') # Tem um caracter escondido aqui

def split_exam(row, analito_options, new_exams, default):
    for i in range(len(analito_options)):
        if analito_options[i] in row['Analito']:
            row['Exame'] = new_exams[i]
            return row

    row['Exame'] = default
    return row

# ---- Join Data Functions ----------------------


def join_exames():

    print("Starting processing exames")

    fleury_e_big = pd.read_csv(
        'dados_originais/Grupo_Fleury_Dataset_Covid19_Resultados_Exames.csv',
        sep='|', encoding='latin1')
    einstein_e_big = pd.read_csv(
        'dados_originais/einstein_full_dataset_exames.csv', sep='|')
    hsl_e_big = pd.read_csv('dados_originais/hsl_lab_result_1.csv', sep='|')

    einstein_e_big.columns = fleury_e_big.columns
    hsl_e_big['Hospital'] = 'HSL'
    einstein_e_big['Hospital'] = 'Einstein'
    fleury_e_big['Hospital'] = 'Fleury'
    exames = pd.concat([einstein_e_big, fleury_e_big, hsl_e_big])

    exames.columns = ['ID_Paciente', 'Data_Coleta', 'Origem', 'Exame',
                      'Analito', 'Resultado', 'Unidade', 'Valor_Referencia',
                      'Hospital', 'ID_Atendimento']
    print("Joined Exames")
    exames = exames.dropna(subset=['Exame'])

    # Only takes exams related with COVID19
    exames = exames[exames.Exame.str.match('.*(COVID|SARS-CoV-2).*') == True]

    print("Filtered exam types")

    exames = exames.applymap(fix_encoding)

    print("Fixed enconding in Exames")

    exames.loc[(exames.Exame == 'COVID-19-Teste Rápido (IgM e IgG), soro') |
               (exames.Exame == 'Teste rápido COVID19 IgG/IgM') |
               (exames.Exame == 'Teste rápido Coronavirus COVID19 IgG/IgM') |
               (exames.Exame == 'SARS-CoV-2, ANTICORPOS IgM E IgG, TESTE RÁPIDO'),
               'Exame'] = 'Teste rápido COVID19 IgG IgM'

    exames.loc[(exames.Exame == 'NOVO CORONAVÍRUS 2019 (SARS-CoV-2), DETECÇÃO POR PCR') |
               (exames.Exame == 'HMVSC-AFIP PCR COVID 19') |
               (exames.Exame == 'COVID-19-PCR para SARS-COV-2, Vários Materiais (Fleury)'),
               'Exame'] = 'COVID19 PCR'

    exames.loc[(exames.Exame == 'Sorologia SARS-CoV-2/COVID19 IgG/IgM') |
               (exames.Exame == 'COVID-19-Sorologia IgM e IgG por quimiluminescência, soro'),
               'Exame'] = 'Soro COVID19 IgG IgM'

    exames.loc[(exames.Exame == 'COVID-19, anticorpos IGA e IGG, soro'),
               'Exame'] = 'Soro COVID19 IgA IgG'

    exames.loc[(exames.Exame == 'COVID19, ANTICORPOS IgG, soro'),
               'Exame'] = 'Soro COVID19 IgG'

    exames.loc[(exames.Exame == 'COVID19, ANTICORPOS IgA, soro') |
               (exames.Exame == 'Anticorpos IgA contra SARS-CoV-2/COVID19'),
               'Exame'] = 'Soro COVID19 IgA'

    exames.loc[exames.Exame == 'COVID19, ANTICORPOS IgM, soro',
               'Exame'] = 'Soro COVID19 IgM'

    # quase certeza que isso tá escrito errado
    print("Standartized exam types")

    cond = exames.Exame.str.match('Soro COVID19 IgG IgM') == True

    exames.loc[cond] = exames[cond].apply(split_exam, axis=1,
                                          args=[['IgG', 'IgM'],
                                                ['Soro COVID19 IgG',
                                                 'Soro COVID19 IgM'],
                                                'Soro COVID19'])

    cond = exames.Exame.str.match('Soro COVID19 IgA IgG') == True

    exames.loc[cond] = exames[cond].apply(split_exam, axis=1,
                                          args=[['IgA e IgG', 'IgA', 'IgG'],
                                                ['Soro COVID19 IgA e IgG',
                                                 'Soro COVID19 IgA',
                                                 'Soro COVID19 IgG'],
                                                'Soro COVID19'])

    cond = exames.Exame.str.match('Teste rápido COVID19 IgG IgM') == True

    exames.loc[cond] = exames[cond].apply(split_exam, axis=1,
                                          args=[['IgM/IgG', 'IgG', 'IgM'],
                                                ['Teste rápido COVID19 IgG e IgM',
                                                 'Teste rápido COVID19 IgG',
                                                 'Teste rápido COVID19 IgM'],
                                                'Teste rápido COVID19'])
    print("Split compounded Exams")

    exames.to_csv('dados/exames.csv', mode='w+', index=False,
                  columns=['ID_Paciente', 'Data_Coleta', 'Origem', 'Exame',
                           'Analito', 'Resultado', 'Unidade',
                           'Valor_Referencia', 'Hospital'])

    print("Finished writing exames.csv")


def join_pacientes():

    print("Starting processing patients")

    # read csv files
    einstein_p_big = pd.read_csv(
        'dados_originais/einstein_full_dataset_paciente.csv', sep='|')
    fleury_p_big = pd.read_csv(
        'dados_originais/Grupo_Fleury_Dataset_Covid19_Pacientes.csv', sep='|')
    hsl_p_big = pd.read_csv('dados_originais/hsl_patient_1.csv', sep='|')

    # padronize columns
    fleury_p_big.columns = einstein_p_big.columns
    hsl_p_big['Hospital'] = 'HSL'
    einstein_p_big['Hospital'] = 'Einstein'
    fleury_p_big['Hospital'] = 'Fleury'

    pacientes = pd.concat([einstein_p_big, fleury_p_big, hsl_p_big])
    pacientes.columns = ['ID_Paciente', 'Sexo', 'Ano_Nascimento', 'País', 'UF',
                         'Município', 'CEP', 'Hospital']

    pacientes.to_csv('dados/pacientes.csv', mode='w+', index=False,
                     columns=['ID_Paciente', 'Sexo',
                              'Ano_Nascimento', 'Hospital'])
    print("Finished writing pacientes.csv")


# ---- Input Creation Functions -----------------

def pac_dict(filename="dados/pacientes.csv"):
    df = pd.read_csv(filename)
    d = {}
    for _, row in df.iterrows():
        if d.get(row['ID_Paciente']) is None:
            d[row['ID_Paciente']] = (row['Sexo'], row['Ano_Nascimento'])
        else:
            print("porra tem conflito de ID")
    return d


def exam_dict(filename="dados/exames.csv"):
    df = pd.read_csv(filename)
    d = {}
    for _, row in df.iterrows():
        val = d.get(row['ID_Paciente'])
        if val is None:
            val = [
                Exame(row['Exame'],
                      row['Analito'],
                      row['Resultado'],
                      row['Unidade'],
                      row['Valor_Referencia'],
                      row['Data_Coleta'])
            ]
        else:
            val.append(
                Exame(row['Exame'],
                      row['Analito'],
                      row['Resultado'],
                      row['Unidade'],
                      row['Valor_Referencia'],
                      row['Data_Coleta'])
            )
        d[row['ID_Paciente']] = val

        # gambiarration
    d['fields'] = df.Exame.unique()
    return d


def get_fields(exames):

    fields = ["ID_Paciente", "Sexo", "Ano_Nasc"]
    for name in exames:
        fields += ['['+name+']_analito',
                   '['+name+']_resultado',
                   '['+name+']_unidade',
                   '['+name+']_datacol',
                   '['+name+']_valref'
                   ]

    return fields


def get_pac_row(info, exams):
    row = {}
#     row['ID_Paciente'] = p_id
    row['Sexo'] = info[0]
    row['Ano_Nasc'] = info[1]

    for ex in exams:
        if is_float_try(ex.resultado):
            key = ex.nome + ' NUM'
            row[key] = float(ex.resultado)
        else:
            key = ex.nome + ' BOOL'
            row[key] = exam_result(ex.resultado)

    return row


def exam_result(resultado):
    #     print(exam)
    DEBUG = True
    res = 'xxxxx'
    matchNegativo = r'negativo|não|fraco|sem evidência|indetectável'
    # Esse caso ta pegando aquele textão absurdo, melhor filtrar
    matchInconclusivo = r'indeterminado|inconclusivo|repetir o teste|aguardar|a critério|possível'
    matchPositivo = r'reagente|detectado.*|detectável|evidência'
    matchNumerico = r'(\d)+(,|\.)(\d)+'
    matchLixo=r'swab|raspado|nasofaringe|laringe|plasma|bronquico|sangue|secreção|traqueal|Nova Coleta|soro|liquor|trato respiratório|lavado|(\*)+|( ){2,}'
    tests = (['INCONCLUSIVO', matchInconclusivo],['NEGATIVO', matchNegativo],  \
        ['POSITIVO', matchPositivo], ['numerico', matchNumerico], \
            ['lixo', matchLixo])

    for test in tests: 
        regexResultado = re.search(test[1], resultado, flags=re.IGNORECASE)
        if regexResultado is not None:
            if test[0] != 'lixo' and test[1] != 'numerico':
                res = test[0]
            if DEBUG:
                try:
                    file_to_open = test[0] + ".txt"
                    file_target = open(file_to_open, "a")
                    file_target.write(resultado)
                    file_target.write('\n')
                    file_target.close()
                except:
                    print('erro na hora de abrir o arquivo')
            break #Interrompe os testes por ter classificado a palavra
    
    print('Palavra {} classificada como {}'.format(resultado, res))
    return res


def create_input():

    print("Creating input csv")

    # Construir dict com sexo e nasc

    sexo_e_nascimento = pac_dict()

    print("Processed pacientes")

    # Construct Exam dict

    exames_dict = exam_dict()

    print("Processed exames")

    # Constroi fields

    # fields = get_fields(exames_dict['fields'])

    # Construct data

    new_rows = []
    for pac_id in sexo_e_nascimento.keys():

        pac_info = sexo_e_nascimento[pac_id]
        pac_exames = exames_dict.get(pac_id)

        if pac_exames is not None:
            new_rows.append(get_pac_row(pac_info, pac_exames))

    print("Joined data")

    pd.DataFrame(new_rows).to_csv(
        'dados/input.csv', mode='w+', index=False)

    print("Finished writing input.csv")


if __name__ == "__main__":

    join_pacientes()
    join_exames()
    create_input()
