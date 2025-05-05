# Trabalho-DW3 
Olá seja bem vindo ao nosso programa de busca de informações de filmes, para utilizar-lo voce fara isso por meio de requisições HTTP, colocando no final da requisição o nome do filme que deseja (tanto faz se você escrever em minúsculo ou maiúsculo, porem recomendo não utilizar acentuação), caso tenhamos ele em nosso banco de dados o retornaremos para voce em formato json, caso não tenhamos utilizaremos a api OMDb para pesquisar e retornar para voce as informações em formato json, alem de salvar em nosso banco para da proxima vez que necessitar estar la, certo mas o que voce recebera nesse json? O titulo, o ano de lançamento e o tipo(filme, serie ou episodio).
# Exemplo de como fazer a requisição 
http://164.90.152.205:80/filme/nome/Matrix
# O que sera exibido?(se tiver no banco) #
{
  "mensagem": "1 filme(s) encontrado(s).",
  "filmes": [
    {
      "id": 1,
      "imdb_id": "tt0120338",
      "titulo": "Titanic",
      "ano": "1997",
      "tipo": "movie"
    }
  ]
}
# O que sera exibido?(se não tiver banco) #
{
  "mensagem": "Filme encontrado na OMDb e salvo no banco",
  "filme": {
    "imdb_id": "tt0120338",
    "titulo": "Titanic",
    "ano": "1997",
    "tipo": "movie"
  }
}
