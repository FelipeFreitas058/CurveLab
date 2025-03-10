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
📌A interface permite importar dados de diferentes fontes para gerar os gráficos:

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
📌Para criar as curvas que irão compor o gráfico, siga os seguintes passos:
  - Vá em "Construção do gráfico" -> "Criar curvas".
  - Adicione a quantidade de curvas necessárias ➕📈.
  - Confira as variáveis disponíveis na 'Lista de variáveis' 📋.
  - Para cada curva nomeie-a e selecione as variáveis X e Y 🏷️.
  - Altere o índice como preferir (mais detalhes posteriormente no **detalhamento de predefinições**).
  - Ative a curva caso queira que apareça no gráfico ✅.


### 📈 Gerar gráfico
📌Para gerar o gráfico, basta seguir os seguintes passos:
  - Após criado as curvas, vá em "Construção do gráfico" -> "Gerar gráfico".
  - Altere as configurações iniciais do gráfico na lateral direita da aba ⚙️.
  - Clique em "Gerar gráfico" 📊.


### 🎨 Personalização do gráfico
📌Após gerado o gráfico, é possível personalizar as mais diferentes características do mesmo:


✔️ Curvas
  - Vá em "Personalização" -> "Curvas".
  - Selecione a curva que se deseja personalizar.
  - Altere os mais diversos parâmetros disponíveis 🛠️.


🏷️ Títulos
  - Vá em "Personalização" -> "Títulos"
  - Escolha qual dos títulos se deseja personalizar 🏷️.
  - Modifique os parâmetros conforme necessário ✏️.


📜 Legenda
  - Vá em "Personalização" -> "Legendas".
  - Ative a legenda caso queira exibi-la ✅.
  - Escolha "Texto da legenda" 📝.
      - Ative "Personalização individual" para personalizar o texto de cada curva separadamente se necessário 🎭.
      - Altere os diferentes parâmetros do texto da legenda 🔧.
  - Escolha "Localização".
      - Escolha a localização da legenda 🗺️.
  - Escolha "Caixa da legenda".
      - Modifique os parâmetros da borda e fundo da legenda 🎨.


📏 Grades
  - Ative a grade principal e secundária 📊.
  - Altere os parâmetros das mesmas conforme desejado 📐.


🖼️ Bordas
  - Ative ou desative as bordas do gráfico separadamente 🖼️.
  - Altere os parâmetros de cada borda conforme desejado 🎨.


### 📤 Exportação do Gráfico
📌Para exportar o gráfico, basta copiar o .png do mesmo clicando em "Copiar gráfico", ou clique em "Exportar gráfico" para mais formatos 📂.


## 💾 Predefinições
📌A interface permite salvar predefinições de um gráfico, permitindo a utilização das mesmas configurações de forma facil e prática 🚀.


### 🔹 Salvando predefinições
📌 A personalização de cada curva será associada ao índice dela, sendo esse índice utilizado ao carregar uma predefinição.
📌 Nomeie os índices de forma clara para facilitar o uso futuro.
  - Vá em "Personalização" -> "Predefinições".
  - Digite um nome para a predefinição e clique em "Salvar" 💾.
  - Em "Utilizar predefinição", confira se a predefinição salva consta na caixa de listagem abaixo de "Usar predefinição" 📜.
  - Caso deseje excluir a predefinição, selecione na caixa de listagem abaixo de "Usar predefinição" e clique em "Excluir predefinição" ❌.


### 🔹 Utilizando predefinições
📌Para utilizar uma predefinição salva, siga os passos à seguir:
  - Selecione a predefinição desejada na caixa de listagem abaixo de "Usar predefinição".
  - Ative a opção "Usar predefinição". Ao ativar, a interface entrará em modo de predefinição, onde não é possível personalizar nenhuma característica do gráfico.
  - Vá em "Construção do gráfico" -> "Criar curvas" e adicione as curvas.
  - Para cada curva, clique na seta '˅' na caixa de listagem abaixo de "Índice" 🔽.
  - Selecione o índice da predefinição para que esta curva tenha a mesma personalização da curva deste índice salva na predefinição.
  - Se nenhum índice for selecionado, a curva será gerada sem personalização ⚠️.
  - Vá em "Construção do gráfico" -> "Gerar gráfico" e gere o gráfico 📈.
