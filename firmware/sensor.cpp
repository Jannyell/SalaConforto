#include "Sensor.h"

Sensor::Sensor(int pino, int tipo)
    : pino(pino), tipo(tipo), dht(pino, tipo) {
}

void Sensor::iniciar() {
    dht.begin();
}

bool Sensor::ler(float &temperatura, float &umidade) {

    temperatura = dht.readTemperature();
    umidade = dht.readHumidity();

    // Verifica se a leitura foi válida
    if (isnan(temperatura) || isnan(umidade)) {
        return false;
    }

    return true;
}
