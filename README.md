# camera_rotatoria
APS 3 - Álgebra Linear e Teoria da Informação - 2021.1

## Integrantes do grupo
* [Isabelle da Silva Santos](https://github.com/isabelleatt)
* [Livia Tanaka](https://github.com/liviatanaka)

## Introdução

Esse projeto consiste na aplicação de efeitos visuais na câmera do computador. Tais efeitos são resultados de transformações na imagem realizadas apartir de multiplicações matriciais.(???)

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

4. Como é necessário realizar três transformações seguidas para obter a rotação necessária, é realizada a multiplicação matricial entre as matrizes de transformação antes de realizar a multiplicação com a matriz de imagem.
    As três transformações são transição, rotação e transição para voltar a posição original. Tendo em vista que a matriz de rotação (R) é em torno do ponto (0,0), para que a imagem rotacione em torno de seu centro, realiza-se duas transições, uma de ida e outra de volta;

        T = np.array([[1, 0, image.shape[0]/2], [0, 1, image.shape[1]/2], [0, 0, 1]])
        R = np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0, 0,1]])
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
