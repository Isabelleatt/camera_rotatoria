import numpy as np
from funcoes import *
import cv2 as cv


def run():

    cap = cv.VideoCapture(0)

    width = 320
    height = 240
    ang = 0
    estado = 'padrao'
    aum = 1
    escala = 1
    salvar = input('Deseja gravar o video? (y/n)')
    
    if salvar == "y":
        nome = input('Digite o nome do video: ') + '.mp4'
        writer = cv.VideoWriter(nome, cv.VideoWriter_fourcc(*'mp4v'), 20, (width,height))

    if not cap.isOpened():
        print("Não consegui abrir a câmera!")
        exit()


    while True:
        # Captura um frame da câmera
        ret, frame = cap.read()

        if not ret:
            print("Não consegui capturar frame!")
            break


        frame = cv.resize(frame, (width,height), interpolation =cv.INTER_AREA)
        image = np.array(frame).astype(float)/255

        key = cv.waitKey(1)

        # estilo de transformação
        if key == ord('p'):
            estado = 'padrao'
            escala = 1
        elif key == ord('r'):
            estado = 'controle'
            aum = 1
        elif key == ord('e'):
            estado = 'expandir'

        # controle da rotação
        if estado =='controle':
            if key == ord('a'): # gira para a esquerda
                aum = abs(aum)
            elif key == ord('d'): # gira para a direita
                aum = abs(aum) * -1
            elif key == ord('w'): # aumenta a velocidade
                aum *= 1.25
            elif key == ord('s'): # diminui a velocidade
                aum *= 0.75
            ang += aum
        else:
            ang += 1
        
        # controle do zoom
        if estado == 'expandir':
            if key == ord('i'): # zoom in
                escala += 0.1
            elif key == ord('o'): # zoom out
                escala -= 0.1

        
        aum = delimita_aumento(aum)
        ang = delimita_angulo(ang)
        escala = delimita_escala(escala)
            
        image_ = transforma_imagem(image, ang, escala, estado)

        cv.imshow('Minha Imagem!', image_)
        
        # encerra o loop
        if key == ord('q'):
            break
        
        if salvar == 'y':
            writer.write((image_* 255).astype(np.uint8))



    cap.release()
    if salvar == 'y':
        writer.release()
    cv.destroyAllWindows()

run()
