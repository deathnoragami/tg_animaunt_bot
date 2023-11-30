import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        'api.app:BOT_ADMIN',
        host='web_api',
        port=8000,
        reload=True
    )
