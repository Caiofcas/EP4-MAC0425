import pandas as pd


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
    return exames


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

    return pacientes


if __name__ == "__main__":

    print("Starting processing patients")

    pac = join_pacientes()
    # padronize_data('dados/exames.csv', 'dados/exames_p.csv')
    # remove_broken_enconding('dados/pacientes.csv')

    pac.to_csv('dados/pacientes.csv', mode='w+', index=False,
               columns=['ID_Paciente', 'Sexo',
                        'Ano_Nascimento', 'Hospital'])
    print("Finished writing pacientes.csv")

    print("Starting processing exames")
    ex = join_exames()

    print("Joined Exames")
    ex = ex.dropna(subset=['Exame'])

    # Only takes exams related with COVID19
    ex = ex[ex.Exame.str.match('.*(COVID|SARS-CoV-2).*') == True]

    print("Filtered exam types")

    ex.to_csv('dados/exames.csv', mode='w+', index=False,
              columns=['ID_Paciente', 'Data_Coleta', 'Origem', 'Exame',
                       'Analito', 'Resultado', 'Unidade',
                       'Valor_Referencia', 'Hospital'])

    print("Finished writing exames.csv")
