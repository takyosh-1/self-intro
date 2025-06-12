from flask import Flask, render_template, request, jsonify, Response
import json
import time
import os
from openai import AzureOpenAI

app = Flask(__name__)

AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_KEY = "your-api-key-here"
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"
DEPLOYMENT_NAME = "gpt-4o"

try:
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version=AZURE_OPENAI_API_VERSION
    )
except Exception as e:
    print(f"Warning: Azure OpenAI client initialization failed: {e}")
    print("This is expected with sample credentials. The app will still run but API calls will fail.")
    client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_intro', methods=['POST'])
def generate_intro():
    data = request.get_json()
    name = data.get('name', '')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    def generate():
        try:
            if client is None:
                demo_text = f"""こんにちは、{name}と申します。

私は東京都出身で、幼い頃から好奇心旺盛な性格でした。小学生の時から読書が大好きで、特に冒険小説や科学の本を読み漁っていました。中学・高校時代は部活動にも積極的に参加し、テニス部で汗を流しながら仲間との絆を深めました。

大学では経済学部に進学し、マクロ経済学やマーケティングについて学びました。在学中はアルバイトでカフェの店員をしており、接客を通じて人とのコミュニケーションの大切さを学びました。また、大学3年生の時には短期留学でオーストラリアに行き、異文化体験を通じて視野を広げることができました。

卒業後は IT企業に就職し、現在はプロジェクトマネージャーとして働いています。チームをまとめながら、お客様のニーズに応える製品開発に携わっています。仕事では常に「相手の立場に立って考える」ことを心がけており、この姿勢が良好な人間関係の構築に役立っています。

趣味は料理と写真撮影です。週末には新しいレシピに挑戦したり、街を歩きながら面白い風景を撮影したりしています。最近はドローンを使った空撮にも興味を持ち始めました。また、月に一度は友人たちとハイキングに出かけ、自然の中でリフレッシュしています。

性格は楽観的で、困難な状況でも前向きに取り組むことができます。一方で、細かいところにも気を配る慎重さも持ち合わせています。人との出会いを大切にし、多様な価値観を受け入れることで、自分自身も成長していきたいと考えています。

将来の目標は、自分の経験とスキルを活かして、社会に貢献できるプロジェクトを立ち上げることです。特に、テクノロジーを使って地域社会の課題解決に取り組みたいと思っています。また、いつかは世界一周旅行をして、様々な文化に触れながら自分の視野をさらに広げたいという夢もあります。

これからも学び続ける姿勢を忘れず、周りの人たちと協力しながら、充実した人生を送っていきたいと思います。どうぞよろしくお願いいたします。"""
                
                import time
                for char in demo_text:
                    yield f"data: {json.dumps({'content': char})}\n\n"
                    time.sleep(0.02)  # Small delay to simulate streaming
                return
            
            prompt = f"""
            {name}という名前の人物の架空の自己紹介を2000字程度で作成してください。
            以下の要素を含めてください：
            - 出身地や生い立ち
            - 学歴や職歴
            - 趣味や特技
            - 性格や価値観
            - 将来の目標や夢
            - その他の個人的なエピソード
            
            自然で魅力的な自己紹介文を作成してください。
            """
            
            response = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "あなたは創造的な文章作成のエキスパートです。"},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
                max_tokens=3000,
                temperature=0.7
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    yield f"data: {json.dumps({'content': content})}\n\n"
                    
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
