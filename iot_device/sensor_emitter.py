import paho.mqtt.client as mqtt
import json
import time
import random

# CONFIGURACIÓN MQTT 
BROKER = "broker.hivemq.com"
PORT = 1883

ESTACIONES_IDS = [1, 2, 3, 4]

def leer_sensor_emulado():
    return round(random.uniform(10.0, 85.0), 2)

def enviar_telemetria():
    print("--- Iniciando Emisor IoT Multi-Estación (Vía MQTT) ---")
    print(f"Conectando al Broker: {BROKER}")
    print(f"Monitoreando estaciones con IDs: {ESTACIONES_IDS}\n")

    # Inicializar el cliente MQTT local
    client = mqtt.Client()
    try:
        client.connect(BROKER, PORT)
    except Exception as e:
        print(f"[CRÍTICO] No se pudo conectar al Broker MQTT: {e}")
        return

    while True:
        hay_alerta_global = False

        for estacion_id in ESTACIONES_IDS:
            valor = leer_sensor_emulado()

            payload = {
                "valor": valor,
                "timestamp": time.time()
            }

            topic = f"fisi/smat/estaciones/{estacion_id}"

            try:

                client.publish(topic, json.dumps(payload))
                
                if valor > 70:
                    print(f"[ALERTA] Publicado en MQTT -> Estación ID {estacion_id}: ¡CRÍTICO! {valor} cm")
                    hay_alerta_global = True
                else:
                    print(f"[OK] Publicado en MQTT -> Estación ID {estacion_id}: {valor} cm")

            except Exception as e:
                print(f"[ERROR] Falló el envío MQTT para la estación {estacion_id}: {e}")

        print("-" * 50)

        if hay_alerta_global:
            print("[MODO EMERGENCIA] Hay alertas activas. Próxima ronda en 3 segundos...\n")
            time.sleep(3)
        else:
            print("[SISTEMA ESTABLE] Próxima ronda de telemetría en 10 segundos...\n")
            time.sleep(10)

if __name__ == "__main__":
    enviar_telemetria()