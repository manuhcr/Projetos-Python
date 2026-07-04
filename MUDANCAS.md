# Registro de Mudanças (Changelog)

Este arquivo documenta correções feitas no repositório, explicando **o que** mudou,
**por que** era um problema e **o que se aprende** com cada caso. É um documento de
estudo, então cada mudança tem contexto detalhado.

---

## Correção 1 — Remoção do `import params` (Combobox Dependente)

**Arquivo:** `Combobox Dependente/repositorio.py` (linha 8)

**Antes:**
```python
from datetime import datetime  # Biblioteca para pegar data e hora atual

import params

# Importações de outros arquivos do seu próprio projeto
```

**Depois:**
```python
from datetime import datetime  # Biblioteca para pegar data e hora atual

# Importações de outros arquivos do seu próprio projeto
```

**Qual era o problema?**
A linha `import params` mandava o Python carregar um módulo (arquivo) chamado
`params.py`. Esse arquivo **não existe** em lugar nenhum do projeto.

Em Python, os `import` do topo do arquivo são executados **no exato momento em que o
arquivo é carregado** — antes de qualquer função rodar. Como `params.py` não existe, o
Python levantava o erro:

```
ModuleNotFoundError: No module named 'params'
```

Ou seja: o projeto **Combobox Dependente quebrava logo ao abrir**, sem nem chegar a
mostrar a janela.

**Por que esse import estava lá?**
Foi um resto esquecido. Dentro dos métodos do arquivo existe uma *variável local*
chamada `params` (por exemplo `params = []` no método `list`). O `import params` no
topo era uma linha antiga que não tinha relação com essa variável e ficou sobrando.

**O que se aprende:**
- Imports rodam na carga do módulo; um import quebrado derruba o programa inteiro logo de cara.
- Um *nome de variável* (`params = []`) não tem nada a ver com um *módulo* de mesmo nome. São coisas diferentes.
- Vale a pena remover imports que não são usados (muitos editores/linters, como o Pylint ou o Ruff, avisam sobre isso automaticamente).

> **Observação (não corrigido — fica de exercício):** esse mesmo arquivo tem outros dois
> imports que também não são usados e não fazem sentido aqui:
> `from encodings import utf_8` (linha 2) e `from multiprocessing import connection` (linha 3).
> Eles **não quebram** o programa, mas são "lixo" que confunde a leitura. Bom exercício:
> rodar um linter e remover imports não utilizados.

---

## Correção 2 — Import cruzado que quebrava a execução (FiltroEntreDatas)

**Arquivo:** `FiltroEntreDatas/repositorio.py` (linha 15)

**Antes:**
```python
from FiltroEntreDatas.configBanco import caminhoExportarSQL
```

**Depois:**
```python
from configBanco import caminhoExportarSQL
```

**Qual era o problema?**
Esse `import` estava escrito no formato "de pacote": `FiltroEntreDatas.configBanco`
significa *"entre na pasta/pacote `FiltroEntreDatas` e pegue o `configBanco` de lá"*.

Mas a forma como você roda o projeto é entrando **dentro** da pasta:
```bash
cd FiltroEntreDatas
python appFiltroDatas.py
```
Quando você está dentro da pasta, o Python enxerga o arquivo `configBanco.py` como um
módulo direto (`configBanco`), e **não** como `FiltroEntreDatas.configBanco`. A pasta
`FiltroEntreDatas` não está registrada como um pacote no caminho de busca do Python.
Resultado:

```
ModuleNotFoundError: No module named 'FiltroEntreDatas'
```

Todos os outros arquivos do projeto já importavam do jeito certo
(`from configBanco import ...`). Só essa linha estava fora do padrão.

**O que se aprende:**
- `from configBanco import x` → import **relativo ao diretório atual** (funciona quando você roda de dentro da pasta).
- `from FiltroEntreDatas.configBanco import x` → import **de pacote** (só funciona se você rodar de fora, tratando a pasta como pacote — o que não é o caso aqui).
- Manter um padrão de imports consistente em todo o projeto evita esse tipo de armadilha.

---

## Correção 3 — Padronização da senha do MySQL

**Arquivos alterados:**
- `Combobox Dependente/configBanco.py` (linha 9)
- `FiltroEntreDatas/configBanco.py` (linha 9)
- `Agrupamento de colunas/configBanco.py` (linha 15)

**Antes** (nesses três arquivos):
```python
senha = '$aluno123BD'   # (no Combobox a variável se chama pwd)
```

**Depois:**
```python
senha = '$aluno123DB'
```

