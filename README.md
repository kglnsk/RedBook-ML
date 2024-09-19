# RedBook-ML


## Обзор

**API классификатора изображений CLIP** — это основанный на FastAPI сервис, который позволяет пользователям загружать изображения и получать результаты классификации краснокнижных животных с использованием модели CLIP (Contrastive Language–Image Pretraining). Этот API разработан так, чтобы быть простым, эффективным и легко интегрируемым в различные приложения.

## Установка без Docker
```
pip install -r requirements.txt
```

```
uvicorn app:app --host 0.0.0.0 --port 8000
curl -X POST "http://localhost:8000/classify" -F "file=@path_to_your_image.jpg"

```
## Docker
```
docker build -t clip-image-classifier-api .
docker run -d -p 8000:8000 clip-image-classifier-api
```
