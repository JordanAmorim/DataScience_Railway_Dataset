# DataScience Railway Dataset
Monitoração e Diagnóstico de Máquinas - MCA08719 - UFES - 2022/1

**Orientador do Grupo:** William  Homem

**Componentes do Grupo:**
- Gabriela Caprini
- Jordan Amorim
- Lucca Fialho
- Vinícius Gonçalves

------------
Estre trabalho tem como propósito, analisar os dados de respostas dinâmicas de dois veículos ao tramitarem por trilhos na cidade de Pittsburgh. Temos como base, a análise ja efetuada por meio de diferentes métodos disponível em:  [https://www.nature.com/articles/s41597-019-0148-9](https://www.nature.com/articles/s41597-019-0148-9)

## Contextualização

Os dados foram obtidos atráves de vagões instrumentados acoplados em 2 veículos leves sobre trilhos para transporte de passageiros. Percorrendo trechos da malha ferroviária existente na cidade de Pittsburgh, Pennsylvania, foram adiquiridos dados de velocimeto ,acelerometros dispostos em diferentes posições do vagão e de GPS em conjunto com posicionamento ao longo da via.

Concomitantemente, foram colhidos dados de anomalias presentes na via por meio do sistema de manutenção adotado pela concessionária. Desse modo, é possível treinar um modelo computacional com base em aprendizado de máquina, que identifique necessidade de manutenções de forma preditiva.

Para isso, apresenta-se o passo a passo para gerar tal modelo:

## Extração dos Dados

Primeiramente, os dados devem ser extraídos de [repositório](https://drive.google.com/drive/u/0/folders/1oKn7IN7zznQuhwjDCDdjq8r9wHJYBEhj "repositório"). Nele, são diferenciados os arquivos explicativos, e os dados de GPS e demais sensores são segregados para o veículo [LRV4313](https://drive.google.com/drive/u/0/folders/13bXx9ChC7gwbVAcD-xXXnxluuKzUD3Sa "LRV4313") e [LRV4306](https://drive.google.com/drive/u/0/folders/1hrFL_1GhCPXqAuES8gXvyawUPwCSvfPF "LRV4306").

Apenas dados da Região 5 - demonstrada no mapa -  foram utilizados. Buscando menor erros de GPS existente se comparado com outras áreas.

![](https://github.com/JordanAmorim/DataScience_Railway_Dataset/blob/main/docs/LRV-regions.jpg)

Não é possível fazer download diretamente pelo site, uma vez que os arquivos excedem o tamanho disponível pela plataforma. Portanto, foi criado atalho do repositório no computador e utilizado programa [Extraction_data](https://github.com/JordanAmorim/DataScience_Railway_Dataset/blob/main/Extraction_data.ipynb). 

No programa, deve-se alterar o caminho para a pasta que contém o atalho dos arquivos

    path = '\\seu_caminho\\sua_pasta\\'

O programa une todos os arquivos presentes (disponíveis separados por viagem do trem) em apenas dois arquivos *.parquet* para cada trem. 

### LVRXXX_gps.parquet

Com os dados de GPS dispostos da seguinte forma:

| i | latitude | longitude | altura | velocidade | hora | data | passagem do dia | direção |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
|0|-80.002785|40.4069117|301.5|45.3|735842.9051736111|20140911|1|1|
|1|-80.00273|40.4068083|300.9|46.5|735842.9051851851|20140911|1|1|
|2|-80.0026683|40.4067083|301.4|47.4|735842.9051967593|20140911|1|1|
|3|-80.0026133|40.40662|303.5|44.8|735842.9052083333|20140911|1|1|
|4|-80.00255|40.4065267|304.1|44.2|735842.9052199074|20140911|1|1|

### LVRXXX_acc.parquet

Com os dados dos sensores dispostos da seguinte forma:

|I|sensor_1|sensor_2|sensor_3|sensor_4|sensor_5|Data| passagem do dia | direção |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
|0|0.012022|-0.000916|-0.003262|0.008114|-0.004604|20140911|1|1|
|1|0.01355|-0.007114|-0.009735|0.004604|-0.032598|20140911|1|1|
|2|0.011975|-0.007948|-0.003998|-0.006462|-0.011136|20140911|1|1|
|3|0.014222|-0.004834|-0.008183|-0.006215|0.027174|20140911|1|1|
|4|0.012726|-0.001075|-0.007999|0.001372|0.023591|20140911|1|1|

## Tratamento de Dados

Para tratamento dos dados, é utilizado o programa [Tratamento_dados](https://github.com/JordanAmorim/DataScience_Railway_Dataset/blob/main/Tratamento_dados.ipynb). Nele, deve ser novamente apontado o caminho para os dados já extraídos. As etapas que deveriam seguir neste tratamento são:

### Alinhamento do trajeto

Neste passo, uma rota de referência da linha 5 foi usada e os dados da trajetoria real são aproximados até esta trajetória. Para isso é feito:
 - Separação em eixos y e x (coordenadas Latidudinais e Longitudinais);
 - Redução dos dados de GPS pela função Interpolador (pois as coordenadas de referência possuem menos dados);
 - Alinhamento da trajetória em x e y por meio da função DynamicTimeWarping;
 - Retorno dos dados para a quantidade original pela função AntiInterpolador
 - Plot das coordenadas y e x (coordenadas Latidudinais e Longitudinais) para conferência.

Entretanto, possívelmente pelo grande tamanho dos dados existentes, quando utilizado para toda a gama de dados extraídos, não foi possível por meio de nosso programa, alinhar as trajetórias para todas as viagens, sendo possível apenas alinhar o trajeto em uma viagem escolhida. O resultado da conferência deste alinhamento é exibido abaixo:

![](https://github.com/JordanAmorim/DataScience_Railway_Dataset/blob/main/docs/trajeto-e-correcao.jpeg)

A trajetórias percorrida e exibida neste gráfico são muito próximas da referência. Por este motivo, não é possível verificar grandes variações entre elas e a trajetória corrigida.

### Transformação das Coordenadas

Posteriormente, deveriam ser utilizadas as distâncias ponto a ponto das coordenadas de GPS para trazer uma real distância percorrida. Para isso,  foi criada a função Distancias. Infelizmente o código apresentou Bugs e não foi possível utilizá-lo.

### Integração com Sensores

Já com as distâncioas corrigidas, devem ser integrados os valores da tabela de sensores com as reais distâncias corrigidas. Dessa forma é possível relacionar o os valores dos acelerometros com o trecho da ferrovia em que estas medições foram obtidas. 

## Próximos Passos

Com estes dados em mãos, os próximos passos seriam:

- Pré processamento dos dados, relacioná-los com as respostas esperadas;
- Trazer as respostas esperadas com base nos dados de manutenção da via disponíveis;
- Executar o aprendizado de máquina, buscando a melhor relação dos sensores que prediz necessidade de manutenção na via.
