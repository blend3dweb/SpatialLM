import sys
import json
import time

def generate_model(prompt):
    try:
        # Имитация работы модели
        time.sleep(2)  # Имитация задержки
        
        # Формирование результата
        result = {
            "status": "success",
            "message": f"Generated 3D model for prompt: {prompt}",
            "model_url": "http://example.com/models/generated_model.gltf",  # Фиктивная ссылка
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