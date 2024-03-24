#!/usr/bin/env python3

from  app import App

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main():
    app = App(False)
    app.MainLoop()

if __name__ == "__main__":
    logger.info('start')
    main()
