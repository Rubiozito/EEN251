import ujson

file_name = "senhas.json"

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
    senha = input("Digite a senha mestra para abrir o cofre: ")
    if senha == "1234" or verificar_senha(senha):  # Exemplo de senha mestra (você pode modificar conforme necessário)
        senhas = ler_arquivo()
        senhas["cofre_aberto"] = True
        with open(file_name, "w") as file:
            ujson.dump(senhas, file)
    else:
        print("Senha mestra incorreta.")

# Função para fechar o cofre
def fechar_cofre():
    senha = input("Cadastre a senha para fechar o cofre: ")  # Exemplo de senha mestra (você pode modificar conforme necessário)
    senhas = ler_arquivo()
    senhas["cofre_aberto"] = False
    senhas["senhas"] = senha
    with open(file_name, "w") as file:
        ujson.dump(senhas, file)




# Exemplo de uso das funções
def main():
    while True:
        if verificar_aberto():
            print("O cofre está aberto.")
            fechar_cofre()
            print("O cofre está fechado.") 
        else:
            print("O cofre está fechado.")
            abrir_cofre()
            print("O cofre está aberto.")



if __name__ == "__main__":
    main()
