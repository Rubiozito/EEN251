import ujson
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from teclado import MatrixKeyboard
import utime

# Configuração do LED indicador

# Nome do arquivo JSON para armazenar as senhas
file_name = "senhas.json"

# Pinos 
i2c0_slc_pin = 7
i2c0_sda_pin = 6
i2c0 = I2C(1, scl=Pin(i2c0_slc_pin), sda=Pin(i2c0_sda_pin), freq=400000)
rows_pins = [12, 13, 14, 15]  # Pinos GPIO para as linhas
cols_pins = [8, 9, 10, 11]  # Pinos GPIO para as colunas
debounce_time = 20  # Tempo de debounce em milissegundos
keyboard = MatrixKeyboard(rows_pins, cols_pins, debounce_time)
obstacle_pin = 16
obstacle = Pin(obstacle_pin, Pin.IN)
water_pin = 18
water = Pin(water_pin, Pin.OUT)
water.value(0)
wlevel_pin = 26
#Fora da agua 3.3V
#Dentro da agua 1.7V pra baixo
level_analog = ADC(Pin(wlevel_pin, Pin.IN))


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
def cadastrar_senha(senha, nome):
    if not senha.isdigit() or len(senha) != 4:
        print("A senha deve ser composta apenas por números e ter 4 dígitos.")
        return
    
    senhas = ler_senhas()
    senhas[nome] = senha
    with open(file_name, "w") as file:
        ujson.dump(senhas, file)
    print("Senha cadastrada com sucesso.")

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
    return obstacle.value()

def verifica_agua():
    pass

def aciona_agua():
    water.value(1)
    display_oled_clear()
    display_oled_longtext('Agua Acionada', 0)
    utime.sleep_ms(10000)
    water.value(0)
# Testando as funções
def teste():
    # Lendo as senhas
    print("Senhas existentes:", ler_senhas())
    text = ''
    apagar_tela()
    utime.sleep_ms(1000)
    while True:
        nivel_agua = hygrometer_analog_read()
        print("Tensão lida: {:.2f} V".format(nivel_agua))
        utime.sleep_ms(5000)

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
        utime.sleep_ms(100)


# Executando o teste
teste()
