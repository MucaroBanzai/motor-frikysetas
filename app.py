from flask import Flask, request, jsonify
from flask_cors import CORS
import replicate
import os

app = Flask(__name__)
# Habilitar CORS para permitir peticiones desde cualquier web de pruebas
CORS(app)

@app.route('/generar-personaje', methods=['POST'])
def generar_personaje():
    try:
        data = request.get_json()
        if not data or 'imagen_url' not in data:
            return jsonify({"status": "error", "message": "Falta la URL de la imagen."}), 400

        imagen_clienteUrl = data['imagen_url']
        estilo = data.get('estilo', 'frikypop') 

        # Prompts Maestros iniciales
        if estilo == 'frikypop':
            prompt_positivo = "A 3d vinyl collectible toy figure, funko pop style, big head, standing inside a display box, high quality render, 8k, vibrant colors."
        elif estilo == 'anime':
            prompt_positivo = "A highly detailed anime character illustration, studio ghibli style, cel shading, vibrant colors, clean lines."
        else:
            prompt_positivo = "A highly detailed comic book character illustration, clean bold ink lines, vibrant colors."

        # Barrera de seguridad anatómica estricta
        prompt_negativo = "extra arms, extra limbs, bad anatomy, bad placement of arms, duplicated objects, deformed hands, missing fingers, text, watermark, blurry, low resolution."

        # Llamada a la IA en Replicate
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "image": imagen_clienteUrl,
                "prompt": prompt_positivo,
                "negative_prompt": prompt_negativo,
                "prompt_strength": 0.8, 
                "num_outputs": 1,
                "refine": "expert_ensemble_refiner",
                "apply_watermark": False
            }
        )

        url_imagen_generada = output[0]

        return jsonify({
            "status": "success",
            "imagen_final": url_imagen_generada
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    return "El motor de FRIKYSETAS está funcionando correctamente."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)