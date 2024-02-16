########### conn ###########
import os, copy, time
from datetime import datetime
from conn import get_dispensadores
from filtros_actus import filtros_actus, existe_dispensador_codigo
########### asyncio ###########
import asyncio
import random



class MyServer:
    def __init__(self, host, port):
        self.dict_dispensadores_actu_products = dict()
        self.host=host
        self.port=port

    async def handle_client(self, reader, writer):
        direccion_destino = ""
        try:
            while True:
                #Notificador
                if( direccion_destino != ""):
                    await self.send_notifications(writer, direccion_destino)
                
                try: #Lector
                    data = await asyncio.wait_for(reader.readline(), timeout=2.0)
                    message = data.decode().strip()
                    print( direccion_destino+": "+message )
                    if message == 'A':
                        direccion_destino = "1234-1"
                        print(direccion_destino)
                        #break
                    else:
                        print(f"Received {message} from {writer.get_extra_info('peername')}")
                except asyncio.TimeoutError:
                    print("¡Tiempo de espera excedido al leer datos del socket!")
                    #return None  # O maneja la excepción de otra manera
        except asyncio.CancelledError:
            print("Connection with client cancelled")
        finally:
            writer.close()

    async def send_notifications(self, writer, direccion_destino):
        try:
            while True:
                await asyncio.sleep(1)
                if (direccion_destino == ""):
                    continue
                mensaje = ""
                print("direccion_destino ", direccion_destino )
                if ( existe_dispensador_codigo(self.dict_dispensadores_actu_products, direccion_destino) ):
                    mensaje = "{actu_products:1}"+"\n"
                if(mensaje!=""):
                    writer.write(mensaje.encode())
                    await writer.drain()
                    print(mensaje)
                
        except asyncio.CancelledError:
            print("Sending 'ok' cancelled")

    async def ejecutar_consultas(self):
        while True:
            hora_actual = datetime.now()
            print("Hora actual:", hora_actual.strftime("%H:%M:%S"))
            dispensadores = get_dispensadores()
            self.dict_dispensadores_actu_products = filtros_actus(dispensadores, 'actu_products', 1 )
            await asyncio.sleep(2)

    async def main(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        # Ejecutar la función ejecutar_consultas() cada 2 segundos
        consulta_task = asyncio.create_task(self.ejecutar_consultas())

        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    server_instance = MyServer('127.0.0.1', 9999)
    asyncio.run(server_instance.main())

