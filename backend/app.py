from flask import Flask
from routes import configurar_rotas

app = Flask(__name__)

configurar_rotas(app)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
