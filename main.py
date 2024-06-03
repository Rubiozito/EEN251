import ujson
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from teclado import MatrixKeyboard
import utime
from servo import Servo

# Configuração do LED indicador

# Nome do arquivo JSON para armazenar as senhas
file_name = "senhas.json"

# Pinos 
#pinos display OLED
i2c0_slc_pin = 7
i2c0_sda_pin = 6
i2c0 = I2C(1, scl=Pin(i2c0_slc_pin), sda=Pin(i2c0_sda_pin), freq=400000)
# Pinos do teclado matricial
rows_pins = [12, 13, 14, 15]  # Pinos GPIO para as linhas
cols_pins = [8, 9, 10, 11]  # Pinos GPIO para as colunas
debounce_time = 20  # Tempo de debounce em milissegundos
keyboard = MatrixKeyboard(rows_pins, cols_pins, debounce_time)
#Pino do sensor de obstaculo
obstacle_pin = 16
obstacle = Pin(obstacle_pin, Pin.IN)
#Pino do sensor de nivel de agua
water_pin = 18
water = Pin(water_pin, Pin.OUT)
wlevel_pin = 26
#Fora da agua 3.3V
#Dentro da agua 1.7V pra baixo
#Sensor de nivel de agua
level_analog = ADC(Pin(wlevel_pin, Pin.IN))
#pino servo motor
servo = Servo(pin=2)
ABERTO = 10
FECHADO = 100
MAX_ATTEMPTS = 4


# Função temporizada para leitura da saída analógica do sensor
def hygrometer_analog_read():
    # Lê o valor da entrada analógica do sensor como um valor positivo de 16 bits
    hygrometer_analog_value = level_analog.read_u16()
    # Converte o valor analógica na forma de um valor positivo de 16 bits para tensão (valor de um bit = 3.3/(2^16 - 1) = 3.3/65535)
    hygrometer_voltage = hygrometer_analog_value / 65535 * 3.3

    # Imprime o valor da tensão lida
    #print("Tensão lida: {:.2f} V".format(hygrometer_voltage))
    return hygrometer_voltage
    


#TODO:  Habilitar somente o display quadno houver atividade no teclado
display = SSD1306_I2C(128, 64, i2c0)

# Função para ler as senhas do arquivo JSON
def ler_senhas():
    try:
        with open(file_name, "r") as file:
            senhas = ujson.load(file)
        return senhas
    except OSError:
        return {}

# Função para cadastrar uma nova senha
def cadastrar_senha(senha, numero):
    if not senha.isdigit() or len(senha) != 4:
        display_oled_clear()
        display_oled_longtext('Senha Invalida', 0)
        utime.sleep_ms(1000)
        return False
    numero = int(numero)
    if numero < 1 or numero > 5:
        display_oled_clear()
        display_oled_longtext('Numero de Senha Invalido', 0)
        utime.sleep_ms(1000)
        return False

    senhas = ler_senhas()
    senha_key = 'senha' + str(numero)
    senhas[senha_key] = senha
    with open(file_name, "w") as file:
        ujson.dump(senhas, file)
    return True
    

# Função para apagar uma senha
def apagar_senha(nome):
    senhas = ler_senhas()
    if nome in senhas:
        del senhas[nome]
        with open(file_name, "w") as file:
            ujson.dump(senhas, file)
        return True
    else:
        return False

def verificar_senha(senha):
    senhas = ler_senhas()
    for nome, senha_cadastrada in senhas.items():
        if senha == senha_cadastrada:
            return True
    return False

def fechar_porta():
    servo.move(FECHADO)
    display_oled_clear()
    display_oled_longtext('Porta Fechada', 0)
    utime.sleep_ms(1000)
    display_oled_clear()

def abrir_porta():
    servo.move(ABERTO)
    display_oled_clear()
    display_oled_longtext('Porta Aberta', 0)
    utime.sleep_ms(1000)
    display_oled_clear()

def display_oled_text(text, row):
    # caracteres tem 8 pixels de altura que equivale a 1 linha 
    pix = row * 8 
    display.text(text, 0, pix)    

