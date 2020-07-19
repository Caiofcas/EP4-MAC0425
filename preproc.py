import pandas as pd
from collections import namedtuple
import re

# ---- Definitions ------------------------------

Exame = namedtuple('Exame', 'nome analito resultado unidade valref data')

PAC_DATA = 'dados/pacientes.csv'
EXM_DATA = 'dados/exames.csv'
INP_DATA = 'dados/input.csv'

F_PAC = 'dados_originais/Grupo_Fleury_Dataset_Covid19_Pacientes.csv'
E_PAC = 'dados_originais/einstein_full_dataset_paciente.csv'
H_PAC = 'dados_originais/hsl_patient_1.csv'

F_EXAM = 'dados_originais/Grupo_Fleury_Dataset_Covid19_Resultados_Exames.csv'
E_EXAM = 'dados_originais/einstein_full_dataset_exames.csv'
H_EXAM = 'dados_originais/hsl_lab_result_1.csv'


# ---- Pacient Processing ----------------------

def join_pacientes():

    print("Starting processing patients")

    # read csv files
    einstein_p = pd.read_csv(E_PAC, sep='|')
    fleury_p = pd.read_csv(F_PAC, sep='|')
    hsl_p = pd.read_csv(H_PAC, sep='|')

    # padronize columns
    fleury_p.columns = einstein_p.columns
    hsl_p['Hospital'] = 'HSL'
    einstein_p['Hospital'] = 'Einstein'
    fleury_p['Hospital'] = 'Fleury'

    pacientes = pd.concat([einstein_p, fleury_p, hsl_p])
    pacientes.columns = ['ID_Paciente', 'Sexo', 'Ano_Nascimento', 'País', 'UF',
                         'Município', 'CEP', 'Hospital']

    pacientes.to_csv(PAC_DATA, mode='w+', index=False,
                     columns=['ID_Paciente', 'Sexo',
                              'Ano_Nascimento', 'Hospital'])
    print("Finished writing pacientes.csv")


# ---- Exam Processing ----------------------


def fix_encoding(entry):
    '''
    Auxiliary function that deals with some enconding issues in _entry_.
    '''
    if type(entry) != str:
        return entry

    return entry \
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
        .replace('í­', 'í')  # Tem um caracter escondido aqui


def split_exam(exam, analito_matches, names):
    '''
    Changes _exam_ 'Exame' field based on which str present in _analito_matches_
    is contained in _exam_ 'Analito' field. If there is no match the value is set
    to NaN to allow data filtering.
    '''
    for i in range(len(analito_matches)):
        if analito_matches[i] in exam['Analito']:
            exam['Exame'] = names[i]
            return exam

    exam['Exame'] = float('nan')
    return exam


def filter_exam_types(df):

    blood_A = (
        (df.Exame == 'HEMOGRAMA, sangue total') & (
            (df.Analito == 'Linfócitos (%)') |
            (df.Analito == 'Basófilos (%)') |
            (df.Analito == 'Neutrófilos (%)') |
            (df.Analito == 'Monócitos (%)') |
            (df.Analito == 'Eosinófilos (%)')
        ))

    blood_B = (
        (df.Exame == 'Hemograma Contagem Auto') & (
            (df.Analito == 'Linfócitos') |
            (df.Analito == 'Basófilos') |
            (df.Analito == 'Neutrófilos') |
            (df.Analito == 'Monócitos') |
            (df.Analito == 'Eosinófilos')
        ))

    covid = (df.Exame.str.match('.*(COVID|SARS-CoV-2).*') == True)

    return df[blood_A | blood_B | covid]


