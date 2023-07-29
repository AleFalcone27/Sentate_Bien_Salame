import cv2 as cv
from win11toast import toast

cont = 0 # Creamos el contador para detectar el iempo transcurrido 

face_cascade = cv.CascadeClassifier("face_cascade.xml") # cargamos un clasificador de cascada Haar entrenado para detectar rostros humanos

video_cap = cv.VideoCapture(0)  # Creamos el capturador de video

if not video_cap.isOpened():  # Verificamos que este abierto y sino printeamos error
    print("Error al abrir la cámara")

def capturar_video(cap):
    ret, frame = cap.read()  # Leemos cada uno de los fotogramas
    # - Desempaquetamamos el return del metodo .read()
    # - ret: Booleano que determina si el fotograma se pudo leer correctamente
    # - frame: La imagen en sí leída
    if not ret:
        print("Error al capturar el fotograma")
    return frame


def detect_face():
    """Esta función se encarga de detectar rostros"""
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # Transforma el fram a una imagen en escala de grises El detector de cascada Haar funciona mejor con imágenes en escala de grises, ya que busca patrones basados en cambios de intensidad y no en el color.
    face = face_cascade.detectMultiScale(gray, 1.1, 4) # Esta línea de código aplica el clasificador de cascada Haar a la imagen en escala de grises (gray). La función detectMultiScale() devuelve una lista de rectángulos que representan las regiones donde se han detectado los rostros en la imagen.

    for (x, y, w, h) in face:
        cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3) # Dibujamos el rectangulo 
        if x: 
            return True # Si existe el rectangulo devolvemos True y sino devolvemos None


def throw_notification():

    toast("SENTATE BIEN SALAME") # Arrojamos la notificación con su mensaje (Podes customizarlo a tu gusto

# Loop principal
while True:
    frame = capturar_video(video_cap)  # Capturamos el video en vivo

    detected = detect_face() # Chekeamos si hay algun rostro en nuestra captura

    if detected == True: 
        cont = 0
    else:
        cont +=1
        # - Mientras se detecte una cara el contador esta en 0
        # - Sumamos 1 al contador por cada iteración que no se dectecte una cara 
        # - Si se detecta una cara el contador vuelve a 0
        # - Esto nos permite determinar la cantidad de iteraciones que se hicieron sin que se detecte una cara y asi poder arrojar la notificación
    
    print(cont) # Printeamos el contador 
    
    #  ⬇ Descomenta la linea de abajo para poder ver el trackeo en vivo ⬇
    # cv.imshow("Face tracker", frame) # Mostramos El frame

    if cv.waitKey(1) & 0xFF == 27:  # Presionar Esc para salir
        break

    if cont > 120: # Tic en el cual se triggerea la notificación 
        
        throw_notification()
        
video_cap.release() # Frenamos la captura del video

