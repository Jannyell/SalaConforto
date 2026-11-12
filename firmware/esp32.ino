#include "Sensor.h"
#include "WifiConector.h"
#include "credenciais.h"

// CONFIGURAÇÕES DO SENSOR
#define DHTPIN 17
#define DHTTYPE DHT22

// INSTÂNCIAS DOS MÓDULOS
Sensor sensor(DHTPIN, DHTTYPE);

WifiConector wifi;

void setup() {

    Serial.begin(115200);

    // Inicializa o sensor
    sensor.iniciar();

    // Conecta ao Wi-Fi
    wifi.iniciar();
}


void loop() {

    // Verifica a conexão Wi-Fi
    if (!wifi.conectado()) {

        Serial.println("Wi-Fi desconectado. Reconectando...");

        wifi.iniciar();
        return;
    }

    float temperatura;
    float umidade;

    // Realiza a leitura do sensor
    if (sensor.ler(temperatura, umidade)) {

        Serial.println("\n--- NOVA LEITURA ---");

        Serial.print("Temperatura: ");
        Serial.print(temperatura);
        Serial.print(" °C | ");

        Serial.print("Umidade: ");
        Serial.print(umidade);
        Serial.println(" %");

        // Envia os dados para a API
        if (wifi.enviarDados(temperatura, umidade)) {

            Serial.println("Dados enviados com sucesso!");

        } else {

            Serial.println("Falha ao enviar os dados.");
        }

    } else {

        Serial.println("Falha na leitura do sensor.");
    }


    delay(INTERVALO_ENVIO);
}
