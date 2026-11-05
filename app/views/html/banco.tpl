<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Banco</title>
</head>
<body>
    <h1>Banco - Produtos cadastrados</h1>
    <p>Usuário autenticado: {{current_user.username}}</p>

    <table border="1" cellpadding="6">
        <tr><th>ID</th><th>Nome</th><th>Preço (R$)</th></tr>
        % for produto in produtos:
        <tr>
            <td>{{produto.id}}</td>
            <td>{{produto.nome}}</td>
            <td>{{'%.2f' % produto.preco}}</td>
        </tr>
        % end
    </table>
</body>
</html>
