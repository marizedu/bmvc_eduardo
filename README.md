# Sistema BMVC: portal e banco (Produto)

Sistema desenvolvido a partir do framework BMVC (Bottle + MVC), mantendo a mesma arquitetura: as rotas ficam em `route.py` e apenas delegam para o controlador `Application` (`app/controllers/application.py`), que administra as actions pelo dicionário `pages` e compõe um objeto `DataRecord` (`app/controllers/datarecord.py`), responsável pela persistência em um banco SQLite na pasta `app/controllers/db`; os modelos `UserAccount` e `Produto` ficam em `app/models` e as páginas `.tpl` em `app/views/html`. O recurso **portal** faz o login dos usuários (modelo `UserAccount`): ao autenticar, o `DataRecord` gera um `session_id` com `uuid` e o controlador o grava em um cookie, verificado pelo método `require_login` em todas as actions do banco. O recurso **banco** só responde a usuários autenticados e apresenta a lista de objetos cadastrados, com o tema `Produto` (atributos nome e preço); o READ é feito no próprio sistema, na página `/banco`, enquanto o CREATE (`POST /banco/create`) e o DELETE (`DELETE /banco/delete/<id>`) são feitos via cURL no terminal Linux, enviando o cookie da sessão obtido no login do portal.

## Como executar

```bash
pip install bottle
python3 route.py
```

Abra http://localhost:8080/portal e entre com `admin` / `admin`. Depois do login, `/banco` mostra os produtos cadastrados. O arquivo `banco.db` é criado automaticamente.

## CREATE e DELETE via cURL

```bash
# login no portal (guarda o cookie de sessão)
curl -c cookies.txt -d "username=admin&password=admin" http://localhost:8080/portal

# CREATE
curl -b cookies.txt -X POST -d "nome=Teclado&preco=99.90" http://localhost:8080/banco/create

# DELETE
curl -b cookies.txt -X DELETE http://localhost:8080/banco/delete/1
```
