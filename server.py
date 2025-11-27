"""
Módulo principal para la aplicación Flask del detector de emociones.
Procesa texto de entrada, llama al servicio de detección de emociones
y devuelve el resultado formateado al cliente.
"""
from flask import Flask, render_template, request, json
from EmotionDetection import emotion_detector
#Initiate the flask app :
app = Flask("emotionDetector")

@app.route("/emotionDetector")
def receive_emotion():
    """
    Recibe el texto del cliente vía query parameter, llama al detector de emociones,
    y devuelve el análisis formateado o un mensaje de error.
    """
    text_to_analyze = request.args.get('textToAnalyze')
    if text_to_analyze.strip() == "" or text_to_analyze.strip() == "None":
        return "¡Texto inválido! ¡Por favor, inténtalo de nuevo!."

    response = emotion_detector(text_to_analyze)
    message = "For the given statement, the system response is"
    emotion_scores = json.loads(response)
    result_1 = {
        'anger': emotion_scores['anger'],
        'disgust': emotion_scores['disgust'],
        'fear': emotion_scores['fear'],
        'joy': emotion_scores['joy'],
        'sadness': emotion_scores['sadness']
     }
    joy = result_1['joy']
    anger = result_1['anger']
    disgust = result_1['disgust']
    sadness = result_1['sadness']
    fear = result_1['fear']
    #score_mas_alto = max(result_1.values())
    emocion_dominante = max(result_1, key=result_1.get)
    message1 = (message + "'anger:'" + str(anger) + "\n" +
    "'disgust:'" + str(disgust) + "\n" +
    "'fear:'" + str(fear) + "\n" +
    "'joy:'" + str(joy) + " and " + "\n" +
    "'sadness:'" + str(sadness) + "." + " The dominant emotion is " + emocion_dominante + ". " )
    return str(message1)

@app.route("/")
def render_index_page():
    """Renderiza la página HTML principal."""
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
