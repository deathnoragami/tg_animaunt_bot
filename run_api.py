import uvicorn
from loguru import logger

if __name__ == '__main__':
    logger.add('BotLOG.log', encoding='utf-8')
    uvicorn.run(
        'api.app:BOT_ADMIN',
        host='web_api',
        port=8000,
        reload=True
    )
