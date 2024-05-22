# Sistema de Cofre Digital

Este repositório contém o código e as instruções para um sistema de cofre digital utilizando o Raspberry Pi Pico. O sistema integra um display OLED, teclado matricial, motor servo e sensores para gerenciar o acesso ao cofre e monitorar condições ambientais.

## Funcionalidades

- **Display OLED**: Fornece feedback e instruções ao usuário.
- **Teclado Matricial**: Para entrada de usuário e senha.
- **Motor Servo**: Controla o mecanismo de bloqueio.
- **Sensor de Nível de Água**: Monitora e controla os níveis de água.
- **Detecção de Obstáculos**: Garante que a porta esteja fechada corretamente antes do bloqueio.

## Componentes

| Item          | Código           | Qtd    |   Preço | Preço Total  | Fonte                                       |
| ------------- |:----------------:| :-----:| :-----: | :-----:      | -------------:|
| Raspberry Pi Pico | ? | 1 | R$ 33,90 | R$ 33,90 | https://tinyurl.com/2s45v4t9|
| Servo motor mg996 | MG996  | 1 | R$ 45,90 | R$ 45,90 | https://shorturl.at/DctgH |
| Mini bomba de água | DC-JT160 | 1 | R$ 95,00 | R$ 95,00 | https://shorturl.at/y9YZJ |
| Display OLED i2c OLED 128x32 Px | Oled | 1 | R$ 31,90 | R$ 31,90 | https://shorturl.at/yYNVK |
| Bateria externa para embarcados | ? | 1 | R$ 10,14 | R$ 10,14 | https://t.ly/dYp5f |
| Sensor umidade solo | Higrômetro | 1 | R$ 11,90 | R$ 11,90 | https://t.ly/64o8A |
| Teclado matriz 4x4 membrana | Teclado 4x4 | 1 | R$ 8,90 | R$ 8,90 | https://t.ly/hmqxS |
| Proto 170 pinos | Proto | 1 | R$ 28,00 | R$ 28,00 | https://t.ly/TIt6C |
| Sensor obstáculo | IR | 1 | R$ 10,00 | R$ 10,00 | https://t.ly/wDjsv |

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
