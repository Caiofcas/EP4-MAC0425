# Relatório

(título?)

## Nome dos autores

Caio Fontes          - 10692061
Eduardo Laurentino   - xxxxxxxx

## Resumo

## Introdução

deve conter os seguintes elementos: motivação para o trabalho, contendo um ou dois parágrafos; objetivos do trabalho, contendo um parágrafo; estrutura do relatório a seguir, contém um parágrafo.

## Metodologia

### Pré-processamento dos Dados

O pré-processamento é uma fase importantíssima que nem sempre recebe a devida atenção. No nosso caso, para ressaltar a importância dessa fase, metade da nota vai vir para processamento.

Eu já dei uma pequena transformada e normalizada nos dados fornecidos, mas aqui vocês deverão fazer diversas outras atividades. Em particular vocês devem decidir quais serão os dados de entrada para rede neural, que devem ser resultados de exames. É importante notar que não há nenhuma garantia e que todos os pacientes tenham realizados os mesmos exames em todas as datas, então vocês devem indicar como estarão tratando dados inexistentes/ faltantes. É razoável que , tendo três fontes diferentes de exames,esses não tenham exatamente os mesmos nomes em todas as fontes, e é importante verificar se as unidades de resposta de cada um dos exames são as mesmas em todos as fontes.

Similarmente, é muito improvável que todos os pacientes tenham realizado os três exames de detecção de saída em todos os exames, então é importante dizer como você vai lidar se não houver algum dado de saída numa determinada instância. No entanto para não alongar muito esta parte do relatório, você não deve levar mais do que duas páginas nesta descrição. Use figuras se isto facilitar a explicação.

Esta fase de pré-processamento deverá produzir uma planilha (csv) ou o banco de dados (sql) que sirva de entrada para o treinamento da rede neural. Você deverá entregar tanto a planilha/ banco de dados quanto os programas em Python que foram utilizados para gerar esta planilha.

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
