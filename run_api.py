import uvicorn
from loguru import logger


logger.add('BotLOG.log', encoding='utf-8')

if __name__ == '__main__':
    uvicorn.run(
        'api.app:BOT_ADMIN',
        host='web_api',
        port=8000,
        reload=True
    )