def join_exam_types(df):
    cond_igg_igm = (
        (df.Exame == 'COVID-19-Teste Rápido (IgM e IgG), soro')
        | (df.Exame == 'Teste rápido COVID19 IgG/IgM')
        | (df.Exame == 'Teste rápido Coronavirus COVID19 IgG/IgM')
        | (df.Exame == 'SARS-CoV-2, ANTICORPOS IgM E IgG, TESTE RÁPIDO')
        | (df.Exame == 'Sorologia SARS-CoV-2/COVID19 IgG/IgM')
        | (df.Exame == 'COVID-19-Sorologia IgM e IgG por quimiluminescência, soro')
    )

    cond_iga_igg = (df.Exame == 'COVID-19, anticorpos IGA e IGG, soro')

    cond_igg = (df.Exame == 'COVID19, ANTICORPOS IgG, soro')
    cond_igm = (df.Exame == 'COVID19, ANTICORPOS IgM, soro')
    cond_iga = (
        (df.Exame == 'COVID19, ANTICORPOS IgA, soro') |
        (df.Exame == 'Anticorpos IgA contra SARS-CoV-2/COVID19')
    )

    cond_pcr = (
        (df.Exame == 'NOVO CORONAVÍRUS 2019 (SARS-CoV-2), DETECÇÃO POR PCR') |
        (df.Exame == 'HMVSC-AFIP PCR COVID 19') |
        (df.Exame == 'COVID-19-PCR para SARS-COV-2, Vários Materiais (Fleury)')
    )

    df.loc[cond_igg_igm, 'Exame'] = 'COVID19 IgG IgM'
    df.loc[cond_iga_igg, 'Exame'] = 'COVID19 IgA IgG'
    df.loc[cond_pcr, 'Exame'] = 'COVID19 PCR'
    df.loc[cond_igg, 'Exame'] = 'COVID19 IgG'
    df.loc[cond_iga, 'Exame'] = 'COVID19 IgA'
    df.loc[cond_igm, 'Exame'] = 'COVID19 IgM'
    return df


def join_exames():

    print("Starting processing exames")

    # read csv files
    fleury_e = pd.read_csv(F_EXAM, sep='|', encoding='latin1')
    einstein_e = pd.read_csv(E_EXAM, sep='|')
    hsl_e = pd.read_csv(H_EXAM, sep='|')

    # padronize columns
    einstein_e.columns = fleury_e.columns
    hsl_e['Hospital'] = 'HSL'
    einstein_e['Hospital'] = 'Einstein'
    fleury_e['Hospital'] = 'Fleury'

    exames = pd.concat([einstein_e, fleury_e, hsl_e])

    print("Joined Exames")

    exames.columns = ['ID_Paciente', 'Data_Coleta', 'Origem', 'Exame',
                      'Analito', 'Resultado', 'Unidade', 'Valor_Referencia',
                      'Hospital', 'ID_Atendimento']

    exames = exames.dropna(subset=['Exame'])

    exames = filter_exam_types(exames)

    print("Filtered exam types")

    exames = exames.applymap(fix_encoding)

    print("Fixed enconding in Exames")

    exames = join_exam_types(exames)

    print("Standartized exam types")

    conditions = [
        (exames.Exame.str.match('COVID19 IgG IgM') == True),
        (exames.Exame.str.match('COVID19 IgA IgG') == True),
        ((exames.Exame == 'Hemograma Contagem Auto')
         | (exames.Exame == 'HEMOGRAMA, sangue total'))
    ]

    args = [
        [['IgG', 'IgM'],
         ['COVID19 IgG',
          'COVID19 IgM']],
        [['IgA e IgG', 'IgA', 'IgG'],
         [None,
          'COVID19 IgA',
          'COVID19 IgG']],
        [['Linfócitos',
            'Basófilos',
          'Neutrófilos',
          'Monócitos',
          'Eosinófilos'],
         ['Linfócitos',
            'Basófilos',
          'Neutrófilos',
          'Monócitos',
          'Eosinófilos']]
    ]

    for cond, args in zip(conditions, args):

        exames.loc[cond] = exames[cond].apply(
            split_exam, axis=1,
            args=args)

    exames = exames.dropna(subset=['Exame'])

    print("Split compounded Exams")

    exames.to_csv(EXM_DATA, mode='w+', index=False,
                  columns=['ID_Paciente', 'Data_Coleta', 'Origem', 'Exame',
                           'Analito', 'Resultado', 'Unidade',
                           'Valor_Referencia', 'Hospital'])

    print("Finished writing exames.csv")

