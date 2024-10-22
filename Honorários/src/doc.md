## Documentação do Script para Extração e Processamento de Texto em PDF

### 1. Objetivo
Este script tem como principal objetivo extrair texto de um arquivo PDF, estruturar as informações de acordo com a lógica interna das seções e subseções do conteúdo, e, finalmente, salvar os dados processados em um arquivo JSON. O exemplo específico aplica-se à extração de uma tabela de honorários da Ordem dos Advogados do Brasil (OAB), porém, o código pode ser adaptado para outros documentos similares.

### 2. Dependências
O script faz uso das seguintes bibliotecas:
- `pdfplumber`: Para a extração do texto de arquivos PDF.
- `json`: Para converter os dados extraídos em um formato JSON.
- `os`: Para gerenciar os diretórios e caminhos de arquivos no sistema operacional.

Antes de executar o script, certifique-se de que as dependências estão instaladas. Caso contrário, instale-as usando o comando abaixo:
```bash
pip install pdfplumber
```

### 3. Caminho do Arquivo PDF
O caminho do arquivo PDF a ser processado está definido na variável `pdf_file_path`. Modifique este caminho conforme necessário, de acordo com o local onde o arquivo está armazenado.

```python
pdf_file_path = '/media/peixoto/stuff/padroes-direito/Honorários/tabelas/tabela_site_10_2024.pdf'
```

### 4. Estrutura do Código

#### a. Inicialização de Variáveis
O script começa inicializando uma lista vazia `data` para armazenar os dados extraídos de cada página do PDF:

```python
data = []
```

#### b. Função de Processamento do Texto
A função `process_extracted_text()` é responsável por processar o texto extraído de cada página. Ela realiza a divisão do texto em linhas e identifica se as linhas pertencem a uma seção ou subseção com base no conteúdo:

```python
def process_extracted_text(extracted_text):
    lines = extracted_text.split('\n')
    structured_data = []
    current_section = None
    for line in lines:
        if line.strip() == '' or 'ORDEM DOS ADVOGADOS DO BRASIL' in line:
            continue
        if 'TABELA' in line:
            current_section = line.strip()
            continue
        if current_section:
            structured_data.append({"section": current_section, "text": line.strip()})
    return structured_data
```

Essa função faz o seguinte:
- Divide o texto em linhas.
- Ignora linhas vazias ou irrelevantes (como títulos ou marcações da OAB).
- Detecta se a linha corresponde a uma seção (quando contém a palavra "TABELA").
- Estrutura as informações em um formato adequado para serem armazenadas.

#### c. Extração de Texto do PDF
A extração do texto é feita página a página. A biblioteca `pdfplumber` abre o arquivo PDF e percorre cada página, extraindo o texto que é então processado pela função anterior:

```python
with pdfplumber.open(pdf_file_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            page_data = process_extracted_text(text)
            data.extend(page_data)
```

#### d. Conversão para JSON
Após a extração e o processamento dos dados, o script converte a lista `data` em um arquivo JSON utilizando a função `json.dumps()`. O parâmetro `ensure_ascii=False` garante que caracteres especiais (como acentos) sejam corretamente preservados:

```python
output_json = json.dumps(data, indent=4, ensure_ascii=False)
```

#### e. Salvamento do Arquivo JSON
O JSON gerado é salvo em um arquivo cujo caminho é definido pela variável `output_json_path`. O script garante que o diretório onde o arquivo será salvo existe, criando-o caso necessário, com o uso de `os.makedirs()`:

```python
output_json_path = '/media/peixoto/stuff/padroes-direito/Honorários/extraidos/tabela.json'
os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
```

Finalmente, o arquivo JSON é salvo:

```python
with open(output_json_path, 'w', encoding='utf-8') as f:
    f.write(output_json)
```

### 5. Estrutura do JSON
O arquivo JSON gerado terá a seguinte estrutura:

```json
[
    {
        "section": "TABELA 1",
        "text": "Texto extraído da seção 1..."
    },
    {
        "section": "TABELA 2",
        "text": "Texto extraído da seção 2..."
    }
]
```

Cada item da lista representa uma linha extraída do PDF, associada a uma seção correspondente.

### 6. Pontos de Atenção
- Certifique-se de que o PDF a ser processado tem o texto selecionável, pois PDFs gerados a partir de imagens (como escaneamentos) não conterão texto acessível e precisarão de um OCR (reconhecimento ótico de caracteres) para funcionar.
- O script foi projetado para lidar com um formato específico de tabelas de honorários da OAB. Modificações podem ser necessárias para processar outros tipos de documentos.
  
### 7. Uso e Execução
Após a configuração do caminho do PDF e a instalação das dependências, o script pode ser executado diretamente em um ambiente Python. Ele processará o arquivo PDF e gerará um arquivo JSON estruturado no caminho especificado.

### 8. Considerações Finais
Este código oferece uma solução eficiente para extrair e organizar informações de documentos em PDF. Ele pode ser facilmente adaptado para diferentes estruturas de documentos ao modificar a lógica de processamento do texto dentro da função `process_extracted_text`.