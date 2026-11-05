from app.controllers.datarecord import DataRecord
from bottle import template, redirect, request, response


class Application():

    def __init__(self):

        self.pages = {
            'portal': self.portal,
            'banco': self.banco,
            'banco_create': self.banco_create,
            'banco_delete': self.banco_delete
        }

        self.__model = DataRecord()


    def render(self, page, parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        else:
            return content(parameter)


    def get_session_id(self):
        return request.get_cookie('session_id')


    # O navegador envia "Accept: text/html"; o cURL não.
    def is_browser(self):
        return 'text/html' in request.headers.get('Accept', '')


    def helper(self):
        return template('app/views/html/helper')


    # ---------------- recurso PORTAL ----------------

    def portal(self):
        return template('app/views/html/portal')


    def login(self, username, password):
        session_id = self.__model.checkUser(username, password)
        if session_id:
            response.set_cookie('session_id', session_id, httponly=True, max_age=3600)
            if self.is_browser():
                redirect('/banco')
            return 'Login realizado\n'
        if self.is_browser():
            redirect('/portal')
        response.status = 401
        return 'Usuário ou senha inválidos\n'


    def current_user(self):
        return self.__model.getCurrentUser(self.get_session_id())


    def require_login(self):
        """Interrompe a action se não houver usuário autenticado."""
        if self.current_user() is None:
            if self.is_browser():
                redirect('/portal')
            response.status = 401
            return 'Não autenticado: faça login em /portal\n'
        return None


    # ---------------- recurso BANCO ----------------

    def banco(self):
        erro = self.require_login()
        if erro:
            return erro
        produtos = self.__model.getProdutos()
        return template('app/views/html/banco', current_user=self.current_user(), produtos=produtos)


    def banco_create(self):
        erro = self.require_login()
        if erro:
            return erro
        nome = request.forms.get('nome')
        preco = request.forms.get('preco')
        if not nome or not preco:
            response.status = 400
            return 'Use: curl -b cookies.txt -X POST -d "nome=...&preco=..." http://localhost:8080/banco/create\n'
        produto = self.__model.addProduto(nome, float(preco))
        return f'Produto criado com id {produto.id}\n'


    def banco_delete(self, id):
        erro = self.require_login()
        if erro:
            return erro
        if self.__model.deleteProduto(id):
            return f'Produto {id} removido\n'
        response.status = 404
        return f'Produto {id} não encontrado\n'
