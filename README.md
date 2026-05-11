# Workplace Mouthpiece (职场嘴替)

A Feishu Bot that helps you reply to colleagues with different personas.

## Features

- 6 unique personas to choose from
- 3 reply versions per message (mild, standard, fire)
- Fun quiz to discover your persona
- Mock mode when no OpenAI API key

## Deployment

1. Set environment variables in Render:
   - FEISHU_APP_ID
   - FEISHU_APP_SECRET
   - OPENAI_API_KEY (optional)

2. Build Command: `pip install -r requirements.txt`

3. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Feishu Configuration

1. Create a custom app in Feishu Open Platform
2. Add event subscription: `im.message.receive_v1`
3. Set request URL to your Render URL
4. Publish the app

## Personas

- 🕊️ Sha Seng (Peacemaker)
- 🔥 Hanzawa Naoki (Rebel)
- 🌀 Zhen Huan (Diplomat)
- 🧊 Yu Hua (Philosopher)
- 🎭 Yue Yunpeng (Comedian)
- 💀 Xiao S (Critic)
