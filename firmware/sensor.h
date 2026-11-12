#ifndef SENSOR_H
#define SENSOR_H

#include "DHT.h"

class Sensor {

private:
    const int pino;
    const int tipo;
    DHT dht;

public:
    Sensor(int pino, int tipo);

    void iniciar();

    bool ler(float &temperatura, float &umidade);
};

#endif
