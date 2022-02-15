import asyncio

# async를 포함하는 함수 -> 코루틴
async def async_func1():
    print('hello')

# 일반적으로 사용하는 이벤트 루프
# asyncio.run(async_func1())

# 이벤트 루프를 세부적으로 제어해야 할 때 사용
#loop = asyncio.get_event_loop()
#loop.run_until_complete(async_func1())
#loop.close()

# 실제 활용해보기

async def make_americano():
    print("Americano Start")
    await asyncio.sleep(3)
    print("Americano End")
    return "AMERICANO"
async def make_latte():
    print("Latte Start")
    await asyncio.sleep(5)
    print("Latte End")
    return "LATTE"

async def main():
    coro1 = make_americano()
    coro2 = make_latte()
    # 두개의 이벤트를 동시에 실행
    result = await asyncio.gather(
        coro1,coro2
    )
    print(result)

print("MainStart")
asyncio.run(main())
print("Main End")