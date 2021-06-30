import discord
import requests
import json
import asyncio
import aiohttp
import io
from discord.ext import commands

with open('config.json') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix='fn.')
bot.remove_command('help')

async def fortnite_api_request(url: str, params: dict = {}) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.request(
                method='GET', url=f'https://fortnite-api.com/v2/{url}',
                params=params) as r:
            return await r.json()

@bot.event
async def on_ready():
    print("bot is ready")

@bot.command()
async def help(ctx):
    await ctx.send("map,item,stats,shop,br,creative,stw,cc")

@bot.command()
async def map(ctx, lang=config['lang']):
    data = requests.get(f'https://fortnite-api.com/v1/map?language={lang}')
    em = discord.Embed(title="フォートナイトのマップ", colour=0x6a5acd)
    em.set_image(url=data['data']['images']['pois'])
    em.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em)

@bot.command()
async def item(ctx, *, args=None):
    if args == None:
        em = discord.Embed(title="Error",description="検索したいアイテム名を打ってください。",color=0xff0000)
        await ctx.send(embed=em)
    else:
        response = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search/all?name={args}&matchMethod=starts&language=ja&searchLanguage={config["lang"]}').json()

        if response['status'] == 200:

            for item in response['data']:
                try:
                    item_set = item["set"]["value"]
                except:
                    item_set = 'このアイテムはセットではありません。'
                try:
                    item_introduction = item['introduction']['text']
                except:
                    item_introduction = 'データがありません。'

                embed = discord.Embed(title=item['type']['displayValue'],colour=0x6a5acd,timestamp=ctx.message.created_at)
                if item['images']['icon'] != None:
                    embed.set_thumbnail(url=item['images']['icon'])
                embed.add_field(name="アイテム名",value=f'{item["name"]}')
                embed.add_field(name="ID",value=f'{item["id"]}')
                embed.add_field(name="説明", value=f'{item["description"]}')
                embed.add_field(name="レアリティ", value=f'{item["rarity"]["displayValue"]}')
                embed.add_field(name="セット",value=f'{item_set}')
                embed.add_field(name="導入日",value=f'{item_introduction}')
                embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

        elif response['status'] == 400:
            error = response['error']
            embed = discord.Embed(title=':no_entry_sign:｜Error',description=f'``{error}``',color=0xff0000)
            embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        elif response['status'] == 404:
            error = response['error']
            embed = discord.Embed(title=':no_entry_sign:｜Error', description="アイテムが存在しませんでした。",color=0xff0000)
            embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

@bot.command()
async def stats(ctx, *, account = None):

    if account == None:

        embed = discord.Embed(title="ステータスを検索したいアカウント名を指定してください。",color=0xff0000)
        await ctx.send(embed=embed)
        return
    embed = discord.Embed(title="プレイヤーステータス",description="現在プレイヤーステータスを取得中、しばらくお待ち下さい...",colour=0x6a5acd)
    msg = await ctx.send(embed=embed)     
    response = requests.get(f'https://fortnite-api.com/v1/stats/br/v2?name={account}&image=all')
    if response.status_code == 200:
        
        embed = discord.Embed(title="プラットフォーム選択",description="プラットフォームを以下のリアクションから選んでください。",colour=0x6a5acd)
        await msg.edit(embed=embed)        
        await msg.add_reaction('⌨️')
        await msg.add_reaction('🎮')
        await msg.add_reaction('👆')
        def judge_reaction1(reaction,user):
            return reaction.message == msg and user == ctx.message.author and str(reaction.emoji) == "⌨️"
            
        def judge_reaction2(reaction,user):
            return reaction.message == msg and user == ctx.message.author and str(reaction.emoji) == "🎮"

        def judge_reaction3(reaction,user):
            return reaction.message == msg and user == ctx.message.author and str(reaction.emoji) == "👆"
        

        wait_reaction_task1 = asyncio.create_task(bot.wait_for("reaction_add",check=judge_reaction1),name="wait_reaction1")
        wait_reaction_task2 = asyncio.create_task(bot.wait_for("reaction_add",check=judge_reaction2),name="wait_reaction2")
        wait_reaction_task3 = asyncio.create_task(bot.wait_for("reaction_add",check=judge_reaction3),name="wait_reaction3")

        aws = {wait_reaction_task1, wait_reaction_task2, wait_reaction_task3}
        done, pending = await asyncio.wait(aws, return_when=asyncio.FIRST_COMPLETED)
        done_task_type = list(done)[0].get_name()

        if done_task_type == "wait_reaction1":
            await msg.clear_reactions()
            embed = discord.Embed(title="プレイヤーステータス",description="ステータス画像を取得中...",colour=0x6a5acd)
            await msg.edit(embed=embed)        
            response = requests.get(f'https://fortnite-api.com/v1/stats/br/v2?name={account}&image=keyboardMouse')

            if response.status_code == 200:

                embed = discord.Embed(title="プレイヤーステータス",colour=0x6a5acd)
                embed.set_image(url='attachment://stats.jpg')
                embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, file=discord.File(io.BytesIO(requests.get(response.json()['data']['image']).content), 'stats.jpg'))
                await msg.delete()

        elif done_task_type == "wait_reaction2":
            await msg.clear_reactions()
            embed = discord.Embed(title="プレイヤーステータス",description="ステータス画像を取得中...",colour=0x6a5acd)
            await msg.edit(embed=embed)         
            response = requests.get(f'https://fortnite-api.com/v1/stats/br/v2?name={account}&image=gamepad')

            if response.status_code == 200:

                embed = discord.Embed(title="プレイヤーステータス",colour=0x6a5acd)
                embed.set_image(url='attachment://stats.jpg')
                embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, file=discord.File(io.BytesIO(requests.get(response.json()['data']['image']).content), 'stats.jpg'))
                await msg.delete()

        elif done_task_type == "wait_reaction3":
            await msg.clear_reactions()
            embed = discord.Embed(title="プレイヤー統計",description="ステータス画像を取得中...",colour=0x6a5acd)
            await msg.edit(embed=embed)           
            response = requests.get(f'https://fortnite-api.com/v1/stats/br/v2?name={account}&image=touch')

            if response.status_code == 200:

                embed = discord.Embed(title="プレイヤーステータス",colour=0x6a5acd)
                embed.set_image(url='attachment://stats.jpg')
                embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, file=discord.File(io.BytesIO(requests.get(response.json()['data']['image']).content), 'stats.jpg'))
                await msg.delete()

    elif response.status_code == 404 or 400:

        embed = discord.Embed(description = "ユーザーが見つかりませんでした、プレイヤー名が間違えている場合があります。",color = 0xff0000,)
        await msg.edit(embed=embed)
    else:
        embed = discord.Embed(description = "データの取得に失敗しました、APIがダウンしている場合がありますので時間をおいてから再実行してみてください。",color = 0xff0000)
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await msg.edit(embed=embed)

