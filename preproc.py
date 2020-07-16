import pandas as pd
from collections import namedtuple


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


def join_exames():
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

    exames.to_csv('dados/exames.csv', mode='w+', index=False,
                  columns=['ID_Paciente', 'Data_Coleta', 'Origem', 'Exame',
                           'Analito', 'Resultado', 'Unidade',
                           'Valor_Referencia', 'Hospital'])

    print("Finished writing exames.csv")


def join_pacientes():
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


def create_input():
    # THIS IS A FUCKING MESS

    pac = pd.read_csv("dados/pacientes.csv")
    exames = pd.read_csv("dados/exames.csv")

    # Define o tipo de dado
    Exame = namedtuple('Exame', 'nome analito resultado unidade valref data')

    # Construir dict com sexo e nasc
    sexo_e_nascimento = {}
    for index, row in pac.iterrows():
        if sexo_e_nascimento.get(row['ID_Paciente']) is None:
            sexo_e_nascimento[row['ID_Paciente']] = (
                row['Sexo'], row['Ano_Nascimento'])
        else:
            print("porra tem conflito de ID")

    # Construct Exam dict
    exames_dict = {}
    for index, row in exames.iterrows():
        val = exames_dict.get(row['ID_Paciente'])
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
        exames_dict[row['ID_Paciente']] = val

    # Constroi fields

    fields = ["ID_Paciente", "Sexo", "Ano_Nasc"]
    for name in exames.Exame.unique():
        fields += ['['+name+']_analito',
                   '['+name+']_resultado',
                   '['+name+']_unidade',
                   '['+name+']_datacol',
                   '['+name+']_valref'
                   ]

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

    pd.DataFrame(new_rows, columns=fields).to_csv(
        'dados/input.csv', mode='w+', index=False)

    print("Finished writing input")


if __name__ == "__main__":

    print("Starting processing patients")
    join_pacientes()

    print("Starting processing exames")
    join_exames()

    # create actual input for the networks
    print("Creating input csv")
    create_input()
    # generate_igg_input()
    # generate_iga_input()
    # generate_PCR_input()
