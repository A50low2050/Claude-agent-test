import os
import anthropic

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
# Инициализация клиента Claude
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def generate_swagger():
    # 1. Читаем исходный код (например, файлы контроллеров)
    with open("main.py", "r", encoding="utf-8") as file:
        source_code = file.read()

    # 2. Формируем промпт для Claude
    prompt = f"""
    Ты — эксперт по API-документации. Проанализируй следующий код на Python и сгенерируй для эндпоинта users
    актуальную OpenAPI 3.0 спецификацию в формате YAML. 
    Верни ТОЛЬКО валидный YAML код без дополнительных объяснений.

    Код:
    {source_code}
    """

    # 3. Отправляем запрос к Claude Sonnet
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # 4. Сохраняем результат
    swagger_content = response.content[0].text
    swagger_content = swagger_content.replace("```yaml\n", "").replace("```yml\n", "").replace("```", "").strip()

    with open("docs/swagger.yaml", "w", encoding="utf-8") as out_file:
        out_file.write(swagger_content)

    print("Swagger-документация успешно сгенерирована!")


if __name__ == "__main__":
    generate_swagger()