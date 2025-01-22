from app import App
from logging import error, debug, basicConfig, INFO
from time import time


basicConfig(
    level=INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=f'logs/app_detector_bot{time()}.log',
    filemode='a'
)

if __name__ == '__main__':
    try:
        app = App()
        try:
            app.run()
        except Exception as err:
            error(f"Unexpected error during RUN App: {str(err)}")
            debug("Stack trace:", exc_info=True)
    except Exception as err:
        error(f"UnExcepted error during creation App: {str(err)}")
        debug("Stack trace:", exc_info=True)