def display_oled_longtext(text, row):
    # caracteres tem 8 pixels de altura que equivale a 1 linha 
    #16 caracteres por linha    
    texts = [text[i:i+16] for i in range(0, len(text), 16)]
    for i, t in enumerate(texts):
        display_oled_text(t, row+i)
    display.show()  

def display_password(password,row):
    pix = row * 8 
    display.text(password, 48, pix)
    display.show()

def display_oled_clear():
    display.fill(0)
    #display.show()  

def apagar_tela():
    display.fill(0)
    display.show() 

def verifica_porta():
    if obstacle.value() == 1:
        return False
    return True

def verifica_agua():
    if hygrometer_analog_read() > 3:
        return False
    else:
        return True
    
def aciona_agua():
    if verifica_agua():
        water.value(0)
        display_oled_clear()
        display_oled_longtext('Agua Acionada', 0)
        utime.sleep_ms(1000)
        water.value(1)
    else:
        display_oled_clear()
        display_oled_longtext('Agua Nivel Baixo', 0)

def check_boot():
    display_oled_clear()
    water.value(1)
    display_oled_longtext('Sistema Iniciado', 0)
    utime.sleep_ms(1000)
    display_oled_clear()
    display_oled_longtext('Verificando Porta', 0)
    utime.sleep_ms(1000)
    porta = verifica_porta()
    while not porta:
            abrir_porta()
            display_oled_clear()
            display_oled_longtext('Fechar porta', 0)
            utime.sleep_ms(2000)
            porta = verifica_porta()
    display_oled_clear()
    utime.sleep_ms(1500)
    fechar_porta()
    utime.sleep_ms(1000)
    display_oled_clear()
    display_oled_longtext('Verificando Agua', 0)
    nivel_agua = verifica_agua()
    if nivel_agua:
        display_oled_clear()
        display_oled_longtext('Agua Nivel Baixo', 0)
    else:
        display_oled_clear()
        display_oled_longtext('Agua Nivel Normal', 0)
    utime.sleep_ms(1000)
    display_oled_clear()
    display_oled_longtext('Sistema Pronto', 0)
    utime.sleep_ms(1000)
    apagar_tela()

def keybord_get_password():
    password = ''
    while len(password) < 4:
        key_chars = keyboard.get_pressed_keys()  # Obtém a lista de teclas pressionadas
        display_oled_longtext('Digite sua Senha ', 0)  
        for key in key_chars:
            if key == 'A' or key == 'B' or key == 'C' or key == '*' or key == '#':
                continue
            if key == 'D':
                password = password[:-1]
                display_oled_clear()
                display_oled_longtext('Digite sua Senha ', 0)  
            else:
                password += key
            display_password(password, 2)
        utime.sleep_ms(100)
    
    utime.sleep_ms(3000)
    return password

def keybord_get_number():
    number =''
    while len(number) < 1:
        key_chars = keyboard.get_pressed_keys()  # Obtém a lista de teclas pressionadas
        display_oled_longtext('Digite um numero de 1 a 5 ', 0)  
        for key in key_chars:
            if key == 'A' or key == 'B' or key == 'C' or key == 'D' or key == '*' or key == '#':
                continue
            else:
                number += key
            display_password(number, 2)
        utime.sleep_ms(100)

    utime.sleep_ms(3000)
    return number

