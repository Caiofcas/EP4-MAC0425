import pandas as pd
from collections import namedtuple

Exame = namedtuple('Exame', 'nome analito resultado unidade valref data')

# ---- Auxiliary Functions ----------------------


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
        .replace('í', 'Á')


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

def pac_dict(df):
    d = {}
    for _, row in df.iterrows():
        if d.get(row['ID_Paciente']) is None:
            d[row['ID_Paciente']] = (row['Sexo'], row['Ano_Nascimento'])
        else:
            print("porra tem conflito de ID")
    return d


def exam_dict(df):
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


def create_input():

    print("Creating input csv")

    pac = pd.read_csv("dados/pacientes.csv")
    exames = pd.read_csv("dados/exames.csv")

    print("Load pacientes and exames data")

    # Construir dict com sexo e nasc

    sexo_e_nascimento = pac_dict()

    print("Processed pacientes")

    # Construct Exam dict

    exames_dict = exam_dict()

    print("Processed exames")

    # Constroi fields

    fields = get_fields(exames.Exame.unique())

    # Construct data

    new_rows = []
    for pac_id in sexo_e_nascimento.keys():

        # initialize empty dict
        row = dict.fromkeys(fields)

        # recover pacient info
        pac_info = sexo_e_nascimento[pac_id]

        row['ID_Paciente'] = pac_id
        row['Sexo'] = pac_info[0]
        row['Ano_Nasc'] = pac_info[1]

        # recover exams (if there are any)
        pac_exames = exames_dict.get(pac_id)

        if pac_exames is not None:
            for ex in pac_exames:
                row['['+ex.nome+']_analito'] = ex.analito
                row['['+ex.nome+']_resultado'] = ex.resultado
                row['['+ex.nome+']_unidade'] = ex.unidade
                row['['+ex.nome+']_datacol'] = ex.data
                row['['+ex.nome+']_valref'] = ex.valref

            # Only appends pacients that have at least one of the desired exams
            new_rows.append(row)

    print("Joined data")

    pd.DataFrame(new_rows, columns=fields).to_csv(
        'dados/input.csv', mode='w+', index=False)

    print("Finished writing input.csv")


if __name__ == "__main__":

    join_pacientes()
    join_exames()
    create_input()
