from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:

# Recurso PORTAL: login de usuários (modelo UserAccount)

@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')


@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    return ctl.login(username, password)


# Recurso BANCO: lista de objetos cadastrados (modelo Produto)
#   GET    /banco              READ   (no próprio sistema)
#   POST   /banco/create       CREATE (via cURL)
#   DELETE /banco/delete/<id>  DELETE (via cURL)

@app.route('/banco', method='GET')
def action_banco():
    return ctl.render('banco')


@app.route('/banco/create', method='POST')
def action_banco_create():
    return ctl.render('banco_create')


@app.route('/banco/delete/<id:int>', method='DELETE')
def action_banco_delete(id):
    return ctl.render('banco_delete', id)


#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
