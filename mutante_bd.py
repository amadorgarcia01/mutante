from persistencia import insertar_adn, consultar_adn
import json

# Variables de configuración
str_validar = "ATCG"
n_repite = 4
n_cant_letras_adn = 6
opc_respuesta = ['El ADN NO pertenece a un mutante', 'Error en el ADN suministrado, posee valores no validos', 'El ADN pertenece a un mutante']

def validar_adn(base_adn, adn):
    """Se valida si se repite N (nrepite) veces la misma letra

    Parámetros:
      base_adn: string que contiene las letras que son permitidas dentro de un ADN
      adn: cadena de caracteres del ADN que se debe validar

    Excepciones:
      Ninguna
    
    """

    for x in list(base_adn):
        res = [s for s in adn if (x*n_repite) in s]
        if res != []:
            return 2
    return 0

# Se valida si el adn es de mutante o no
def mutante(data):
    """Se valida si se un ADN es mutante o no y se insertan en la BBDD en caso de que
    no existe

    Parámetros:
      data: JSON que contiene la cadena de ADN, debe ser del tipo:
      {"dna":["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]}

    Excepciones:
      No se procesan los ADN que no tengan los valores de letras permitidos en str_validar
    
    """

    data = json.dumps(data)
    data = json.loads(data)
    data_list = list(data['dna'])

    codigo_ejecucion = 0
    arreglo = []
    arreglo_h = []
    arreglo_d = []
    arreglo_v = []
    arreglo_temp = []

    inicio = n_cant_letras_adn - 1
    final = 0

    # Se validan las letras permitidas y se cargan arreglo, arreglo_h, arreglo_temp --> arreglo_d
    for x in data_list:
        for y in x:
            if str_validar.find(y) == -1:
                codigo_ejecucion = 1
                break
        if codigo_ejecucion == 0:
            arreglo_h.append(x)
            arreglo.append(list(x))
            arreglo_temp.append((' '*inicio) + "".join(x) + (' '*final))
            inicio = inicio - 1
            final = final + 1
        else:
            break

    if codigo_ejecucion == 1:
        resp = opc_respuesta[codigo_ejecucion]
        return False, resp
    else:
        # Se valida la matriz horizontalmente
        codigo_ejecucion = validar_adn(str_validar, arreglo_h)
        if codigo_ejecucion == 2:
            insertar_adn(1, " ".join(data['dna']))
            resp = opc_respuesta[codigo_ejecucion]
            return True, resp
        else:
            for x in list(zip(*arreglo_temp)):
                arreglo_d.append("".join(x).replace(" ", ""))
            # Se valida la matriz diagonalmente
            codigo_ejecucion = validar_adn(str_validar, arreglo_d)
            if codigo_ejecucion == 2:
                insertar_adn(1, " ".join(data['dna']))
                resp = opc_respuesta[codigo_ejecucion]
                return True, resp
            else:
                for x in list(zip(*arreglo)):
                    arreglo_v.append("".join(x))            
                # Se valida la matriz verticalmente
                codigo_ejecucion = validar_adn(str_validar, arreglo_v)
                if codigo_ejecucion == 2:
                    insertar_adn(1, " ".join(data['dna']))
                    resp = opc_respuesta[codigo_ejecucion]
                    return True, resp

    if codigo_ejecucion == 0:
        insertar_adn(0, " ".join(data['dna']))
        resp = opc_respuesta[codigo_ejecucion]
        return False, resp


def consulta():
    """Se consulta la relación y frecuena de mutantes y no mutantes

    Parámetros:
      Ninguno

    Excepciones:
      Ninguna

      """

    error, verificacion = consultar_adn()
    return error, verificacion
