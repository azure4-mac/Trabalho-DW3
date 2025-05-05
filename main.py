from flask import Flask, request, jsonify
import psycopg
import requests

app = Flask(__name__)

connection_db = psycopg.connect("dbname=mac user=postgres password=3f@db host=164.90.152.205 port=80")

# Endpoint para buscar por NOME
@app.route('/filme/nome/<nome>', methods=['GET'])
def buscar_filme_nome(nome):
    with connection_db.cursor() as cur:
        cur.execute("SELECT * FROM filmes WHERE titulo ILIKE %s", (f"%{nome}%",))
        filmes = cur.fetchall()

        if filmes:
            resultado = []
            for filme in filmes:
                resultado.append({
                    "id": filme[0],
                    "imdb_id": filme[1],
                    "titulo": filme[2],
                    "ano": filme[3],
                    "tipo": filme[4]
                })

            return jsonify({
                "mensagem": f"{len(resultado)} filme(s) encontrado(s).",
                "filmes": resultado
            })

        # Se não achar, buscar na OMDb
        resposta = requests.get(f"http://www.omdbapi.com/?t={nome}&apikey=58cc3cb5")
        print(resposta)  
        if resposta.status_code == 200:
            dados = resposta.json()

            if dados.get('Response') == 'True':  # Verifica se a resposta é verdadeira
                # Salvar no banco
                cur.execute("""
                    INSERT INTO filmes (imdb_id, titulo, ano, tipo)
                    VALUES (%s, %s, %s, %s)
                """, (dados['imdbID'], dados['Title'], dados['Year'], dados['Type']))
                connection_db.commit()

                return jsonify({
                    "mensagem": "Filme encontrado na OMDb e salvo no banco",
                    "filme": {
                        "imdb_id": dados['imdbID'],
                        "titulo": dados['Title'],
                        "ano": dados['Year'],
                        "tipo": dados['Type']
                    }
                })
            else:
                # Caso o filme não seja encontrado na OMDb
                return jsonify({
                    "mensagem": "Filme não encontrado na OMDb.",
                    "erro": "Nenhum filme encontrado com esse nome na API OMDb."
                }), 404  # Código de status HTTP 404 (não encontrado)

# Endpoint para buscar por ID
@app.route('/filme/id/<imdb_id>', methods=['GET'])
def buscar_filme_id(imdb_id):
    with connection_db.cursor() as cur:
        # Procurar no banco
        cur.execute("SELECT * FROM filmes WHERE imdb_id = %s", (imdb_id,))
        filme = cur.fetchone()

        if filme:
            return jsonify({
                "mensagem": "Filme encontrado no banco",
                "filme": {
                    "id": filme[0],
                    "imdb_id": filme[1],
                    "titulo": filme[2],
                    "ano": filme[3],
                    "tipo": filme[4]
                }
            })

        # Se não achar, buscar na OMDb
        resposta = requests.get(f"http://www.omdbapi.com/?i={imdb_id}&apikey=58cc3cb5")

        if resposta.status_code == 200:
            dados = resposta.json()

            if dados.get('Response') == 'True':  # Verifica se a resposta é verdadeira
                # Salvar no banco
                cur.execute("""
                    INSERT INTO filmes (imdb_id, titulo, ano, tipo)
                    VALUES (%s, %s, %s, %s)
                """, (dados['imdbID'], dados['Title'], dados['Year'], dados['Type']))
                connection_db.commit()

                return jsonify({
                    "mensagem": "Filme encontrado na OMDb e salvo no banco",
                    "filme": {
                        "imdb_id": dados['imdbID'],
                        "titulo": dados['Title'],
                        "ano": dados['Year'],
                        "tipo": dados['Type']
                    }
                })
            else:
                # Caso o filme não seja encontrado na OMDb
                return jsonify({
                    "mensagem": "Filme não encontrado na OMDb.",
                    "erro": "Nenhum filme encontrado com esse ID na API OMDb."
                }), 404  # Código de status HTTP 404 (não encontrado)
