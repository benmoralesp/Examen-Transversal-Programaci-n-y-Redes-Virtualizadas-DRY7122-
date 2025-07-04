import requests
import urllib.parse

# Clave API de Graphhopper (pon aquí tu propia clave)
key = "96d56480-da58-4292-9113-708efb88c010"

# URLs base
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"

def geocoding(location, key):
    # Armar URL de geocodificación
    geo_params = {"q": location, "limit": 1, "key": key}
    url = geocode_url + urllib.parse.urlencode(geo_params)
    response = requests.get(url)
    status = response.status_code
    data = response.json()
    if status == 200 and data['hits']:
        lat = data["hits"][0]["point"]["lat"]
        lon = data["hits"][0]["point"]["lng"]
        name = data["hits"][0]["name"] + ", " + data["hits"][0]["country"]
        print("URL de Geocodificación para {}: \n{}".format(location, url))
        return (status, lat, lon, name)
    else:
        print("No se pudo obtener coordenadas para: {}".format(location))
        return (status, None, None, None)

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Medios de transporte disponibles:")
    print("auto, bicicleta, a pie")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    medio = input("Ingrese el medio de transporte (o 's' para salir): ").strip().lower()
    if medio == "s":
        break

    # Mapeo español -> inglés
    if medio == "auto":
        vehicle = "car"
    elif medio == "bicicleta":
        vehicle = "bike"
    elif medio == "a pie":
        vehicle = "foot"
    else:
        vehicle = "car"
        print("No se ingresó un medio válido. Se usará 'auto'.")

    origen = input("Ciudad de Origen (o 's' para salir): ").strip()
    if origen.lower() == "s":
        break
    destino = input("Ciudad de Destino (o 's' para salir): ").strip()
    if destino.lower() == "s":
        break

    orig = geocoding(origen, key)
    dest = geocoding(destino, key)
    print("=================================================")

    if orig[0] == 200 and dest[0] == 200 and orig[1] and dest[1]:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        ruta_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        response = requests.get(ruta_url)
        status_ruta = response.status_code
        data_ruta = response.json()
        print("Estado de la API de Routing: {}".format(status_ruta))
        print("URL de Routing:\n{}".format(ruta_url))
        print("=================================================")
        print("Ruta desde {} hasta {} en {}".format(orig[3], dest[3], medio))
        print("=================================================")

        if status_ruta == 200:
            # Distancia en metros y conversión
            metros = data_ruta["paths"][0]["distance"]
            km = metros / 1000
            millas = km / 1.61
            # Tiempo en ms -> h:m:s
            tiempo_ms = data_ruta["paths"][0]["time"]
            seg = int(tiempo_ms / 1000 % 60)
            min = int(tiempo_ms / 1000 / 60 % 60)
            hr = int(tiempo_ms / 1000 / 60 / 60)

            print("Distancia recorrida: {:.1f} km / {:.1f} millas".format(km, millas))
            print("Duración del viaje: {:02d}:{:02d}:{:02d}".format(hr, min, seg))
            print("=================================================")

            # Narrativa paso a paso
            for step in data_ruta["paths"][0]["instructions"]:
                texto = step["text"]
                dist = step["distance"]
                print("{} ({:.2f} km / {:.2f} millas)".format(
                    texto, dist/1000, dist/1000/1.61))
            print("=================================================")

        else:
            print("Error al obtener la ruta: {}".format(data_ruta.get("message", "Sin mensaje")))
            print("*************************************************")

    else:
        print("No se pudieron obtener coordenadas válidas para ambas ciudades.")
