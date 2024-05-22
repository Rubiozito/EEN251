# Sistema de Cofre Digital Seguro

Este repositório contém o código e as instruções para um sistema de cofre digital seguro utilizando o Raspberry Pi Pico. O sistema integra um display OLED, teclado matricial, motor servo e sensores para gerenciar o acesso seguro e monitorar condições ambientais.

## Funcionalidades

- **Display OLED**: Fornece feedback e instruções ao usuário.
- **Teclado Matricial**: Para entrada de usuário e senha.
- **Motor Servo**: Controla o mecanismo de bloqueio.
- **Sensor de Nível de Água**: Monitora e controla os níveis de água.
- **Detecção de Obstáculos**: Garante que a porta esteja fechada corretamente antes do bloqueio.

## Componentes

- Raspberry Pi Pico
- Display OLED (128x64)
- Teclado Matricial
- Motor Servo
- Sensor de Nível de Água
- Sensor de Obstáculos

## Configuração

1. **Conectar Componentes**: Siga a configuração de pinos especificada no código.
2. **Carregar Código**: Use MicroPython para carregar o script no seu Raspberry Pi Pico.
3. **Arquivo JSON**: Garanta que o arquivo `senhas.json` exista para armazenamento de senhas.

## Uso

- **Iniciar Sistema**: Na inicialização, o sistema verifica a porta e os níveis de água.
- **Entrada de Senha**: Insira uma senha de 4 dígitos para abrir o cofre.
- **Adicionar Nova Senha**: Insira uma nova senha e atribua um número de slot.
- **Monitoramento de Sensores**: Monitora e controla continuamente o nível de água.

## Visão Geral do Código

- **Funções de Display**: Gerenciam a exibição de texto na tela OLED.
- **Gerenciamento de Senhas**: Lida com leitura, escrita e verificação de senhas.
- **Controle do Servo**: Abre e fecha o mecanismo de bloqueio.
- **Funções de Sensor**: Leem e agem com base nos dados dos sensores.

## Licença

Este projeto é de código aberto e está disponível sob a Licença MIT.

Para mais detalhes, consulte o [repositório do projeto](https://github.com/Rubiozito/EEN251).
