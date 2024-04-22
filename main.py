import ujson
from machine import Pin, I2C
from utime import sleep
from ssd1306 import SSD1306_I2C

# Configuração do LED indicador

# Nome do arquivo JSON para armazenar as senhas
file_name = "senhas.json"

# Pinos display OLED
i2c0_slc_pin = 9
i2c0_sda_pin = 8
i2c0 = I2C(0, scl=Pin(i2c0_slc_pin), sda=Pin(i2c0_sda_pin), freq=400000)

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

def display_oled(text):
    #16 caracteres por linha

    display.fill(0)
    display.text(text, 0, 32)
    display.show()

# Testando as funções
def teste():
    # Lendo as senhas
    print("Senhas existentes:", ler_senhas())

    # Cadastrando uma nova senha
    # cadastrar_senha("minha_senha", "usuario2")
    # print("Senha cadastrada")

    # Lendo as senhas após o cadastro
    print("Senhas existentes:", ler_senhas())

    # Apagando uma senha
    # apagar_senha("usuario1")
    # print("Senha apagada")

    # Lendo as senhas após a exclusão
    # print("Senhas existentes:", ler_senhas())
    # display.text("Hello World!", 16, 54)
    # display.show()
    # display.fill(0)
    # display.text("OI", 64, 54)
    # display.show()
    # text = "senha cadastrada"
    # display_oled(text)
    display.fill_rect(0, 0, 32, 32, 1)
    display.show()


# Executando o teste
teste()
