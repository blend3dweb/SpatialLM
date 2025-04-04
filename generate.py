import sys
import json
import time
import os
from pygltflib import GLTF2, Scene, Node, Mesh, Primitive, Accessor, BufferView, Buffer
import numpy as np

def generate_model(prompt):
    try:
        # Создаем папку для моделей, если её нет
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        os.makedirs(models_dir, exist_ok=True)

        # Генерируем уникальное имя для модели
        timestamp = int(time.time())
        output_filename = f"generated_model_{timestamp}.glb"
        output_path = os.path.join(models_dir, output_filename)

        # Создаем простую GLTF-модель с помощью pygltflib
        gltf = GLTF2(
            asset={
                "version": "2.0",
                "generator": "Python GLTF Generator"
            },
            scene=0,
            scenes=[Scene(nodes=[0])],
            nodes=[Node(mesh=0)],
            meshes=[
                Mesh(
                    primitives=[
                        Primitive(
                            attributes={
                                "POSITION": 0,
                                "NORMAL": 1
                            },
                            indices=2
                        )
                    ]
                )
            ],
            accessors=[
                # Вершины (позиции)
                Accessor(
                    bufferView=0,
                    componentType=5126,  # FLOAT
                    count=8,            # 8 вершин
                    type="VEC3",
                    max=[1.0, 1.0, 1.0],
                    min=[-1.0, -1.0, -1.0]
                ),
                # Нормали
                Accessor(
                    bufferView=1,
                    componentType=5126,  # FLOAT
                    count=8,            # 8 нормалей
                    type="VEC3",
                    max=[1.0, 1.0, 1.0],
                    min=[-1.0, -1.0, -1.0]
                ),
                # Индексы
                Accessor(
                    bufferView=2,
                    componentType=5123,  # UNSIGNED_SHORT
                    count=36,           # 12 треугольников * 3 индекса
                    type="SCALAR"
                )
            ],
            bufferViews=[
                # Буфер для вершин
                BufferView(
                    buffer=0,
                    byteOffset=0,
                    byteLength=96,  # 8 вершин * 3 компонента * 4 байта
                    target=34962     # ARRAY_BUFFER
                ),
                # Буфер для нормалей
                BufferView(
                    buffer=0,
                    byteOffset=96,
                    byteLength=96,  # 8 нормалей * 3 компонента * 4 байта
                    target=34962     # ARRAY_BUFFER
                ),
                # Буфер для индексов
                BufferView(
                    buffer=0,
                    byteOffset=192,
                    byteLength=72,  # 36 индексов * 2 байта
                    target=34963    # ELEMENT_ARRAY_BUFFER
                )
            ],
            buffers=[
                Buffer(uri="data.bin", byteLength=264)  # Добавляем URI
            ]
        )

        # Добавляем бинарные данные в буфер
        binary_data = bytearray()

        # Вершины (позиции)
        position_data = np.array([
            -1.0, -1.0, -1.0,
             1.0, -1.0, -1.0,
             1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0, -1.0,  1.0,
             1.0, -1.0,  1.0,
             1.0,  1.0,  1.0,
            -1.0,  1.0,  1.0
        ], dtype=np.float32).tobytes()
        binary_data.extend(position_data)

        # Нормали
        normal_data = np.array([
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0,  1.0,
            0.0, 0.0,  1.0,
            0.0, 0.0,  1.0,
            0.0, 0.0,  1.0
        ], dtype=np.float32).tobytes()
        binary_data.extend(normal_data)

        # Индексы
        index_data = np.array([
            0, 1, 2, 2, 3, 0,  # Face 1
            4, 5, 6, 6, 7, 4,  # Face 2
            0, 4, 5, 5, 1, 0,  # Face 3
            1, 5, 6, 6, 2, 1,  # Face 4
            2, 6, 7, 7, 3, 2,  # Face 5
            3, 7, 4, 4, 0, 3   # Face 6
        ], dtype=np.uint16).tobytes()
        binary_data.extend(index_data)

        # Отладочная информация
        print("Binary data length:", len(binary_data))
        print("Output path:", output_path)
        print("Accessors:", gltf.accessors)
        print("Buffer Views:", gltf.bufferViews)
        print("Buffers:", gltf.buffers)

        # Проверка индексов
        try:
            assert len(gltf.accessors) == 3, "Incorrect number of accessors"
            assert gltf.meshes[0].primitives[0].attributes["POSITION"] == 0, "Invalid POSITION index"
            assert gltf.meshes[0].primitives[0].attributes["NORMAL"] == 1, "Invalid NORMAL index"
            assert gltf.meshes[0].primitives[0].indices == 2, "Invalid indices index"
        except AssertionError as e:
            print(f"Assertion error: {str(e)}")
            return {"status": "error", "message": f"Assertion error: {str(e)}"}

        # Сохраняем бинарные данные в отдельный файл
        with open(os.path.join(models_dir, "data.bin"), "wb") as f:
            f.write(binary_data)

        # Сохраняем модель в формате GLB
        gltf.binary_data = binary_data  # Устанавливаем бинарные данные напрямую
        gltf.save_binary(output_path)   # Передаем путь к файлу

        # Формирование результата
        result = {
            "status": "success",
            "message": f"Generated 3D model for prompt: {prompt}",
            "model_url": f"/models/{output_filename}",
            "metadata": {
                "format": "GLB",
                "size": len(binary_data),
                "polygons": 12,
                "vertices": 8
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