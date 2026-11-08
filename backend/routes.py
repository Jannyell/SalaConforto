
from flask import request, jsonify

import services.leitura_service as service

def configurar_rotas(app):

    @app.route("/", methods=["GET"])
    def inicio():
        return jsonify({"mensagem": "API SalaConforto funcionando!"}), 200

    @app.route("/api/leituras", methods=["POST"])
    def receber_leitura():
        resultado, status = service.registrar_leitura(request.get_json(silent=True))
        return jsonify(resultado), status

    @app.route("/api/leituras/ultima", methods=["GET"])
    def ultima_leitura():
        resultado, status = service.obter_ultima_leitura()
        return jsonify(resultado), status

    @app.route("/api/leituras", methods=["GET"])
    def todas_leituras():
        resultado, status = service.listar_leituras()
        return jsonify(resultado), status