# Testando as funções
#def teste():
    # Lendo as senhas
    # print("Senhas existentes:", ler_senhas())
    # text = ''
    # apagar_tela()
    # servo.move(FECHADO)
    # display_oled_clear()
    # display_oled_longtext('Sistema Iniciado', 0)
    # aciona_agua()
    # utime.sleep_ms(1000)
    # check_boot()
    # utime.sleep_ms(1000)
    # servo.move(100)  # turns the servo to 90°.
    # utime.sleep_ms(1000)
    #servo.move(70)  # turns the servo to 90°.

    # while True:
    # # #     servo.move(45)  # turns the servo to 0°.
    # #     # utime.sleep_ms(1000)
    # #     # servo.move(0)  # turns the servo to 90°.
    #     utime.sleep_ms(1000)
    #     nivel_agua = hygrometer_analog_read()
    #     print("Tensão lida: {:.2f} V".format(nivel_agua))
    #     aciona_agua()
        # utime.sleep_ms(5000)

        # aciona_agua()
        # utime.sleep_ms(10000)
        # porta = verifica_porta()
        # if porta == 0:
        #     display_oled_clear()
        #     display_oled_longtext('Porta Fechada', 0)
        # else:
        #     display_oled_clear()
        #     display_oled_longtext('Porta Aberta', 0)

        # key_chars = keyboard.get_pressed_keys()  # Obtém a lista de teclas pressionadas
        # display_oled_longtext('Digite sua Senha ', 0)
        # Processa cada tecla pressionada
        # for key in key_chars:
        #     print("Tecla pressionada: {}".format(key))
        #     text += key
        #     display_password(text, 2)
        #     if len(text) == 4:
        #         text = ''
        #         utime.sleep_ms(1000)
        #         utime.sleep_ms(3000)
        #         display_oled_clear()
            # if key == '1':
            #     print("Key pressed: 1")
            # elif key == '2':
            #     print("Key pressed: 2")
            # elif key == '3':
            #     print("Key pressed: 3")
            # elif key == 'A':
            #     print("Key pressed: A")
            # elif key == '4':
            #     print("Key pressed: 4")
            # elif key == '5':
            #     print("Key pressed: 5")
            # elif key == '6':
            #     print("Key pressed: 6")
            # elif key == 'B':
            #     print("Key pressed: B")
            # elif key == '7':
            #     print("Key pressed: 7")
            # elif key == '8':
            #     print("Key pressed: 8")
            # elif key == '9':
            #     print("Key pressed: 9")
            # elif key == 'C':
            #     print("Key pressed: C")
            # elif key == '*':
            #     print("Key pressed: *")
            # elif key == '0':
            #     print("Key pressed: 0")
            # elif key == '#':
            #     print("Key pressed: #")
            # elif key == 'D':
            #     print("Key pressed: D")
            # else:
            #     print("Unknown key")

        # Pausa para debounce e redução do uso da CPU
        #utime.sleep_ms(100)


# Executando o teste
#teste()
def main():
    while True:
        while verifica_porta():   
            key_chars = keyboard.get_pressed_keys()
            for key in key_chars:
                if key == 'B' or key == 'C' or key == '*' or key == '#':
                    continue
                if key == 'A':
                    aciona_agua()
                if key == 'D':
                    attempts = 0
                    while attempts < MAX_ATTEMPTS:
                        password = keybord_get_password()
                        if verificar_senha(password):
                            display_oled_clear()
                            display_oled_longtext('Senha Correta', 0)
                            utime.sleep_ms(1000)
                            attempts = 0
                            display_oled_clear()
                            abrir_porta()
                            break
                        else:
                            display_oled_clear()
                            display_oled_longtext('Senha Incorreta', 0)
                            aciona_agua()
                            utime.sleep_ms(1000)
                            display_oled_clear()
                            attempts += 1
                    if attempts == MAX_ATTEMPTS:
                        display_oled_clear()
                        display_oled_longtext('Tentativas Esgotadas', 0)
                        utime.sleep_ms(1000)
                        display_oled_clear()
                        display_oled_longtext('Espere 1 minuto para tentar novamente', 0)
                        utime.sleep_ms(60000)

        while not verifica_porta():
            key_chars = keyboard.get_pressed_keys()
            for key in key_chars:
                if key == 'A' or key == 'B' or key == 'D' or key == '*' or key == '#':
                    continue
                if key == 'C':
                    new_password = keybord_get_password()
                    display_oled_clear()
                    number = keybord_get_number()
                    if cadastrar_senha(new_password, number):
                        display_oled_clear()
                        display_oled_longtext('Senha Cadastrada', 0)
                    else:
                        display_oled_clear()
                        display_oled_longtext('Senha Invalida', 0)

            if verifica_porta():
                utime.sleep_ms(2000)
                if verifica_porta():
                    display_oled_clear()
                    display_oled_longtext('Fechando a porta', 0)
                    fechar_porta()
                    utime.sleep_ms(1000)
                    display_oled_clear()
check_boot()
main()


