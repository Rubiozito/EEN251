import ujson
import utime
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from teclado import MatrixKeyboard


file_name = "senhas.json"

# Pinos display OLED
i2c0_slc_pin = 7
i2c0_sda_pin = 6
i2c0 = I2C(1, scl=Pin(i2c0_slc_pin), sda=Pin(i2c0_sda_pin), freq=400000)
rows_pins = [12, 13, 14, 15]  # Pinos GPIO para as linhas
cols_pins = [8, 9, 10, 11]  # Pinos GPIO para as colunas
debounce_time = 20  # Tempo de debounce em milissegundos
keyboard = MatrixKeyboard(rows_pins, cols_pins, debounce_time)

#TODO:  Habilitar somente o display quadno houver atividade no teclado
display = SSD1306_I2C(128, 64, i2c0)

#
def display_oled_text(text, row):
    # caracteres tem 8 pixels de altura que equivale a 1 linha 
    pix = row * 8 
    display.text(text, 0, pix)    

# Função para exibir um texto longo no display OLED
def display_oled_longtext(text, row):
    # caracteres tem 8 pixels de altura que equivale a 1 linha 
    #16 caracteres por linha    
    texts = [text[i:i+16] for i in range(0, len(text), 16)]
    for i, t in enumerate(texts):
        display_oled_text(t, row+i)
    display.show()  

# Função para exibir uma senha no display OLED
def display_password(password,row):
    pix = row * 8 
    display.text(password, 48, pix)
    display.show()

# Função para exibir um texto no display OLED
def display_oled_clear():
    display.fill(0)
    display.show()  

# Funcao para pegar 4 digitos	
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
            else:
                text += key
            display_password(text, 2)
        utime.sleep_ms(100)
    
    utime.sleep_ms(3000)
    return password

# Função para ler as senhas do arquivo
def ler_senhas():
    try:
        with open(file_name, "r") as file:
            senhas = ujson.load(file)
        return senhas["senhas"]
    except OSError:
        return {}
    
# Função para ler o arquivo
def ler_arquivo():
    try:
        with open(file_name, "r") as file:
            arquivo = ujson.load(file)
        return arquivo
    except OSError:
        return {}

# Função para verificar se o cofre está aberto 
def verificar_aberto():
    try:
        with open(file_name, "r") as file:
            senhas = ujson.load(file)
        return senhas["cofre_aberto"]
    except OSError:
        return {}

# Função para verificar se uma senha está correta
def verificar_senha(senha):
    senhas = ler_senhas()
    if senha in senhas:
        return True
    else:
        return False

# Função para abrir o cofre inserindo a senha mestra
def abrir_cofre():
    #senha = input("Digite a senha mestra para abrir o cofre: ")
    display_oled_longtext('Digite a senha para abrir o cofre:', 0)
    senha = keybord_get_password()

    if senha == "1234" or verificar_senha(senha):  
        senhas = ler_arquivo()
        senhas["cofre_aberto"] = True
        with open(file_name, "w") as file:
            ujson.dump(senhas, file)
    else:
        print("Senha mestra incorreta.")
        
        display_oled_clear()
        display_oled_longtext('Senha mestra incorreta', 0)
        utime.sleep_ms(3000)
        display_oled_clear()

# Função para fechar o cofre
def fechar_cofre():
    #senha = input("Cadastre a senha para fechar o cofre: ") 
    display_oled_longtext('Digite a senha para fechar o cofre:', 0)
    senha = keybord_get_password()
    
    senhas = ler_arquivo()
    senhas["cofre_aberto"] = False
    senhas["senhas"] = senha
    with open(file_name, "w") as file:
        ujson.dump(senhas, file)

    display_oled_clear()
    display_oled_longtext('Cofre fechado com sucesso', 0)
    utime.sleep_ms(3000)
    display_oled_clear()




# Exemplo de uso das funções
def main():
    while True:
        if verificar_aberto():
            fechar_cofre()
        else:
            abrir_cofre()




if __name__ == "__main__":
    main()