@bot.command()
async def shop(ctx):
    
    response = requests.get('https://api.nitestats.com/v1/shop/image')

    if response.status_code == 200:

        embed = discord.Embed(title='Fortnite Item Shop',color=0x6a5acd)
        embed.set_image(url='attachment://shop.png')
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed, file=discord.File(fp=io.BytesIO(response.content), filename='shop.png'))
    else:
        embed = discord.Embed( description = '取得に失敗しました。',color = 0xff0000)
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

@bot.command()
async def br(ctx, *, lang=config['lang']):

    response = await fortnite_api_request(f'news/br?language={lang}')
    
    if response['status'] == 200:

        image = response['data']['image']
        embed = discord.Embed(title="バトルロワイヤルニュース")
        embed.set_image(url=image)
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif response['status'] == 400:
        embed = discord.Embed(title='取得に失敗しました、APIがダウンしている場合があります')
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    elif response['status'] == 404:
        embed = discord.Embed(title='ニュースが存在しません。')
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


@bot.command()
async def creative(ctx, lang=config['lang']):
    response = await fortnite_api_request(f'news/creative?language={lang}')
    
    if response['status'] == 200:

        image = response['data']['image']

        embed = discord.Embed(title="クリエイティブニュース")
        embed.set_image(url=image)
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif response['status'] == 400:
        embed = discord.Embed(title='取得に失敗しました、APIがダウンしている場合があります')
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    elif response['status'] == 404:
        embed = discord.Embed(title='ニュースが存在しません。')
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


@bot.command()
async def stw(ctx, lang=config['lang']):
    response = requests.get(f'https://api.peely.de/v1/stw/news?lang={lang if lang == None else lang}')

    if response.status_code == 200:

        img = response.json()['data']['image']
        embed = discord.Embed(
            title="世界を救えのニュース",
            color=0x6a5acd,
            timestamp=ctx.message.created_at
        )
        embed.set_image(url=img)
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif response['status'] == 400:
        embed = discord.Embed(title='取得に失敗しました、APIがダウンしている場合があります')
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    elif response['status'] == 404:
        embed = discord.Embed(title='ニュースが存在しません。')
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

@bot.command()
async def creatorcode(self, ctx, *, code=None):

    if code == None:

        embed = discord.Embed(
            description = "クリエイターコードを指定してください。",
            color = 0xff0000
        )
        await ctx.send(embed=embed)
        return

    response = requests.get(f'https://fortnite-api.com/v2/creatorcode?name={code}')

    if response.status_code == 200:

        geted = response.json()

        code = geted['data']['code']
        code_account = geted['data']['account']['name']
        code_account_id = geted['data']['account']['id']
        code_status = "アクティブ" if geted['data']['status'] == 'ACTIVE' else "アクティブでない" if geted['data']['status'] == 'INACTIVE' else "無効化" if geted['data']['status'] == 'DISABLED' else "不明"
        code_verified = "はい" if geted['data']['verified'] == True else "いいえ"


        embed = discord.Embed(
            title = "クリエイターコードの詳細",
            color = 0x6a5acd,
            timestamp = ctx.message.created_at
        )
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="コード", value=f'``{code}``')
        embed.add_field(name="アカウント", value=f'``{code_account}``')
        embed.add_field(name="アカウントID", value=f'``{code_account_id}``')
        embed.add_field(name="ステータス", value=f'``{code_status}``')
        embed.add_field(name="認証", value=f'``{code_verified}``')

        await ctx.send(embed=embed)
    elif response.status_code == 404 or 400:

        embed = discord.Embed(description = "ユーザーが見つかりませんでした、プレイヤー名が間違えている場合があります。",color = 0xff0000,)
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description = "データの取得に失敗しました、APIがダウンしている場合がありますので時間をおいてから再実行してみてください。",color = 0xff0000)
        embed.set_footer(text=f"コマンド実行者: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

        await ctx.send(embed=embed)

if __name__ == '__main__':
    bot.run(config['Token'])
