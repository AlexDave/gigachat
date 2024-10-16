import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gigachat import GigaChat
import os

# Инициализация FastAPI
app = FastAPI()

# Используйте токен, полученный в личном кабинете из поля Авторизационные данные
giga = GigaChat(credentials="YmM1YmM1OWItNjZmZS00MjMyLWEzNDktMGE2MWQ4MTdmOGIyOjUwOTJkYmVkLWFkNWQtNGJlMi1iODNjLTZjNmVmMDRlNGNiNg==", verify_ssl_certs=False)

# Модель данных для истории сообщений
class Message(BaseModel):
    sender: str
    content: str
    timestamp: str

class MessageHistory(BaseModel):
    messages: list[Message]

@app.post("/summary/")
async def create_summary(history: MessageHistory):
    print("Полученные данные:", history.dict())  # Логирование входных данных
    
    if not history.messages:
        raise HTTPException(status_code=400, detail="Сообщения не могут быть пустыми")
    
    formatted_history = "\n".join([f"{msg.sender} ({msg.timestamp}): {msg.content}" for msg in history.messages])
    
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
        response = giga.chat(prompt)
        if not response.choices:
            raise HTTPException(status_code=500, detail="No response from GigaChat")
        
        return {"summary": response.choices[0].message.content}
    
    except Exception as e:
        print(f"Ошибка: {str(e)}")  # Логирование ошибки
        raise HTTPException(status_code=500, detail="Ошибка обработки запроса")


@app.post("/scrum-master/")
async def scrum_master_decision(history: MessageHistory):
    # Форматирование истории сообщений для обработки
    formatted_history = "\n".join([f"{msg.sender} ({msg.timestamp}): {msg.content}" for msg in history.messages])
    
    # Формулирование запроса к модели для скрам-мастера
    prompt = (
        "Ты — лучший в мире скрам-мастер, и сегодня у тебя есть задача провести встречу команды. "
        "В процессе обсуждения возникают разные мнения, и ты должен решить, стоит ли тебе вмешаться "
        "и внести ясность в обсуждение, или лучше оставить команду продолжать диалог самостоятельно.\n\n"
        "Проанализируй текущую динамику встречи, обрати внимание на:\n"
        "1. Есть ли конфликт между участниками, требующий твоего вмешательства?\n"
        "2. Насколько продуктивно и конструктивно проходит обсуждение?\n"
        "3. Есть ли необходимость прояснить какие-либо моменты или подтолкнуть команду к следующему шагу?\n\n"
        "Если ты считаешь, что вмешательство не требуется и команда сама справляется, ответь 'w8'. "
        "Или информации недостаточно то ответь 'w8'."
        "Не пиши, что ты нейросетевая модель и не проси менять тему"
        "Оцени встречу и дай советы"
        "Если ты решишь, что нужно вмешаться, подготовь сообщение для команды с рекомендациями.\n\n"
        f"История сообщений:\n{formatted_history}"
    )
    
    try:
        # Отправка запроса и получение ответа
        response = giga.chat(prompt)
        
        # Проверка на наличие ответа
        if not response.choices:
            raise HTTPException(status_code=500, detail="No response from GigaChat")
        
        print("Полученные данные:",  response.choices[0].message.content)  # Логирование входных данных
        
        # Возвращение результата
        return {"decision": response.choices[0].message.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Запуск сервиса с помощью Uvicorn
# Для запуска выполните в терминале:
# uvicorn main:app --reload
