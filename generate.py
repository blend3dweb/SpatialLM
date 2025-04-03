import sys
import json
import time
import os

def generate_model(prompt):
    try:
        # Создаем папку для моделей, если её нет
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        os.makedirs(models_dir, exist_ok=True)

        # Сохраняем фиктивную GLTF-модель
        output_path = os.path.join(models_dir, "generated_model.gltf")
        with open(output_path, "w") as f:
            f.write('{"asset": {"version": "2.0"}, "scene": 0, "scenes": [{"nodes": []}]}')

        # Формирование результата
        result = {
            "status": "success",
            "message": f"Generated 3D model for prompt: {prompt}",
            "model_url": f"/models/generated_model.gltf",  # Относительный путь к модели
            "metadata": {
                "format": "GLTF",
                "size": "10MB",
                "polygons": 5000
            }
        }
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No prompt provided"}))
        sys.exit(1)
    
    prompt = sys.argv[1]
    result = generate_model(prompt)
    print(json.dumps(result))