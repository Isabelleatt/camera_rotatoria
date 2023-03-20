import numpy as np
from funcoes import *
import cv2 as cv


def run():
    # Essa função abre a câmera. Depois desta linha, a luz de câmera (se seu computador tiver) deve ligar.
    cap = cv.VideoCapture(0)

    # Aqui, defino a largura e a altura da imagem com a qual quero trabalhar.
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

        # estilo de transformação
        if key == ord('p'):
            estado = 'padrao'
        elif key == ord('r'):
            estado = 'controle'
            aum = 1
        elif key == ord('e'):
            estado = 'expandir'
        elif key == ord('m'):
            estado = 'magica'

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
        else:
            ang += 1
            
        if estado == 'expandir':
            if key == ord('i'):
                escala += 0.1
            elif key == ord('o'):
                escala -= 0.1

        
        aum = delimita_aumento(aum)
        ang = delimita_angulo(ang)
        escala = delimita_escala(escala)
            
        if estado == 'expandir':
            image_ = expandir_imagem(image, escala, ang)
            # image_ = gira_imagem(image_, ang)
        elif estado == 'magica':
            image_ = imagem_magica(image, ang)
        else:
            image_ = gira_imagem(image, ang)


        # Agora, mostrar a imagem na tela!
        cv.imshow('Minha Imagem!', image_)
        
        # Se aperto 'q', encerro o loop
        if key == ord('q'):
            break
        
        if salvar == 'y':
            writer.write((image_* 255).astype(np.uint8))


    # Ao sair do loop, vamos devolver cuidadosamente os recursos ao sistema!
    cap.release()
    if salvar == 'y':
        writer.release()
    cv.destroyAllWindows()

run()
