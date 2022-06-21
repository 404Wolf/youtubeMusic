import asyncio
from ui import mainWindow
from PyQt6.QtWidgets import QApplication
import helpers


# app = QApplication([]) # sys.argv if command line use is needed
# window = mainWindow()
# window.show()

# app.exec()


async def main():
    data = await helpers.locate.metadata(input("Enter search query: "))
    print(data)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
