from mutante_bd import mutante, consulta
from flask import Flask, request, json

appMutante = Flask(__name__)

@appMutante.route("/mutante", methods=["GET", "POST"])
def analizar_adn():
    """Consume el API que analiza el ADN suministrado, devuelve si es mutante o no y
        lo inserta en la BBDD si no es repetido
    
    Parámetros:
      Ninguno

    Excepciones:
      Solo se procesa por POST

      """

    if request.method == "POST":
        data = request.get_json()
        es_mutante, mensaje = mutante(data)
        if es_mutante:
            response = appMutante.response_class(
                response=json.dumps({"status":"success","data":{"verificacion":mensaje}}),
                status=200,
                mimetype='application/json')
        else:
            response = appMutante.response_class(
                response=json.dumps({"error":"error","data":{"error":mensaje}}),
                status=403,
                mimetype='application/json')
        return response
    else:
        response = appMutante.response_class(
            response=json.dumps({"status":"error","data":{"error":"ADN para revisión no recibido"}}),
            status=403,
            mimetype='application/json')
        return response
 

@appMutante.route("/stats", methods=["GET","POST"])
def consultar_adn():
    """Se consulta la relación y frecuena de mutantes y no mutantes

    Parámetros:
      Ninguno

    Excepciones:
      Error en la ejecución de la consulta

      """

    error, verificacion = consulta()

    if error:
        response = appMutante.response_class(
            response=json.dumps({"status":"error","data":{"error":"Error ejecutando la consulta: " + error}}),
            status=403,
            mimetype='application/json')
    else:
        response = appMutante.response_class(
            response=json.dumps({"status":"success","data":{"verificacion":verificacion}}),
            status=200,
            mimetype='application/json')
    return(response)

appMutante.run(host="0.0.0.0", port=3000, debug=True)
