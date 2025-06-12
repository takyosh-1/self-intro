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
                demo_text = f"""# {name}の自己紹介

こんにちは、{name}と申します。東京都出身で、幼い頃から好奇心旺盛な性格でした。小学生の時から読書が大好きで、特に冒険小説や科学の本を読み漁っていました。

- **中学・高校時代**: テニス部で活動し、仲間との絆を深めました
- **大学**: 経済学部でマクロ経済学やマーケティングを学習
- **アルバイト**: カフェの店員として接客スキルを習得
- **留学**: 大学3年生でオーストラリアに短期留学
- **現職**: IT企業でプロジェクトマネージャーとして勤務

- **料理**: 週末に新しいレシピに挑戦
- **写真撮影**: 街歩きをしながら風景を撮影
- **ドローン空撮**: 最近興味を持ち始めた新しい趣味
- **ハイキング**: 月に一度友人たちと自然の中でリフレッシュ

楽観的で前向きな性格ですが、細かいところにも気を配る慎重さも持ち合わせています。「相手の立場に立って考える」ことを心がけており、人との出会いを大切にしています。多様な価値観を受け入れることで、自分自身も成長していきたいと考えています。

- **社会貢献**: 自分の経験とスキルを活かしたプロジェクトの立ち上げ
- **地域課題解決**: テクノロジーを使った地域社会の課題解決
- **世界一周旅行**: 様々な文化に触れながら視野を広げたい

学び続ける姿勢を忘れず、周りの人たちと協力しながら充実した人生を送っていきたいと思います。どうぞよろしくお願いいたします。"""
                
                import time
                for char in demo_text:
                    yield f"data: {json.dumps({'content': char})}\n\n"
                    time.sleep(0.02)  # Small delay to simulate streaming
                return
            
            prompt = f"""
            {name}という名前の人物の架空の自己紹介を2000字程度でマークダウン形式で作成してください。
            以下のような構造で、見出しを使って整理してください：


            - 出身地や生い立ちについて

            - 学校での経験や現在の仕事について

            - 好きなことや得意なことについて

            - 自分の性格や大切にしていることについて

            - これからやりたいことや目標について

            - 印象的なエピソードや追加情報

            各セクションは具体的で魅力的な内容にしてください。マークダウン形式で見やすく構造化してください。
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
