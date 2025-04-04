import sys
import json
import os
import trimesh
import numpy as np
import time  # Добавляем импорт модуля time

def generate_model(prompt):
    try:
        # Создаем папку для моделей, если её нет
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        os.makedirs(models_dir, exist_ok=True)

        # Генерируем уникальное имя для модели
        timestamp = int(time.time())
        output_filename = f"generated_model_{timestamp}.glb"
        output_path = os.path.join(models_dir, output_filename)

        # Создаем куб
        box = trimesh.creation.box(extents=(2, 2, 2))  # Размеры куба: 2x2x2

        # Добавляем материал (опционально)
        material = trimesh.visual.material.SimpleMaterial(
            diffuse=[1.0, 0.0, 0.0, 1.0],  # Красный цвет
            ambient=[0.2, 0.2, 0.2, 1.0],
            specular=[0.8, 0.8, 0.8, 1.0]
        )
        box.visual = trimesh.visual.texture.TextureVisuals(material=material)

        # Сохраняем модель в формате GLB
        box.export(output_path, file_type="glb")

        # Формирование результата
        result = {
            "status": "success",
            "message": f"Generated 3D model for prompt: {prompt}",
            "model_url": f"/models/{output_filename}",
            "metadata": {
                "format": "GLB",
                "size": os.path.getsize(output_path),
                "polygons": len(box.faces),
                "vertices": len(box.vertices)
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