# Relatório EP4 - MAC350

## Nome dos autores

Caio Andrade    -  9797232
Caio Fontes     - 10692061

## Resumo

## Introdução

deve conter os seguintes elementos: motivação para o trabalho, contendo um ou dois parágrafos; objetivos do trabalho, contendo um parágrafo; estrutura do relatório a seguir, contém um parágrafo.



## Metodologia

### Pré-processamento dos Dados

O preprocessamento é realizado pelo arquivo _preproc.py_, ele assume que os arquivos originais estão em uma pasta _dados_originais_, e gera 3 arquivos dentro da pasta _dados_, _pacientes.csv_,_exames.csv_ e _input.csv_. Primeiramente realizamos uma unificação das diferentes bases de dados através das funções `join_pacientes()` e `join_exames()`. A unificação das bases de pacientes é bem simples e o código é autoexplicativo. A unificação das bases de exames possui alguns passos extras.

Primeiramente os dados das bases são unificados em uma maneira muito similar a da função `join_pacientes()`. Depois disso selecionamos apenas alguns tipos de exames com os quais iremos trabalhar, devido ao escopo enorme da base, esse processo é feito pela função `filter_exam_types()`. A função `join_exame_types()` recebe esse subconjunto de exames e realiza uma união de diversos tipos de exames que são equivalentes para os nossos propósitos, padronizando os valores do campo 'Exame'.

Uma característica das bases disponibilizadas é que muitas vezes um exame possui muitos diferentes analitos, que efetivamente caracterizam um tipo diferente de dado. Realizamos mais uma etapa de processamento separando todos esses diferentes 'subexames', baseando-se no valor do campo Analito, utilizando a função _split_exam_ no laço da linha 207. Por fim salvamos esses  dados no arquivo _dados/exames.csv_.

Por fim a função `create_input()` realiza o processamento final dos dados, unificando as informações sobre os pacientes e seus respectivos exames no arquivo _input.csv_. 

### Arquitetura da Rede Neural

Nesta seção você deverá descrever arquitetura da rede neural utilizada e incluir os programas em Python utilizados para treinar e rodar a rede. Não há qualquer problema que esses programas sejam modificações dos programas fornecidos no exercício em sala, mas se na descrição da arquitetura você simplesmente disser algo como “a mesma arquitetura do exercício”, vou entender que você não tem ideia do que está sendo utilizado.

É necessário descrever o número de entradas, o número de camadas, o tamanho de cada uma das camadas escondidas; é necessário descrever a função utilizada para calcular a perda (loss) e eventuais otimizações do usado no treinamento. É necessário descrever como a rede é utilizada no treinamento e durante sua execução, quando iremos prever o estágio de infecção de um paciente, mencionando formato das entradas, o tamanho dos batches, e o formato da saída.

Entregar os programas Python usados no treinamento e na execução da rede, bem como um minúsculo manual do usuário. No relatório essa parte não deverá ter mais do que três parágrafos.

### Experimentos

Nessa parte você deve descrever como foram feitos os treinamentos, e o que está sendo medido (apresentando uma fórmula de preferência) no experimento. Como a quantidade de dados é relativamente pequena, espera-se que você realize um processo de “k-fold treinamento’ ‘, com k = 10. Em cada treinamento, você deverá usar 90% do conjunto de dados para treino, e 10% para validação. Descreva como essas partes foram obtidas.

Neste caso é esperado que você repita o treinamento 10 vezes. Se o tempo de treinamento for excessivo (muitas horas) você pode decidir por utilizar k = 5 ou k = 3, mas terá de apresentar o tempo de treinamento como justificativa para este encurtamento do experimento.

## Resultados

O mínimo que você deve apresentar nesta fase de resultados são os valores de acurácia para cada uma das três medidas para cada um dos k-treinamentos. No final, você deve apresentar a média e desvio padrão, o melhor e o pior valores de acurácia para cada uma das três medidas de saída.

Se você propuser alguma valoração da rede neural, deverá realizar um experimento para cada variante e apresentar os dados relativos a cada uma das variantes.

## Discussão

o nosso caso esta seção deverá centrar-se na viabilidade e utilidade de usar arquitetura neural proposta como uma previsor da fase da infecção.

## Bibliografia
