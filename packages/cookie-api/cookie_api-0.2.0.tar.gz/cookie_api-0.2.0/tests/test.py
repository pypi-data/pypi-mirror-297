import asyncio

from cookie import AsyncCookieAPI, CookieAPI

api = CookieAPI(api_key="cb26f209-f2b4-4a25-af61-9a7ca1e9663b")
async_api = AsyncCookieAPI(api_key="cb26f209-f2b4-4a25-af61-9a7ca1e9663b")


USER_ID = 203208036053942272
GUILD_ID = 1010915072694046794


async def start():
    async with async_api as test:
        member_count = await test.get_member_count(GUILD_ID)
        print(member_count)
        user_stats = await test.get_user_stats(USER_ID)
        print(user_stats)
        member_stats = await test.get_member_stats(USER_ID, GUILD_ID)
        print(member_stats)
        member_activity = await test.get_member_activity(USER_ID, GUILD_ID)
        print(member_activity.voice_activity)
        print(member_activity.msg_activity)


        guild_activity = await test.get_guild_activity(GUILD_ID)
        print(guild_activity.msg_activity)
        print(guild_activity.voice_activity)
        guild_image = await test.get_guild_image(GUILD_ID)
        #print(guild_image)
        guild_image = await test.get_member_image(USER_ID, GUILD_ID)
        #print(guild_image)

    # await test.close()

asyncio.run(start())

member_count = api.get_member_count(GUILD_ID)
print(member_count)
user_stats = api.get_user_stats(USER_ID)
print(user_stats)
member_stats = api.get_member_stats(USER_ID, GUILD_ID)
print(member_stats)
member_activity = api.get_member_activity(USER_ID, GUILD_ID)
print(member_activity.voice_activity)
print(member_activity.msg_activity)


guild_activity = api.get_guild_activity(GUILD_ID)
print(guild_activity.msg_activity)
print(guild_activity.voice_activity)
