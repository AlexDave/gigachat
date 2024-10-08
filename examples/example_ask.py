"""Пример вопрос - ответ"""
from gigachat import GigaChat

# Используйте токен, полученный в личном кабинете из поля Авторизационные данные
with GigaChat(credentials='YmM1YmM1OWItNjZmZS00MjMyLWEzNDktMGE2MWQ4MTdmOGIyOmQyN2EwMjdiLTlmYzktNGRkOC1hMjQyLTBkYTIzMGUzMTE2MA==', verify_ssl_certs=False) as giga:
    response = giga.chat("Какие факторы влияют на стоимость страховки на дом?")
    print(response.choices[0].message.content)