# ---- NN Input Processing -----------------


def is_float_try(entry):
    '''
    Simple function that checks if _entry_ can be parsed into a float.
    '''
    try:
        float(entry.replace(',', '.'))
        return True
    except ValueError:
        return False


def pac_dict(filename=PAC_DATA):
    '''
    Create and return a dict representation of _filename_ where:
        KEY: ID_PACIENTE
        VAL: (SEXO,ANO_NASCIMENTO)
    '''
    df = pd.read_csv(filename)
    d = {}
    for _, row in df.iterrows():
        if d.get(row['ID_Paciente']) is None:
            d[row['ID_Paciente']] = (row['Sexo'], row['Ano_Nascimento'])
        else:
            print("porra tem conflito de ID")
    return d


def exam_dict(filename=EXM_DATA):
    '''
    Create and return a dict representation of _filename_ where:
        KEY: ID_PACIENTE
        VAL: list of -Exame- namedtuples
    '''
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
    return d


def get_pac_row(info, exams):
    res2num = {
        'POSITIVO': 1,
        'NEGATIVO': 0
    }
    row = {}
    row['Sexo'] = info[0]
    row['Ano_Nasc'] = info[1]

    for ex in exams:
        if is_float_try(ex.resultado):
            key = ex.nome + ' NUM'
            row[key] = float(ex.resultado.replace(',', '.'))
        else:
            key = ex.nome + ' BOOL'
            row[key] = res2num.setdefault(
                exam_result(ex.resultado), float('nan'))

    return row


def exam_result(resultado):
    DEBUG = False
    res = 'xxxxx'
    matchNegativo = re.compile(
        r'negativo|não|fraco|sem evidência|indetectável', re.IGNORECASE)
    matchInconclusivo = re.compile(
        r'indeterminado|inconclusivo|repetir o teste|aguardar|a critério|possível',
        re.IGNORECASE)
    matchPositivo = re.compile(
        r'reagente|detectado.*|detectável|evidência', re.IGNORECASE)
    matchNumerico = re.compile(r'(\d)+(,|\.)(\d)+', re.IGNORECASE)
    matchLixo = re.compile(
        r'swab|raspado|nasofaringe|laringe|plasma|bronquico|sangue|secreção|traqueal|Nova Coleta|soro|liquor|trato respiratório|lavado|(\*)+|( ){2,}',
        re.IGNORECASE)
    tests = (['INCONCLUSIVO', matchInconclusivo], ['NEGATIVO', matchNegativo],
             ['POSITIVO', matchPositivo], ['numerico', matchNumerico],
             ['lixo', matchLixo])

    for test in tests:
        regexResultado = test[1].search(resultado)
        if regexResultado is not None:
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
            break  # Interrompe os testes por ter classificado a palavra

    # print('Palavra {} classificada como {}'.format(resultado, res))
    return res


def create_input():

    print("Creating input csv")

    # Construir dict com sexo e nasc

    sexo_e_nascimento = pac_dict()

    print("Processed pacientes")

    # Construct Exam dict

    exames_dict = exam_dict()

    print("Processed exames")

    # Construct data

    new_rows = []
    for pac_id in sexo_e_nascimento.keys():

        pac_info = sexo_e_nascimento[pac_id]
        pac_exames = exames_dict.get(pac_id)

        if pac_exames is not None:
            new_rows.append(get_pac_row(pac_info, pac_exames))

    print("Joined data")

    pd.DataFrame(new_rows).dropna(how='all', axis=1).to_csv(
        INP_DATA, mode='w+')

    print("Finished writing input.csv")


if __name__ == "__main__":

    join_pacientes()
    join_exames()
    create_input()