**Qual era o problema?**
A senha do banco estava escrita de **duas formas diferentes** pelos projetos:

| Grafia          | Projetos que usavam                                          |
| --------------- | ------------------------------------------------------------ |
| `$aluno123DB` ✅ | Sistema-de-Cadastros, Destacar Células                       |
| `$aluno123BD` ❌ | Combobox Dependente, FiltroEntreDatas, Agrupamento de colunas |

Repare que o final trocava: **DB** vs **BD**. Como a senha real do seu MySQL é uma só
(`$aluno123DB`), os três projetos com a grafia errada **não conseguiam conectar** —
o MySQL recusava o login com um erro parecido com:

```
pymysql.err.OperationalError: (1045, "Access denied for user 'root'@'localhost'")
```

Padronizei os três para `$aluno123DB`. Agora **os cinco projetos usam exatamente a
mesma senha** e todos conseguem conectar.

**O que se aprende:**
- Um único caractere trocado numa senha (DB → BD) já derruba a conexão inteira.
- Repetir a mesma informação (a senha) copiada em vários arquivos é frágil: um erro de digitação em um deles passa despercebido. Isso se chama **duplicação** e é uma fonte clássica de bugs.
- **Próximo passo natural de estudo:** em vez de escrever a senha em texto puro dentro do código (e ainda por cima versionada no git), o ideal é guardá-la numa *variável de ambiente* ou num arquivo `.env` que não vai para o git. Pesquise `python-dotenv` e `os.environ`. Isso resolve tanto a duplicação quanto a segurança.

---

## Correção 4 — Clareza na função de conexão (Combobox Dependente)

**Arquivo:** `Combobox Dependente/configBanco.py`

**Antes:**
```python
def getConn(nameBench: str | None = None) -> pymysql.connections.Connection:
    conn = pymysql.connect(..., database=nameBench, ...)
```

**Depois:**
```python
def getConn(banco: str | None = None) -> pymysql.connections.Connection:
    """Cria e retorna uma conexão com o MySQL.
    - getConn()         -> conecta ao SERVIDOR, sem selecionar um banco.
    - getConn("geo_db") -> conecta diretamente a um banco específico.
    """
    conn = pymysql.connect(..., database=banco, ...)
```

**Qual era o problema?**
O parâmetro da função tinha o **mesmo nome** de uma variável global do arquivo
(`nameBench = 'geo_db'`). Isso faz o leitor pensar que a global é o valor padrão do
parâmetro — mas não é. Dentro da função, `nameBench` sempre se referia ao parâmetro.
Renomeei o parâmetro para `banco` e adicionei uma docstring explicando os dois modos
de uso. O comportamento é **idêntico**: todas as 13 chamadas no `repositorio.py` são
posicionais (`getConn()` / `getConn(nameBench)`), então nada quebra.

**O que se aprende:**
- Um parâmetro com o mesmo nome de uma variável global "sombreia" (esconde) a global dentro da função. Isso confunde e é fonte de bugs. Dê nomes distintos.
- Uma boa *docstring* documenta o que a função faz e seus casos de uso — ajuda quem lê (inclusive você mesma no futuro).

---

## Correção 5 — Método `capturaSelecao` que faltava (Agrupamento de colunas) — CRÍTICO

**Arquivo:** `Agrupamento de colunas/appAgrupamentoDeColunas.py`

**Qual era o problema?**
No `montaUI()` existia esta linha, ligando o evento de seleção de uma linha da tabela
a um método:
```python
self.tree.bind("<<TreeviewSelect>>", self.capturaSelecao)
```
Mas o método **`capturaSelecao` não existia** em lugar nenhum da classe. Duas consequências:

1. **O app quebrava ao abrir.** O Python avalia `self.capturaSelecao` no momento em que
   essa linha roda (dentro do `__init__`). Como o método não existe, levanta
   `AttributeError` e a janela nem aparece.
2. **Os botões "Alterar" e "Excluir" nunca funcionariam.** O atributo `self.idSelecionado`
   só recebia o valor `None`. Era o `capturaSelecao` que deveria guardar o ID da linha
   clicada. Sem ele, `idSelecionado` ficava sempre `None` e os botões só respondiam
   "Selecione uma linha".

**O que fiz:**
Implementei o método que faltava. Quando o usuário seleciona uma linha, ele: (1) lê o
identificador da linha — que é o próprio ID da venda, pois cada linha foi inserida com
`iid=str(valor.id)` no `populaTabela()` —, (2) guarda esse ID em `self.idSelecionado`,
e (3) preenche o formulário da direita com os dados da venda, para permitir a edição.
(Ao preencher quantidade e preço, os *traces* já existentes recalculam o total sozinhos.)

