# AI自己紹介ジェネレーター

人の名前を入力すると、Azure OpenAI (GPT-4o) を使用して架空の自己紹介文（約2000字）を生成するWebアプリケーションです。

## 機能

- 名前入力による自己紹介文の自動生成
- ChatGPTライクなストリーミング表示
- レスポンシブデザイン（左側：入力、右側：出力）
- リアルタイムタイピング効果

## 技術スタック

- **バックエンド**: Flask (Python)
- **フロントエンド**: HTML, CSS, JavaScript
- **AI**: Azure OpenAI GPT-4o
- **スタイリング**: CSS Grid, Flexbox

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. Azure OpenAI設定

`app.py` の以下の部分を実際の値に変更してください：

```python
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_KEY = "your-api-key-here"
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"
DEPLOYMENT_NAME = "gpt-4o"
```

### 3. アプリケーションの起動

```bash
python app.py
```

アプリケーションは `http://localhost:5000` で起動します。

## 使用方法

1. 左側の入力欄に名前を入力
2. 「自己紹介を生成」ボタンをクリック
3. 右側に生成された自己紹介がリアルタイムで表示されます

## ファイル構成

```
self-intro/
├── app.py                 # Flaskアプリケーション
├── requirements.txt       # Python依存関係
├── README.md             # このファイル
├── templates/
│   └── index.html        # メインHTMLテンプレート
└── static/
    ├── css/
    │   └── style.css     # スタイルシート
    └── js/
        └── script.js     # JavaScript
```

## 注意事項

- Azure OpenAIのAPIキーとエンドポイントの設定が必要です
- 生成には数秒から数十秒かかる場合があります
- 生成される自己紹介は完全に架空のものです
