from core.application import Application

if __name__ == '__main__':
    app = Application('./data/data.txt', './output/result.txt')
    app.run()