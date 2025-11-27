import requests
import json

def emotion_detector(text_to_analyse):
    """
    Realiza una predicción de emociones llamando a un servicio externo 
    y devuelve un string JSON con los scores y la emoción dominante.
    """
    
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    myobj = { "raw_document": { "text": text_to_analyse } }
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    # 1. Enviar la solicitud POST
    try:
        response = requests.post(url, json=myobj, headers=header)
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al servicio: {e}")
        # Retorna el formato de error si hay un problema de red
        return json.dumps({
            'dominant_emotion': 'Error de Conexión', 
            'error_details': str(e)
        }, indent=4)

    # 2. Manejo de Status Code 400 (Error del Cliente o Entrada Inválida)
    if response.status_code == 400:
        output_data_none = {
            'anger': 'None',
            'disgust': 'None',
            'fear': 'None',
            'joy': 'None',
            'sadness': 'None',
            'dominant_emotion': 'None'
        }
        # Aseguramos la indentación de 4 espacios aquí
        respuesta_none = json.dumps(output_data_none, indent=4)
        print("--- Error 400: Entrada Inválida ---")
        print(respuesta_none)
        return respuesta_none

    # 3. Manejo de Respuesta Exitosa (Status Code 200)
    try:
        # Cargar el JSON de la respuesta
        data = json.loads(response.text)
        
        # Acceso seguro a las predicciones (asumiendo la estructura conocida)
        # Usamos .get() para manejar la posible ausencia de claves
        emotion_predictions = data.get('emotionPredictions', [])
        if not emotion_predictions:
            raise ValueError("No se encontraron predicciones de emociones en la respuesta.")
            
        first_prediction = emotion_predictions[0]
        emotion_scores = first_prediction.get('emotion', {})
        
        # Encontrar la emoción dominante y asegurar que todos los scores son números
        # Si no hay scores, usamos un diccionario vacío para max()
        if not emotion_scores:
            dominant_emotion = 'None'
        else:
            # max(..., key=emotion_scores.get) encuentra la clave con el valor más alto
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)

        # 4. Construir el diccionario de salida
        output_data = {
            'anger': emotion_scores.get('anger'),
            'disgust': emotion_scores.get('disgust'),
            'fear': emotion_scores.get('fear'),
            'joy': emotion_scores.get('joy'),
            'sadness': emotion_scores.get('sadness'),
            'dominant_emotion': dominant_emotion
        }

        print("--- Predicción Exitosa ---")
        respuesta = json.dumps(output_data, indent=4)
        print(respuesta)
        return respuesta

    except json.JSONDecodeError:
        # Manejo de error si la respuesta no es un JSON válido
        error_message = f"Error al decodificar JSON. Respuesta: {response.text[:100]}..."
        print(error_message)
        return json.dumps({"dominant_emotion": "JSON Error", "details": error_message}, indent=4)
    
    except Exception as e:
        # Manejo de cualquier otro error (ej. KeyError si falta una clave)
        error_message = f"Error al procesar la respuesta: {e}"
        print(error_message)
        return json.dumps({"dominant_emotion": "Processing Error", "details": error_message}, indent=4)

