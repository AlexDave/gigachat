import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gigachat import GigaChat
import os

# Инициализация FastAPI
app = FastAPI()

# Используйте токен, полученный в личном кабинете из поля Авторизационные данные
giga = GigaChat(credentials="YmM1YmM1OWItNjZmZS00MjMyLWEzNDktMGE2MWQ4MTdmOGIyOmI5YWFmMjU1LWYwN2EtNDdlMS1hNTg1LTY5NmRkYmJlZGNhYw==", verify_ssl_certs=False)

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
    
    # Формулирование запроса к модели для резюме
    prompt = (
        "Проанализируйте следующую историю сообщений:\n"
        f"{formatted_history}\n"
        "Результат: Краткое резюме встречи, состоящее из следующих пунктов: "
        "1. Основные темы обсуждения "
        "2. Ключевые решения, принятые на встрече "
        "3. Упомянутые действия и их исполнители "
        "4. Важные моменты и выводы"
    )
    
    try:
        # Отправка запроса и получение ответа
        response = giga.chat(prompt)
        
        # Проверка на наличие ответа
        if not response.choices:
            raise HTTPException(status_code=500, detail="No response from GigaChat")
        
        # Возвращение результата
        return {"summary": response.choices[0].message.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrum-master/")
async def scrum_master_decision(history: MessageHistory):
    # Форматирование истории сообщений для обработки
    formatted_history = "\n".join([f"{msg.speaker} ({msg.time}): {msg.message}" for msg in history.messages])
    
    # Формулирование запроса к модели для скрам-мастера
    prompt = (
        "Ты — лучший в мире скрам-мастер, и сегодня у тебя есть задача провести встречу команды. "
        "В процессе обсуждения возникают разные мнения, и ты должен решить, стоит ли тебе вмешаться "
        "и внести ясность в обсуждение, или лучше оставить команду продолжать диалог самостоятельно.\n\n"
        "Проанализируй текущую динамику встречи, обрати внимание на:\n"
        "1. Есть ли конфликт между участниками, требующий твоего вмешательства?\n"
        "2. Насколько продуктивно и конструктивно проходит обсуждение?\n"
        "3. Есть ли необходимость прояснить какие-либо моменты или подтолкнуть команду к следующему шагу?\n\n"
        "Если ты считаешь, что вмешательство не требуется и команда сама справляется, ответь '8'. "
        "Если ты решишь, что нужно вмешаться, подготовь сообщение для команды с рекомендациями.\n\n"
        f"История сообщений:\n{formatted_history}"
    )
    
    try:
        # Отправка запроса и получение ответа
        response = giga.chat(prompt)
        
        # Проверка на наличие ответа
        if not response.choices:
            raise HTTPException(status_code=500, detail="No response from GigaChat")
        
        # Возвращение результата
        return {"decision": response.choices[0].message.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Запуск сервиса с помощью Uvicorn
# Для запуска выполните в терминале:
# uvicorn main:app --reload
