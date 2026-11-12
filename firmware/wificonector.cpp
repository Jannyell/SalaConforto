
#include "WifiConector.h"

#include <WiFi.h>
#include <HTTPClient.h>

#include "credenciais.h"

// --------------------------------------
// INICIA A CONEXÃO WI-FI
// --------------------------------------

void WifiConector::iniciar() {

    Serial.println("Conectando ao Wi-Fi...");

    // Define o ESP32 como dispositivo cliente
    WiFi.mode(WIFI_STA);

    // Limpa uma possível configuração anterior
    WiFi.disconnect(true);

    delay(1000);

    // Habilita a reconexão automática
    WiFi.setAutoReconnect(true);

    // Inicia a conexão
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    int tentativas = 0;

    // Aguarda a conexão por até 20 segundos
    while (!conectado() && tentativas < 40) {

        delay(500);

        Serial.print(".");

        tentativas++;
    }

    if (conectado()) {

        Serial.println("\nWi-Fi conectado!");

        Serial.print("IP do ESP32: ");
        Serial.println(WiFi.localIP());

        Serial.print("Intensidade do sinal: ");
        Serial.print(WiFi.RSSI());
        Serial.println(" dBm");

    } else {

        Serial.println("\nFalha ao conectar ao Wi-Fi.");
    }
}

// --------------------------------------
// VERIFICA A CONEXÃO
// --------------------------------------

bool WifiConector::conectado() {

    return WiFi.status() == WL_CONNECTED;
}

// --------------------------------------
// ENVIA DADOS PARA A API FLASK
// --------------------------------------

bool WifiConector::enviarDados(float temperatura, float umidade) {

    if (!conectado()) {

        Serial.println("Wi-Fi desconectado.");

        return false;
    }

    HTTPClient http;

    // Inicia a comunicação com a API
    if (!http.begin(API_URL)) {

        Serial.println("Falha ao iniciar conexão HTTP.");

        return false;
    }

    // Define o tempo limite da requisição
    http.setTimeout(5000);

    http.addHeader("Content-Type", "application/json");

    // Monta o JSON
    String json = "{";
    json += "\"temperatura\":" + String(temperatura, 2) + ",";
    json += "\"umidade\":" + String(umidade, 2);
    json += "}";

    Serial.println("Enviando dados para a API...");
    Serial.println(json);

    // Envia os dados
    int resposta = http.POST(json);

    bool sucesso = false;

    if (resposta > 0) {

        Serial.print("Resposta da API: ");
        Serial.println(resposta);

        // Considera respostas HTTP entre 200 e 299 como sucesso
        sucesso = resposta >= 200 && resposta < 300;

    } else {

        Serial.print("Erro HTTP: ");
        Serial.println(http.errorToString(resposta));
    }

    // Encerra a comunicação HTTP
    http.end();

    return sucesso;
}
