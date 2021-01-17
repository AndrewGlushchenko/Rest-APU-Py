from api_rest_serv import app
from api_rest_serv import logger

if __name__ == '__main__':
    logger.warning(f'Start server.')
    app.run(host='127.0.0.1', port='5005')
