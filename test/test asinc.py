import asyncio
import schedule


def GoCode():
    print('second past')

async def async_func():
    print('Запуск ...')
    await asyncio.sleep(1)
    print('... Готово!')

async def schedule_check():
    schedule.every(1).seconds.do(GoCode())

async def main():
    async_func()  # этот код ничего не вернет
    await async_func()
    await schedule_check()


asyncio.run(main())