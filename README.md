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

* 4.1 Matrizes de Translação (T, T_) 
 
A matriz de translação (T) é responsável por mover a imagem para uma determinada posição. Ela é definida por uma matriz de 3x3, em que os elementos da diagonal principal são iguais a 1, os elementos da última coluna são as coordenadas x e y da translação e os demais elementos são iguais a 0. No exemplo abaixo, a imagem é transladada em metade da largura pixels para a esquerda e metade da altura para cima.
        
        T = np.array([[1, 0, image.shape[0]/2], [0, 1, image.shape[1]/2], [0, 0, 1]]) 

$$
T = 
\begin{bmatrix}
1 & 0 & 160 \\
0 & 1 & 120 \\
0 & 0 & 1
\end{bmatrix}
$$

* 4.2 Matriz de Rotação (R)

A matriz de rotação (R) é responsável por rotacionar a imagem em torno do ponto (0,0). Ela é definida por uma matriz de 3x3, em que os elementos da diagonal principal são iguais a cos(θ) e os elementos da diagonal secundária são iguais a -sin(θ) e sin(θ), onde θ é o ângulo de rotação em radianos. 

        R = np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0, 0, 1]])
        
$$
R = 
\begin{bmatrix}
    \cos(\theta) & -\sin(\theta) & 0 \\
    \sin(\theta) & \cos(\theta) & 0 \\
    0 & 0 & 1
\end{bmatrix}
$$


* 4.3 Matriz de Expansão (S)

A matriz de expansão (S) é responsável por aumentar ou diminuir a imagem. Ela é definida por uma matriz de 3x3, em que os elementos da diagonal principal são iguais a 1 e os elementos da última coluna são os fatores de expansão. No exemplo abaixo, a imagem é expandida em 2 vezes:

        S = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]])

$$
S = 
\begin{bmatrix}
2 & 0 & 0 \\
0 & 2 & 0 \\
0 & 0 & 1
\end{bmatrix}
$$


* 4.4 Matriz de Transformação Completa (E)

A matriz de transformação completa (E) é obtida pela multiplicação das matrizes de translação e rotação. Ela é responsável por realizar as três transformações em sequência e, assim, obter a imagem rotacionada no ponto desejado.

        T = np.array([[1, 0, image.shape[0]/2], [0, 1, image.shape[1]/2], [0, 0, 1]])
        R = np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0, 0, 1]])
        T_ = np.array([[1, 0, -image.shape[0]/2], [0, 1, -image.shape[1]/2], [0, 0, 1]])

        # matriz de rotação
        E = T @ R @ T_

        # matriz de rotação e expansão
        E = T @ R @ S @ T_


5. Para evitar que sejam "perdidos" pixels durante a transformação, ou seja, que haja pontos pretos na imagem final, não realizamos a multiplicação matricial com os pixels de origem para encontrar os pixels de destino. Mas sim, multiplicamos a matriz de destino pelo inversa da matriz de transformação, para encontrar os pixels na matriz de origem;

        X = np.linalg.inv(E) @ Xd


$$
X_o = E^{-1} X_d
$$


6. Filtra as matrizes de destino e origem, delimitando no espaço da janela e transformando os valores em inteiro;

        X = X.astype(int) # posições tem que ser inteiros
        Xd = Xd.astype(int)
        filtro = (X[0,:] >=0) & (X[0,:] < image_.shape[0]) & (X[1,:] >=0) & (X[1,:] < image_.shape[1])
        Xd = Xd[:,filtro]
        X = X[:,filtro]

        image_[Xd[0,:], Xd[1,:], :] = image[X[0,:], X[1,:], :]

## b. Velocidade e direção da rotação

O controle da rotação funciona a partir da mudança no incremento do ângulo a cada iteração do loop. No estado padrão, o ângulo começa no 0 e vai aumentando de 1 em 1 grau. 

* Para rotacionar no sentido horário, o incremento deve ser positivo, por isso o incremento é colocado em módulo;
* Para rodar no sentido anti-horário, o incremento deve ser negativo, por isso multiplica-se o seu módulo por -1;
* Para aumentar a velocidade da rotação, aumenta-se em 25% quantos graus serão incrementados por iteração;
* Para diminuir a velocidade da rotação, diminui 25% de quantos graus serão incrementados por iteração;

        if key == ord('a'): # gira para a esquerda
                aum = abs(aum)
        elif key == ord('d'): # gira para a direita
                aum = abs(aum) * -1
        elif key == ord('w'): # aumenta a velocidade
                aum *= 1.25
        elif key == ord('s'): # diminui a velocidade
                aum *= 0.75

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
