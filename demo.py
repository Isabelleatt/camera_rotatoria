import numpy as np
from funcoes import *

# Instalar a biblioteca cv2 pode ser um pouco demorado. Não deixe para ultima hora!
import cv2 as cv


def run():
    # Essa função abre a câmera. Depois desta linha, a luz de câmera (se seu computador tiver) deve ligar.
    cap = cv.VideoCapture(0)

    # Aqui, defino a largura e a altura da imagem com a qual quero trabalhar.
    # Dica: imagens menores precisam de menos processamento!!!
    width = 320
    height = 240
    ang = 0
    estado = 'padrao'
    aum = 1

    # Talvez o programa não consiga abrir a câmera. Verifique se há outros dispositivos acessando sua câmera!
    if not cap.isOpened():
        print("Não consegui abrir a câmera!")
        exit()

    # Esse loop é igual a um loop de jogo: ele encerra quando apertamos 'q' no teclado.
    while True:
        # Captura um frame da câmera
        ret, frame = cap.read()

        # A variável `ret` indica se conseguimos capturar um frame
        if not ret:
            print("Não consegui capturar frame!")
            break

        # Mudo o tamanho do meu frame para reduzir o processamento necessário
        # nas próximas etapas
        frame = cv.resize(frame, (width,height), interpolation =cv.INTER_AREA)

        # A variável image é um np.array com shape=(width, height, colors)
        image = np.array(frame).astype(float)/255

        key = cv.waitKey(1)

        image_ = gira_imagem(image, ang)
        if key == ord('p'):
            estado = 'padrao'
        if key == ord('r'):
            estado = 'controle'
            aum = 1

        
        if estado =='controle':
            if key == ord('a'):
                aum = abs(aum)
            elif key == ord('d'):
                aum = abs(aum) * -1
            elif key == ord('w'):
                aum *= 1.25
            elif key == ord('s'):
                aum *= 0.75
            ang += aum
 
        if estado == 'padrao':
            ang += 1
        
        aum = delimita_aumento(aum)
        ang = delimita_angulo(ang)
            
        # Agora, mostrar a imagem na tela!
        cv.imshow('Minha Imagem!', image_)
        
        # Se aperto 'q', encerro o loop
        if key == ord('q'):
            break

        # aum = keyboard.on_press(on_press)


    # Ao sair do loop, vamos devolver cuidadosamente os recursos ao sistema!
    cap.release()
    cv.destroyAllWindows()

run()
