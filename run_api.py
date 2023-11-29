import uvicorn

if __name__ == '__main__':
    uvicorn.run('api.app:BOT_ADMIN', reload=True)