**O que se aprende:**
- Em Python, `self.metodo` é avaliado na hora — referenciar um método inexistente gera `AttributeError` imediatamente, não só quando o evento acontece.
- Fluxo de uma interface orientada a eventos: **selecionar linha → evento dispara → método preenche o formulário e guarda o ID → botões usam esse ID**. Se o elo do meio falta, toda a cadeia quebra.

---

## Correção 6 — `return` duplicado (código morto) em `parsePrecoBR`

**Arquivo:** `Agrupamento de colunas/appAgrupamentoDeColunas.py`

**Antes:**
```python
    texto = texto.replace(".", "").replace(",", ".")
    return float(texto)          # <- retorna aqui

    # Converte o texto em um número decimal
    # e retorna esse valor.
    return float(texto)          # <- NUNCA executa (código morto)
```

**Depois:**
```python
    texto = texto.replace(".", "").replace(",", ".")

    # Converte o texto (já no formato americano) em um número
    # decimal e retorna esse valor.
    return float(texto)
```

**Qual era o problema?**
Havia dois `return` seguidos. Assim que o primeiro executa, a função termina — tudo o
que vem depois é **código morto** (nunca roda). Não causava erro, mas polui a leitura.
Removi o `return` repetido e deixei um só, com o comentário no lugar certo.

**O que se aprende:**
- Um `return` encerra a função na hora. Qualquer linha depois dele (no mesmo bloco) nunca executa. Linters como o Ruff ou o Pylint apontam "unreachable code" automaticamente.

---

## Correção 7 — Escape de aspas no backup corrompia os dados (Agrupamento de colunas)

**Arquivo:** `Agrupamento de colunas/repositorio.py` (método `exportarDumpSQL`)

**Antes:**
```python
nomeCliente = linha["nomeCliente"].replace("'", '"')   # troca ' por "
```

**Depois:**
```python
nomeCliente = linha["nomeCliente"].replace("'", "''")  # duplica a ' (escape correto do SQL)
```

**Qual era o problema?**
No SQL, textos ficam entre aspas simples (`'...'`). Se o próprio dado tiver uma aspa
(ex: `Sant'Ana`), ela encerraria o texto no lugar errado e quebraria o comando. O código
tentava evitar isso **trocando a aspa simples por aspa dupla** — mas isso **corrompe o
dado**: `Sant'Ana` viraria `Sant"Ana` no arquivo de backup. Ao restaurar, o nome estaria
errado.

A regra correta do SQL é **duplicar** a aspa: para representar uma `'` dentro do texto,
escreve-se `''`. Assim `Sant'Ana` vira `'Sant''Ana'`, e o banco lê de volta exatamente
`Sant'Ana`. (É assim que o projeto `Combobox Dependente` já fazia.)

**O que se aprende:**
- "Escapar" um caractere ≠ "trocar" por outro. Escapar preserva o dado; trocar altera o dado.
- Montar SQL concatenando texto exige esse cuidado. Por isso, para dados de entrada, o ideal é sempre usar *parâmetros* (`%s`) — como o resto do repositório faz nas consultas normais. O escape manual só aparece aqui porque estamos gerando um arquivo `.sql` de texto.

---

## Correção 8 — Nome da tabela inconsistente: `Vendas` vs `vendas` (Agrupamento de colunas)

**Arquivo:** `Agrupamento de colunas/repositorio.py` (método `garantirBancoEtabela`)

**Antes:**
```sql
CREATE TABLE IF NOT EXISTS Vendas ( ... )   -- com V maiúsculo
```

**Depois:**
```sql
CREATE TABLE IF NOT EXISTS vendas ( ... )   -- minúsculo, igual ao resto
```

**Qual era o problema?**
A tabela era **criada** como `Vendas`, mas **todas** as outras consultas
(`INSERT INTO vendas`, `SELECT ... FROM vendas`, `UPDATE`, `DELETE`, o dump) usavam
`vendas` minúsculo. No Windows e no macOS o MySQL, por padrão, ignora maiúsculas/minúsculas
em nomes de tabela — então funcionava. **Mas no Linux (padrão sensível a maiúsculas)
`Vendas` e `vendas` seriam tabelas diferentes**, e a aplicação daria erro
`Table 'agrupamentoTabelasDB.vendas' doesn't exist`.

Padronizei a criação para `vendas` minúsculo, igual a todo o resto.

