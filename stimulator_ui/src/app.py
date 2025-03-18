from ui import AppUI
import asyncio

async def main():
    app_ui = AppUI()
    await app_ui.run()

if __name__ == "__main__":
    asyncio.run(main())