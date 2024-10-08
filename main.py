import json
from fastapi import FastAPI
from pydantic import BaseModel
from gigachat import GigaChat

# Инициализация FastAPI
app = FastAPI()

# Используйте токен, полученный в личном кабинете из поля Авторизационные данные
giga = GigaChat(credentials='YmM1YmM1OWItNjZmZS00MjMyLWEzNDktMGE2MWQ4MTdmOGIyOmQyN2EwMjdiLTlmYzktNGRkOC1hMjQyLTBkYTIzMGUzMTE2MA==', verify_ssl_certs=False)

# Модель данных для истории сообщений
class Message(BaseModel):
    speaker: str
    message: str
    time: str

class MessageHistory(BaseModel):
    messages: list[Message]

@app.post("/summary/")
async def create_summary(history: MessageHistory):
    # Форматирование истории сообщений для обработки
    formatted_history = "\n".join([f"{msg.speaker} ({msg.time}): {msg.message}" for msg in history.messages])
    
    # Формулирование запроса к модели
    prompt = (
        "Проанализируйте следующую историю сообщений:\n"
        f"{formatted_history}\n"
        "Результат: Краткое резюме встречи, состоящее из следующих пунктов: "
        "1. Основные темы обсуждения "
        "2. Ключевые решения, принятые на встрече "
        "3. Упомянутые действия и их исполнители "
        "4. Важные моменты и выводы"
    )
    
    # Отправка запроса и получение ответа
    response = giga.chat(prompt)
    
    # Возвращение результата
    return {"summary": response.choices[0].message.content}

# Запуск сервиса с помощью Uvicorn
# Для запуска выполните в терминале:
# uvicorn main:app --reload