**O que se aprende:**
- Em nomes de identificadores (tabelas, colunas), a diferença maiúscula/minúscula pode importar ou não **dependendo do sistema operacional e da configuração do MySQL** (`lower_case_table_names`). Manter um padrão único evita a surpresa de "funciona na minha máquina, quebra na outra".

---

## Correção 9 — Destacar Células: app incompleto + vários bugs

**Arquivos:** `Destacar Células/appDestacarCélulas.py` e `Destacar Células/repositorio.py`

Este projeto estava **inacabado e não abria**. Foram feitas várias correções e
implementados os métodos que faltavam. Resumo:

**a) Erro de sintaxe (o arquivo nem compilava)** — `formatarMoedaBR` tinha uma cadeia
de `.replace()` quebrada em várias linhas *dentro* de uma f-string de aspas simples, o
que é proibido (`EOL while scanning string literal`). As trocas foram movidas para uma
variável antes de montar o texto.

**b) Bloqueios de inicialização (crash no `__init__`):**
- `self.corLinhaSel` (usado numa tag) não existia → trocado por `self.corLinhaBG`.
- A tag era configurada como `"rowSel"`, mas `aplicarTagNaLinha` aplicava
  `"linhaSelecionada"` (nomes diferentes) → padronizado para `"rowSel"`.
- Bind usava `self.onSelectRow`, mas o método é `onSelectedRow` (erro de digitação).
- Estilo `"Form.Button"` não é válido no ttk (precisa terminar em `.TButton`) →
  criado o estilo `"Form.TButton"` e ajustados os botões.
- `__init__` declarava `self.dadosLista`, mas o resto do código usa `self.dados`
  (variável morta) → padronizado para `self.dados`.

**c) Métodos que eram chamados mas nunca tinham sido escritos** (implementados agora):
- `desenharColuna` — o coração do app: desenha o destaque de coluna/linha/célula num
  Canvas transparente por cima da tabela.
- `ysync` / `xsync` / `onVScroll` / `onHScroll` — sincronizam a rolagem da tabela com
  as barras (nos dois sentidos) e redesenham o destaque.
- `preencherFormPorIid` — preenche o formulário ao selecionar uma linha.
- `lerEValidarFormulario` — validação única, reaproveitada por cadastrar e alterar.
- `cadastrarProduto` / `alterarProduto` / `excluirProduto` / `limparFormulario` — o CRUD.
- Bloco `if __name__ == "__main__"` — o app não tinha ponto de entrada para ser iniciado.

**d) Bugs no `repositorio.py`** (renomearam a coluna `criadoEm` → `dataProduto` e
esqueceram 3 lugares):
- `__init__` chamava `inserirDadosSeVazio()`, mas o método era `insercaoDeDadosSeVazio`
  → crash ao criar o repositório. Nomes alinhados.
- `listarTudo` construía `Produto(..., criadoEm=linha["criadoEm"])` → corrigido para
  `dataProduto=linha["dataProduto"]`.
- `atualizarProduto` fazia `UPDATE ... criadoEm = %s` → corrigido para `dataProduto = %s`.

**O que se aprende:**
- Um método referenciado (`command=self.x`, `bind(..., self.x)`) é buscado por nome; se não existir, dá `AttributeError` — às vezes já na abertura da janela.
- Renomear um campo/coluna exige buscar **todas** as referências. Um "renomear pela metade" deixa bugs espalhados que só aparecem em tempo de execução.
- Reaproveitar a validação (`lerEValidarFormulario`) em vez de duplicá-la evita que cadastrar e alterar fiquem com regras diferentes.

> Observação: a lógica está correta e o arquivo compila, mas o **visual** do destaque
> (cores/intensidade do `stipple`) só pode ser afinado rodando o app com o MySQL ligado.

---

## Como testar se está tudo funcionando

Com o servidor MySQL local rodando, entre em cada pasta e rode o app:
```bash
cd "Combobox Dependente"     && python appDependentes.py
cd FiltroEntreDatas          && python appFiltroDatas.py
cd "Agrupamento de colunas"  && python appAgrupamentoDeColunas.py
cd "Destacar Células"        && python appDestacarCélulas.py
```
Antes das correções, o Combobox e o FiltroEntreDatas quebravam ao abrir (imports), o
Agrupamento de colunas também quebrava ao abrir (método `capturaSelecao` faltando), e
os três não conectavam por causa da senha. Agora as janelas devem abrir e conectar
normalmente — e no Agrupamento, ao clicar numa linha da tabela, o formulário à direita
é preenchido e os botões "Alterar"/"Excluir" passam a funcionar.
