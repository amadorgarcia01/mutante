import mysql.connector
from mysql.connector import errorcode


def conectar_bd():
  """Crea la conexión a la BBDD

      Se debe configurar la lista conexion con los valores de la BBDd a conectar

      Parámetros:
        ninguno

      Excepciones:
        Controladas, se especifica el Nro del error cuando no son del tipo
        usuario/clave o que no existe la BBDD
      
      """
  

  conexion = {
    'database':'mutante', 
    'user':'mutante', 
    'passwd':'meli',
    'host': '35.175.141.199',
    'port':'3306',
    'auth_plugin':'mysql_native_password'
    }

  try:
    cnx = mysql.connector.connect(**conexion)

  except mysql.connector.Error as err:
    cnx = None
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      mensaje_error = "Error en el usuario y/o clave para conexión a la Base de Datos"
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      mensaje_error = "Base de datos no existe"
    else:
      #mensaje_error = "Error conectándose a la Base de Datos: " + str(err.errno)
      mensaje_error = str(err)
  else: 
    mensaje_error = ""

  return cnx, mensaje_error


def insertar_adn(mutante, adn):
  """Inserta un ADN en la BBDD

    Se controla que no rse inserten ADN repetidos en la BBDD

    Parámetros:
      mutante: boolean que indica si el ADN es mutante o no
      adn: cadena de caracteres del ADN que se debe insertar en la BBDD

    Excepciones:
      Se controla el error de ADN repetidos
    
    """

  cnx, error = conectar_bd()
  
  if error == "":
    cursor = cnx.cursor()
    nuevo_mutante = ("INSERT INTO ADN "
                  "(mutante, adn, fecha_registro) "
                  "VALUES (%(mutante)s, %(adn)s, NOW())")

    datos_mutante = {
      'mutante': mutante,
      'adn': adn,
    }
    try:
      cursor.execute(nuevo_mutante, datos_mutante)
    except mysql.connector.Error as error_insert:
      if error_insert.errno != errorcode.ER_DUP_ENTRY:
        error = "Se produjo un error guardando el registro en la BBDD"
        cnx.rollback()
      else:
        cnx.commit()
    else:
      cnx.commit()
    finally:
      cursor.close()
      cnx.close()

    return True, error
  else:
    return False, error


def consultar_adn():
  """Consultar la relación entre mutantes y no mutantes

    Parámetros:
       ninguno

    Excepciones:
      Se controla el error de en la ejecución del select
    
    """

  cnx, error = conectar_bd()

  verificaciones = ""
  c_mutante = 0
  c_no_mutante = 0
  ratio = 0

  if error == "":
    cursor = cnx.cursor()

    consulta_mutante = ("SELECT SUM(MUTANTE), COUNT(*) - SUM(MUTANTE), CASE WHEN SUM(MUTANTE) = 0 THEN 0 WHEN COUNT(*) = SUM(MUTANTE) THEN 1 ELSE SUM(MUTANTE) / COUNT(*) END FROM ADN")

    try:
      cursor.execute(consulta_mutante)
    except mysql.connector.Error as err:
        error = str(err.errno)
    else:
      for (c_mutante, c_no_mutante, ratio) in cursor:
        verificaciones = '{“count_mutant_dna”:' + str(c_mutante) + ', “count_human_dna”:' + str(c_no_mutante) + ', “ratio”:' + str(ratio) + '}'
    finally:
      cursor.close()
      cnx.close()

    return error, verificaciones
  else:
    return error, verificaciones
