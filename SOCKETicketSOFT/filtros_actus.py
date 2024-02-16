import copy

def filtros_actus( dispensadores, campo, valor_positivo ):
    dispensadores_temp = copy.deepcopy( dispensadores )
    dispensadores_salida = dict()
    for dispensador in dispensadores_temp:
        if (dispensador[campo] == valor_positivo):
            clave_dict = "{}-{}".format( dispensador['codigo_estacion'], dispensador['posicion_dispensador'] )
            dispensadores_salida[ clave_dict ] = dispensador
    return dispensadores_salida
    
def existe_dispensador_codigo(dispensadores, codigo_estacion):
    if( dispensadores=={} ):
        return False
    if codigo_estacion not in dispensadores:
        return False
    return True

