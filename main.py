import cv2
import os
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# Função para aplicar filtro
def aplicar_filtro(imagem, filtro):
    if filtro == 'blur':
        return imagem.filter(ImageFilter.BLUR)
    elif filtro == 'contour':
        return imagem.filter(ImageFilter.CONTOUR)
    elif filtro == 'detail':
        return imagem.filter(ImageFilter.DETAIL)
    elif filtro == 'sharpen':
        return imagem.filter(ImageFilter.SHARPEN)
    elif filtro == 'enhance_color':
        enhancer = ImageEnhance.Color(imagem)
        return enhancer.enhance(2)
    else:
        return imagem

# Função para adicionar moldura
def adicionar_moldura(imagem, largura_moldura=10, cor_moldura='black'):
    return ImageOps.expand(imagem, border=largura_moldura, fill=cor_moldura)

# Função para tirar foto
def tirar_foto():
    # Criar pasta 'fotos' se não existir
    if not os.path.exists('fotos'):
        os.makedirs('fotos')

    # Iniciar a captura da webcam
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Erro ao acessar a câmera")
        return

    count = 1  # Contador para nomear as fotos
    filtro = None  # Filtro inicial

    while True:
        # Ler a imagem da webcam
        ret, frame = camera.read()
        if not ret:
            print("Erro ao capturar a imagem")
            break

        # Mostrar a imagem capturada ao vivo
        cv2.imshow('Pressione "p" para tirar foto ou "f" para aplicar filtro', frame)

        # Espera pela tecla "p" para capturar a foto, "f" para filtro ou "q" para sair
        key = cv2.waitKey(1) & 0xFF
        if key == ord('p'):  # Se a tecla 'p' for pressionada
            # Nome do arquivo da foto
            foto_nome = f'fotos/foto_{count}.jpg'
            # Salvar a imagem capturada
            cv2.imwrite(foto_nome, frame)
            print(f"Foto salva como '{foto_nome}'")

            # Abrir a imagem usando Pillow
            img = Image.open(foto_nome)

            # Aplicar filtro se selecionado
            if filtro:
                img = aplicar_filtro(img, filtro)
                print(f"Filtro '{filtro}' aplicado na foto '{foto_nome}'")

            # Adicionar moldura
            img = adicionar_moldura(img)
            img.save(foto_nome)
            print(f"Moldura adicionada na foto '{foto_nome}'")

            count += 1  # Incrementar o contador para o próximo nome

        elif key == ord('f'):  # Se a tecla 'f' for pressionada
            # Selecionar o filtro (aqui você pode mudar para outros filtros)
            filtro = 'blur'  # Mude aqui o filtro desejado, exemplo: 'contour', 'detail', etc.
            print(f"Filtro '{filtro}' será aplicado na próxima foto.")

        elif key == ord('q'):  # Se a tecla 'q' for pressionada, sai do loop
            break

    # Liberar a câmera e fechar a janela de visualização
    camera.release()
    cv2.destroyAllWindows()

# Chamar a função para iniciar a captura
tirar_foto()
