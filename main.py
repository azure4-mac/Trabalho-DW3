from flask import Flask, request, jsonify
import psycopg
import requests

app = Flask(__name__)

connection_db = psycopg.connect("dbname=mac user=postgres password=3f@db host=164.90.152.205 port=80")

# Endpoint para buscar por NOME
@app.route('/filme/nome/<nome>', methods=['GET'])
def buscar_filme_nome(nome):
    with connection_db.cursor() as cur:
        # Buscar no banco
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
                "mensagem": f"{len(resultado)} filme(s) encontrado(s) no banco.",
                "filmes": resultado
            })

        # Se não achar, buscar na OMDb
        try:
            resposta = requests.get(f"https://www.omdbapi.com/?t={nome}&apikey=58cc3cb5")
            resposta.raise_for_status() 
        except requests.exceptions.RequestException as e:
            return jsonify({
                "mensagem": "Erro ao acessar a OMDb",
                "erro": str(e)
            }), 500

        if resposta.status_code == 200:
            dados = resposta.json()

            if dados.get('Response') == 'True':
                try:
                    # Salvar no banco
                    cur.execute("""
                        INSERT INTO filmes (imdb_id, titulo, ano, tipo)
                        VALUES (%s, %s, %s, %s)
                    """, (dados['imdbID'], dados['Title'], dados['Year'], dados['Type']))
                    connection_db.commit()
                except psycopg.Error as db_error:
                    return jsonify({
                        "mensagem": "Erro ao salvar filme no banco",
                        "erro": str(db_error)
                    }), 500

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
                return jsonify({
                    "mensagem": "Título não encontrado.",
                    "erro": "Não foi encontrado nenhum título com esse nome, nem no banco de dados, nem na API OMDb (a pesquisa inclui filmes e séries)."
                }), 404  # não encontrado

        else:
            return jsonify({
                "mensagem": "Título não encontrado.",
                "erro": "Não foi encontrado nenhum título com esse nome, nem no banco de dados, nem na API OMDb (a pesquisa inclui filmes e séries)."
            }), 404  # não encontrado

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
        try:
            resposta = requests.get(f"https://www.omdbapi.com/?i={imdb_id}&apikey=58cc3cb5")
            resposta.raise_for_status() 
        except requests.exceptions.RequestException as e:
            return jsonify({
                "mensagem": "Erro ao acessar a OMDb",
                "erro": str(e)
            }), 500

        if resposta.status_code == 200:
            dados = resposta.json()

            if dados.get('Response') == 'True':
                try:
                    # Salvar no banco
                    cur.execute("""
                        INSERT INTO filmes (imdb_id, titulo, ano, tipo)
                        VALUES (%s, %s, %s, %s)
                    """, (dados['imdbID'], dados['Title'], dados['Year'], dados['Type']))
                    connection_db.commit()
                except psycopg.Error as db_error:
                    return jsonify({
                        "mensagem": "Erro ao salvar filme no banco",
                        "erro": str(db_error)
                    }), 500

                return jsonify({
                    "mensagem": "Filme encontrado na OMDb e salvo no banco",
                    "filme": {
                        "imdb_id": dados['imdbID'],
                        "titulo": dados['Title'],
                        "ano": dados['Year'],
                        "tipo": dados['Type']
                    }
                })
                # Caso nao tenha
            else:
                return jsonify({
                    "mensagem": "Título não encontrado.",
                    "erro": "Não foi encontrado nenhum título com esse ID, nem no banco de dados, nem na API OMDb (a pesquisa inclui filmes e séries)."
                }), 404  # não encontrado

      
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)