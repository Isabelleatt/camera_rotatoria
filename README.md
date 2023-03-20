# camera_rotatoria
APS 3 - Álgebra Linear e Teoria da Informação - 2021.1

## Integrantes do grupo
* [Isabelle da Silva Santos](https://github.com/isabelleatt)
* [Livia Tanaka](https://github.com/liviatanaka)

## Introdução

Este projeto consiste em um conjunto de funções em Python para a realização de transformações em imagens, tais como rotação e expansão. As transformações são realizadas através de operações matriciais, e o usuário pode definir o ângulo de rotação, a escala de expansão e o tipo de transformação a ser aplicado. As funções também incluem a delimitação dos valores de entrada para evitar erros e comportamentos inesperados.

# Transformação da imagem

O projeto apresenta as seguintes possibilidades de transformação na imagem:

## a. Rotação da imagem

A rotação da imagem é realizada através da função `gira_imagem(image, ang)` que recebe como argumentos a matriz de uma imagem que será rotacionada e o ângulo (em graus) de sua rotação.
A função funciona da seguinte maneira:

1. Cria uma matriz de zeros com o mesmo formato da matriz da imagem;

        image_ = np.zeros_like(image)

2. Tranforma o ângulo de grus para radianos;

        rad = np.radians(ang)

3. Cria uma matriz com todos as coordenadas possíveis dos pixels da imagem. E adiciona uma linha de uns para posteriormente realizar a transição;

        Xd = criar_indices(0, image.shape[0], 0, image.shape[1])
        Xd = np.vstack ( (Xd, np.ones( Xd.shape[1]) ) )

4. Nesse processo, é necessário realizar três transformações para obter a rotação necessária: transição, rotação e transição de volta para a posição original. Para que a imagem rotacione em torno de seu centro, são realizadas duas transições, uma de ida e outra de volta. Antes de multiplicar com a matriz de imagem, as matrizes de transformação são multiplicadas entre si por meio de multiplicação matricial.

* 4.1 Matriz de Translação (T) 
 
A matriz de translação (T) é responsável por mover a imagem para uma determinada posição. Ela é definida por uma matriz de 3x3, em que os elementos da diagonal principal são iguais a 1, os elementos da última coluna são as coordenadas x e y da translação e os demais elementos são iguais a 0. No exemplo abaixo, a imagem é transladada em 50 pixels para a direita e 100 pixels para baixo:
        
        T = np.array([[1, 0, 50], [0, 1, 100], [0, 0, 1]])

* 4.2 Matriz de Rotação (R)

A matriz de rotação (R) é responsável por rotacionar a imagem em torno de um ponto. Ela é definida por uma matriz de 3x3, em que os elementos da diagonal principal são iguais a cos(θ) e os elementos da diagonal secundária são iguais a -sin(θ), onde θ é o ângulo de rotação em radianos. No exemplo abaixo, a imagem é rotacionada em 45 graus:

        R = np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0, 0, 1]])
        
* 4.3 Matriz de Expansão (S)

A matriz de expansão (S) é responsável por aumentar ou diminuir a imagem. Ela é definida por uma matriz de 3x3, em que os elementos da diagonal principal são iguais a 1 e os elementos da última coluna são os fatores de expansão. No exemplo abaixo, a imagem é expandida em 2 vezes:

        S = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]])

* 4.4 Matriz de Transformação Completa (E)

A matriz de transformação completa (E) é obtida pela multiplicação das matrizes de translação e rotação. Ela é responsável por realizar as três transformações em sequência e, assim, obter a imagem rotacionada no ponto desejado. No exemplo abaixo, a imagem é rotacionada em 45 graus em torno do centro:

        T = np.array([[1, 0, image.shape[0]/2], [0, 1, image.shape[1]/2], [0, 0, 1]])
        R = np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0, 0, 1]])
        T_ = np.array([[1, 0, -image.shape[0]/2], [0, 1, -image.shape[1]/2], [0, 0, 1]])

        E = T @ R @ T_

5. Para evitar que sejam "perdidos" pixels durante a transformação, ou seja, que haja pontos pretos na imagem final, não realizamos a multiplicação matricial com os pixels de origem para encontrar os pixels de destino. Mas sim, multiplicamos a matriz de destino pelo inversa da matriz de transformação, para encontrar os pixels na matriz de origem;

        X = np.linalg.inv(E) @ Xd

6. Filtra as matrizes de destino e origem, delimitando no espaço da janela e transformando os valores em inteiro;

        X = X.astype(int) # posições tem que ser inteiros
        Xd = Xd.astype(int)
        filtro = (X[0,:] >=0) & (X[0,:] < image_.shape[0]) & (X[1,:] >=0) & (X[1,:] < image_.shape[1])
        Xd = Xd[:,filtro]
        X = X[:,filtro]

        image_[Xd[0,:], Xd[1,:], :] = image[X[0,:], X[1,:], :]



# Instruções de uso
## Clonando um Repositório

Primeiramente, navegue para o diretório aonde você gostaria de clonar o repositório usando comandos como:
*  cd: para mudar de diretório 
* cd ../ para voltar um nível do diretório <br>

Próximo, clone o repositório remoto e crie uma copia local em sua máquina usando o comando: <br>
**git clone https://github.com/Isabelleatt/camera_rotatoria**

Agora, você poderá acessar os arquivos recém baixados com os comandos *cd* e *ls*

## Instalando o necessário

É necessário realizar algumas breves instalações para utilizar o código, isso pode ser realizada de forma simples usando o comando: <br>
**pip install opencv-python**

## Rodando a demo

Para rodar a demo é apenas necessário executar o arquivo demo.py, podendo o mesmo ser realizado pela ferramenta no topo superior direito do Visual Studio Code ou usando o seguinte comando: <br>
**python demo.py**

## Comandos de transformação

| Tecla | Comando |
| --- | --- | 
| q | encerra o programa |
| p | rotação em torno do eixo central |
| r | possibilita o controle do sentido e da velocidade da rotação a partir das teclas a, w, s, d |
| a | rotação para a esquerda |
| d | rotação para a direita |
| w | aumenta a velocidade da rotação |
| s | diminui a velocidade da rotação |
| e | possibilita o zoom na imagem a partir das teclas i, o |
| i | zoom in |
| o | zoom out |
