# CurveLab🎨📈

CurveLab é uma interface gráfica para a criação e personalização de gráficos cartesianos de forma simples e eficiente.

## 📥 Instalação
### 1️⃣ Pré-requisitos
  - Python: (Baixe em: [python.org/downloads](https://www.python.org/downloads/)).
  - Bibliotecas Necessárias: Instale com o comando
  ```pip install PyQt6 matplotlib openpyxl numpy pandas```.

### 2️⃣ Executando o CurveLab
Após a instalação das bibliotecas, basta abrir o aplicativo CurveLab.exe para iniciar a interface gráfica.

## 📊 Como Usar?
### 🔹 Importação de Dados
A interface permite importar dados de diferentes fontes para gerar os gráficos:

✔️ Planilhas (.xlsx, .xls, .csv)
  - Acesse "Seleção de dados" > "Planilha".
  - Clique em "Carregar planilha" e selecione o arquivo.
  - Selecione os dados da variável, nomeie-a e clique em "Importar variável".

✔️ Código Python

  - Vá em "Seleção de dados" > "Código".
  - Digite ou cole um código Python e clique em "Executar código".
  - As variáveis detectadas aparecerão na lista para importação.
  - Selecione quais variáveis serão utilizadas no gráfico e clique em "Importar variáveis".

✔️ Arquivos de Texto (.txt)

  - Vá em "Seleção de dados" > "Arquivo de Texto".
  - Selecione o arquivo e escolha o separador dos valores.
  - Clique em "Gerar planilha", confira os dados da planilha e importe-a.
  - A planilha importada estará em "Seleção de dados" > "Planilha".

### 🔹 Criação de curvas
Para criar as curvas que irão compor o gráfico, siga os seguintes passos:
  - Vá em "Construção do gráfico" -> "Criar curvas".
  - Adicione a quantidade de curvas necessárias.
  - Confira as variáveis disponíveis na 'Lista de variáveis'.
  - Para cada curva nomeie-a e selecione as variáveis X e Y.
  - Altere o índice como preferir (mais detalhes posteriormente no detalhamento de predefinições)
  - Ative a curva caso queira que apareça no gráfico

### 🔹 Gerar gráfico
Para gerar o gráfico, basta seguir os seguintes passos:
  - Após criado as curvas, vá em "Construção do gráfico" -> "Gerar gráfico".
  - Altere as configurações iniciais do gráfico na lateral direita da aba.
  - Clique em "Gerar gráfico".

### 🔹 Personalização do gráfico
Após gerado o gráfico, é possível personalizar as mais diferentes características do mesmo:

✔️ Curvas
  - Vá em "Personalização" -> "Curvas".
  - Selecione a curva que se deseja personalizar.
  - Altere os mais diversos parâmetros de cada curva.

✔️ Títulos
  - Vá em "Personalização" -> "Títulos"
  - Escolha qual dos títulos se deseja personalizar.
  - Altere os mais diversos parâmetros de cada título.

✔️ Legenda
  - Vá em "Personalização" -> "Legendas".
  - Ative a legenda.
  - Escolha "Texto da legenda".
      - Ative "Personalização individual" para personalizar o texto de cada curva separadamente se necessário.
      - Altere os mais diversos parâmetros do texto da legenda.
  - Escolha "Localização".
      - Escolha a localização da legenda.
  - Escolha "Caixa da legenda".
      - Altere os mais diversos parâmetros da caixa e borda da legenda.

✔️ Grades
  - Ative a grade principal e secundária.
  - Altere os parâmetros das mesmas conforme desejado.

✔️ Bordas
  - Ative ou desative as bordas do gráfico separadamente.
  - Altere os parâmetros de cada borda conforme desejado.

### Exportação do gráfico
Para exportar o gráfico, basta copiar o .png do mesmo clicando em "Copiar gráfico", ou clique em "Exportar gráfico" para mais formatos.

### Predefinições
A interface permite salvar predefinições de um gráfico, permitindo a utilização das mesmas configurações de forma facil e prática:

#### ASd
  - Vá em "Personalização" -> "Predefinições".
  
