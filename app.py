from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route('/skill', methods=['POST'])
def skill():
    body = request.get_json()
    user_message = body['action']['params'].get('question', '질문을 입력해주세요.')
    
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        system="당신은 복약 관리 전문 AI입니다. 약 복용법, 부작용, 주의사항 등을 친절하게 안내해주세요. 답변은 200자 이내로 간결하게 해주세요.",
        messages=[{"role": "user", "content": user_message}]
    )
    
    response_text = message.content[0].text
    
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": response_text
                }
            }]
        }
    })

if __name__ == '__main__':
    app.run()
