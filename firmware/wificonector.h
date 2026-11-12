#ifndef WIFI_CONECTOR_H
#define WIFI_CONECTOR_H

class WifiConector {

public:
    void iniciar();

    bool conectado();

    bool enviarDados(float temperatura, float umidade);
};

#endif
