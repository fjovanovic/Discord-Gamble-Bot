import os
import discord
import asyncio
from discord.ext import commands
from replit import db
from keep_alive import keep_alive
import random

client = commands.Bot(command_prefix='$')
bj_players = []


def add_money(user, amount):
    previous_balance = db[user]
    db[user] = previous_balance + amount


def sub_money(user, amount):
    previous_balance = db[user]
    db[user] = previous_balance - amount


@client.event
async def on_ready():
    print(f'You have logged in as {client.user}')


@client.command()
async def coinflip(ctx, *args):
    if len(args) != 2:
        await ctx.send('Wrong call. Make sure you use the right call. ($coinflip amount head/tails, eg. $coinflip 10.2 tails)')
        return

    image = 'https://i.postimg.cc/NfxGwWzm/coinflip.png'
    user_id = str(ctx.author.id)
    user_name = str(ctx.author)
    if user_id not in db.keys():
        await ctx.send('Your balance is 0. Please make a deposit.')
        return
    try:
        amount = float(args[0])
        balance = float(db[user_id])
        if amount > 500 or amount < 10:
            await ctx.send('Wrong call. Minimum bet is 10 and maximum bet is 500')
            return
        if amount > balance:
            await ctx.send('Wrong call. Make sure to put amount that is larger than your balance.')
            return
    except:
        await ctx.send('Wrong call. Make sure you use the right call. ($coinflip amount head/tails, eg. $coinflip 10.2 tails)')
        return
    bet = args[1]
    if bet != 'head' and bet != 'tails':
        await ctx.send('Wrong call. Make sure you use the right call. ($coinflip amount head/tails, eg. $coinflip 10.2 tails)')
        return

    answer = random.choice(['head', 'tails'])
    if answer == bet:
        result = True 
    else:
        result = False

    my_embed = discord.Embed(
        colour = discord.Colour.red() 
    )
    if result:
        my_embed.colour = discord.Colour.green() 
    
    my_embed.set_author(name='Coinflip ' + user_name, icon_url=image)
    if result:
        my_embed.add_field(name='You won', value=db['currency'] + str(round(amount)) + ' has been added to your balance', inline=False)
        add_money(user_id, amount)
    else:
        my_embed.add_field(name='You lost', value=db['currency'] + str(round(amount)) + ' has been removed to your balance', inline=False)
        sub_money(user_id, amount)
    my_embed.add_field(name='Coin landed on', value=answer, inline=False)
    my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

    await ctx.send(embed=my_embed)
    return
    

@client.command()
async def dice(ctx, *args):
    if len(args) != 2:
        await ctx.send('Wrong call. Make sure you use the right call. ($dice amount num[2,98], eg. $dice 10.2 45)')
        return

    image = 'https://i.postimg.cc/cJvdw64B/dice.png'
    user_id = str(ctx.author.id)
    user_name = str(ctx.author)
    if user_id not in db.keys():
        await ctx.send('Your balance is 0. Please make a deposit.')
        return
    try:
        amount = float(args[0])
        balance = float(db[user_id])
        if amount > 500 or amount < 10:
            await ctx.send('Wrong call. Minimum bet is 10 and maximum bet is 500')
            return
        if amount > balance:
            await ctx.send('Wrong call. Make sure to put amount that is larger than your balance.')
            return
    except:
        await ctx.send('Wrong call. Make sure you use the right call. ($dice amount num[2,98], eg. $dice 10.2 45)')
        return

    try:
        bet = int(args[1])
        if bet < 2 or bet > 98:
            await ctx.send('Wrong call. Make sure to choose number between 2 and 98.')
            return
    except:
        await ctx.send('Wrong call. Make sure you use the right call. ($dice amount num[2,98], eg. $dice 10.2 45)')
        return

    answer_number = round(random.uniform(0.01, 99.99), 2)

    if float(bet) > answer_number:
        my_embed = discord.Embed(
            colour = discord.Colour.red() 
        )
        
        my_embed.set_author(name='Dice ' + user_name, icon_url=image)
        my_embed.add_field(name='You lost', value=db['currency'] + str(round(amount)) + ' has been removed from your balance', inline=False)
        sub_money(user_id, amount)
        my_embed.add_field(name='Dice number', value=str(answer_number), inline=False)
        my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

        await ctx.send(embed=my_embed)   
        return   
    else: 
        multis = [1.0102, 1.0206, 1.0313, 1.0421, 1.0532, 1.0645, 1.0761, 1.0879, 1.1, 1.1124, 1.1250, 1.1379, 1.1512, 1.1647, 1.1786, 1.1928, 1.2073, 1.2222, 1.2375, 1.2532, 1.2692, 1.2857, 1.3026, 1.3200, 1.3378, 1.3562, 1.3750, 1.3944, 1.4143, 1.4348, 1.4559, 1.4776, 1.5000, 1.5231, 1.5469, 1.5714, 1.5968, 1.6230, 1.6500, 1.6780, 1.7069, 1.7368, 1.7679, 1.8000, 1.8333, 1.8679, 1.9038, 1.9412, 1.9800, 2.0204, 2.0625, 2.1064, 2.1522, 2.2000, 2.2500, 2.3023, 2.3571, 2.4146, 2.4750, 2.5385, 2.6053, 2.6757, 2.7500, 2.8286, 2.9118, 3.0000, 3.0938, 3.1935, 3.3000, 3.4138, 3.5357, 3.6667, 3.8077, 3.9600, 4.1250, 4.3043, 4.5000, 4.7143, 4.9500, 5.2105, 5.5000, 5.8235, 6.1875, 6.6000, 7.0714, 7.6154, 8.2500, 9.0000, 9.9000, 11.0000, 12.3750, 14.1429, 16.5000, 19.8000, 24.7500, 33.0000, 49.5000]
        my_multi = multis[bet - 2]

        val = float(amount) * my_multi
        won_value = round(val, 2)
        real_won_value = round((won_value - amount), 2)
    
        my_embed = discord.Embed(
            colour = discord.Colour.green() 
        )
        
        my_embed.set_author(name='Dice ' + user_name, icon_url=image)
        my_embed.add_field(name='You won', value=db['currency'] + str(round(real_won_value)) + ' has been added to your balance', inline=False)
        sub_money(user_id, amount)
        add_money(user_id, won_value)
        my_embed.add_field(name='Dice number', value=str(answer_number), inline=False)
        my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

        await ctx.send(embed=my_embed) 
        return


@client.command() 
async def roulette(ctx, *args):
    if len(args) != 2:
        await ctx.send('Wrong call. Make sure you use the right call. ($roulette amount black/red or $roulette amount number[0,36], eg. $roulette 10.2 black/red) or ($roulette 10.2 31)')
        return
    
    image = 'https://i.postimg.cc/bYQKQ80n/Item-Sprites-5.png'
    user_id = str(ctx.author.id)
    user_name = str(ctx.author)
    if user_id not in db.keys():
        await ctx.send('Your balance is 0. Please make a deposit.')
        return
    try:
        amount = float(args[0])
        balance = float(db[user_id])
        if amount > 500 or amount < 10:
            await ctx.send('Wrong call. Minimum bet is 10 and maximum bet is 500')
            return
        if amount > balance:
            await ctx.send('Wrong call. Make sure to put amount that is larger than your balance.')
            return
    except:
        await ctx.send('Wrong call. Make sure you use the right call. ($roulette amount black/red or $roulette amount number[0,36], eg. $roulette 10.2 black/red) or ($roulette 10.2 31)')
        return

    answer_number = random.randrange(0, 37)

    if 'black' in args or 'red' in args:
        bet = args[1].lower()
        color = ''
        result = False

        if answer_number == 0:
            color = 'green'
        elif answer_number % 2 == 0:
            color = 'red'
        else:
            color = 'black'

        if bet == color:
            result = True

        my_embed = discord.Embed(
            colour = discord.Colour.red() 
        )
        
        my_embed.set_author(name='Roulette ' + user_name, icon_url=image)
        if result:
            my_embed.colour = discord.Colour.green()
            won_value = 2 * amount
            my_embed.add_field(name='You won', value=db['currency'] + str(round(amount)) + ' has been added to your balance', inline=False)
            add_money(user_id, amount)
        else:
            my_embed.add_field(name='You lost', value=db['currency'] + str(round(amount)) + ' has been removed from your balance', inline=False)
            sub_money(user_id, amount)
        my_embed.add_field(name='Ball landed in', value=str(answer_number) + ' ' + color, inline=False)
        my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

        await ctx.send(embed=my_embed)
        return
    else:
        try:
            bet = int(args[1])
        except:
            await ctx.send('Wrond call. Make sure to put number in range (0,36). ($roulette 10 34)')
            return

        if answer_number == 0:
            color = 'green'
        elif answer_number % 2 == 0:
            color = 'red'
        else:
            color = 'black'

        if answer_number != bet:
            my_embed = discord.Embed(
                colour = discord.Colour.red() 
            )
            
            my_embed.set_author(name='Roulette ' + user_name, icon_url=image)
            my_embed.add_field(name='You lost', value=db['currency'] + str(round(amount)) + ' has been removed from your balance', inline=False)
            sub_money(user_id, amount)
            my_embed.add_field(name='Ball landed in', value=str(answer_number) + ' ' + color, inline=False)
            my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

            await ctx.send(embed=my_embed)
            return
        else:
            won_value = float(amount) * 36
            my_embed = discord.Embed(
                colour = discord.Colour.green() 
            )
            
            my_embed.set_author(name='Roulette ' + user_name, icon_url=image)
            my_embed.add_field(name='You won', value=db['currency'] + str(round(won_value)) + ' has been added to your balance', inline=False)
            sub_money(user_id, amount)
            add_money(user_id, won_value)
            my_embed.add_field(name='Roulette', value=str(answer_number), inline=False)
            my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

            await ctx.send(embed=my_embed)  
            return         


@client.command() 
async def bj(ctx, *args):
    user_id = str(ctx.author.id)
    if user_id in bj_players:
        await ctx.send('You are already playing.')
        return

    bj_players.append(user_id)

    if len(args) != 1:
        await ctx.send('Wrong call. Make sure to use the right call. ($bj amount, eg. $bj 20)')
        return
    
    image = 'https://i.postimg.cc/N0GZH0Bf/bj.png'
    user_name = str(ctx.author)
    if user_id not in db.keys():
        await ctx.send('Your balance is 0. Please make a deposit.')
        return
    try:
        amount = float(args[0])
        balance = float(db[user_id])
        if amount > 500 or amount < 10:
            await ctx.send('Wrong call. Minimum bet is 10 and maximum bet is 500')
            return
        if amount > balance:
            await ctx.send('Wrong call. Make sure to put amount that is larger than your balance.')
            return
    except:
        await ctx.send('Wrong call. Make sure to use the right call. ($bj amount, eg. $bj 20)')
        return

    p_cards = []
    p_cards_str = ''
    p_count = 0
    d_cards = []
    d_cards_str = ''
    d_count = 0

    cards = []
    for i in range(1, 15):
        for j in range(0, 8):
            if i == 11:
                pass
            elif i == 12:
                cards.append('J')
            elif i == 13:
                cards.append('Q')
            elif i == 14:
                cards.append('K')
            else:
                cards.append(i)
    not_bust = True
    i = 104
    p_i = len(p_cards)
    d_i = len(d_cards)
    random.shuffle(cards)
    index = random.randrange(0, i)
    p_cards.append(cards[index])
    p_cards_str += str(cards[index]) + ' '
    if cards[index] == 'K' or cards[index] == 'Q' or cards[index] == 'J' or cards[index] == 1:
        p_count += 10
    else:
        p_count += cards[index]
    cards.remove(p_cards[p_i - 1])
    i -= 1
    p_i += 1
    index = random.randrange(0, i)
    d_cards.append(cards[index])
    d_cards_str += str(cards[index]) + ' '
    if cards[index] == 'K' or cards[index] == 'Q' or cards[index] == 'J' or cards[index] == 1:
        d_count += 10
    else:
        d_count += cards[index]
    cards.remove(d_cards[d_i - 1])
    i -= 1
    d_i += 1
    index = random.randrange(0, i)
    p_cards.append(cards[index])
    p_cards_str += str(cards[index]) + ' '
    if cards[index] == 'K' or cards[index] == 'Q' or cards[index] == 'J' or cards[index] == 1:
        p_count += 10
    else:
        p_count += cards[index]
    cards.remove(p_cards[p_i - 1])
    i -= 1
    p_i += 1

    my_embed = discord.Embed(
        colour = discord.Colour.gold() 
    )

    my_embed.set_author(name='Blackjack ' + user_name, icon_url=image)
    my_embed.add_field(name='Your hand', value=p_cards_str + '\nCount: ' + str(p_count), inline=True)
    my_embed.add_field(name='Dealer hand', value=d_cards_str + '\nCount: ' + str(d_count), inline=True)
    my_embed.add_field(name='Rules', value='Type "hit" or "stand" in the chat, you have 1 minute.', inline=False)

    await ctx.send(embed=my_embed)

    while not_bust:
        try:
            message = await client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send(user_name + ' 1 minute passed, you lost this bet.')
            sub_money(user_id, amount)  
            bj_players.remove(user_id)         
            return
        
        else:
            if message.content.lower() == 'hit':
                index = random.randrange(0, i)
                p_cards.append(cards[index])
                p_cards_str += str(cards[index]) + ' '
                if cards[index] == 'K' or cards[index] == 'Q' or cards[index] == 'J' or cards[index] == 1:
                    p_count += 10
                else:
                    p_count += cards[index]
                cards.remove(p_cards[p_i - 1])
                i -= 1
                p_i += 1
                my_embed = discord.Embed(
                    colour = discord.Colour.gold() 
                )
                my_embed.set_author(name='Blackjack ' + user_name, icon_url=image)
                my_embed.add_field(name='Your hand', value=p_cards_str + '\nCount: ' + str(p_count), inline=True)
                my_embed.add_field(name='Dealer hand', value=d_cards_str + '\nCount: ' + str(d_count), inline=True)
                my_embed.add_field(name='Rules', value='Type "hit" or "stand" in the chat, you have 1 minute.', inline=False)

                await ctx.send(embed=my_embed)

                if p_count > 21:
                    not_bust = False
                    my_embed = discord.Embed(
                        colour = discord.Colour.red() 
                    )
            
                    my_embed.set_author(name='Blackjack ' + user_name, icon_url=image)
                    my_embed.add_field(name='You lost', value=db['currency'] + str(round(amount)) + ' has been removed from your balance', inline=False)
                    sub_money(user_id, amount)
                    my_embed.add_field(name='Your hand', value=p_cards_str + '\nCount: ' + str(p_count), inline=True)
                    my_embed.add_field(name='Dealer hand', value=d_cards_str + '\nCount: ' + str(d_count), inline=True)
                    my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

                    await ctx.send(embed=my_embed)
                    bj_players.remove(user_id)
                    return
            elif message.content.lower() == 'stand':
                while d_count < 17:
                    index = random.randrange(0, i)
                    d_cards.append(cards[index])
                    d_cards_str += str(cards[index]) + ' '
                    if cards[index] == 'K' or cards[index] == 'Q' or cards[index] == 'J' or cards[index] == 1:
                        d_count += 10
                    else:
                        d_count += cards[index]
                    cards.remove(d_cards[d_i - 1])
                    i -= 1
                    d_i += 1
                if d_count > 21:
                    my_embed = discord.Embed(
                        colour = discord.Colour.green() 
                    )
            
                    my_embed.set_author(name='Blackjack ' + user_name, icon_url=image)
                    my_embed.add_field(name='You won(Dealer bust)', value=db['currency'] + str(round(amount)) + ' has been added to your balance', inline=False)
                    add_money(user_id, amount)
                    my_embed.add_field(name='Your hand', value=p_cards_str + '\nCount: ' + str(p_count), inline=True)
                    my_embed.add_field(name='Dealer hand', value=d_cards_str + '\nCount: ' + str(d_count), inline=True)
                    my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

                    await ctx.send(embed=my_embed)
                    bj_players.remove(user_id)
                    return
                elif d_count > p_count:
                    my_embed = discord.Embed(
                        colour = discord.Colour.red() 
                    )
            
                    my_embed.set_author(name='Blackjack ' + user_name, icon_url=image)
                    my_embed.add_field(name='You lost', value=db['currency'] + str(round(amount)) + ' has been removed from your balance', inline=False)
                    sub_money(user_id, amount)
                    my_embed.add_field(name='Your hand', value=p_cards_str + '\nCount: ' + str(p_count), inline=True)
                    my_embed.add_field(name='Dealer hand', value=d_cards_str + '\nCount: ' + str(d_count), inline=True)
                    my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

                    await ctx.send(embed=my_embed)
                    bj_players.remove(user_id)
                    return
                elif d_count < p_count:
                    my_embed = discord.Embed(
                        colour = discord.Colour.green() 
                    )
            
                    my_embed.set_author(name='Blackjack ' + user_name, icon_url=image)
                    my_embed.add_field(name='You won', value=db['currency'] + str(round(amount)) + ' has been added to your balance', inline=False)
                    add_money(user_id, amount)
                    my_embed.add_field(name='Your hand', value=p_cards_str + '\nCount: ' + str(p_count), inline=True)
                    my_embed.add_field(name='Dealer hand', value=d_cards_str + '\nCount: ' + str(d_count), inline=True)
                    my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

                    await ctx.send(embed=my_embed)
                    bj_players.remove(user_id)
                    return
                elif d_count == p_count:
                    my_embed = discord.Embed(
                        colour = discord.Colour.greyple() 
                    )
            
                    my_embed.set_author(name='Blackjack ' + user_name, icon_url=image)
                    my_embed.add_field(name='Push', value=db['currency'] + str(round(amount)) + ' has been given back to your balance', inline=False)
                    my_embed.add_field(name='Your hand', value=p_cards_str + '\nCount: ' + str(p_count), inline=True)
                    my_embed.add_field(name='Dealer hand', value=d_cards_str + '\nCount: ' + str(d_count), inline=True)
                    my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

                    await ctx.send(embed=my_embed)
                    bj_players.remove(user_id)
                    return

            else:
                await ctx.send('Please type "hit" or "stand" in order to continue')
    return


@client.command()
async def crash(ctx, *args):
    if len(args) != 2:
        await ctx.send('Wrong call. Make sure to use the right call. ($crash amount cashout[1.01,99], eg. $crash 10.2 1.20')
        return      
    
    image = 'https://i.postimg.cc/SNmqVgxs/crash.png'
    user_id = str(ctx.author.id)
    user_name = str(ctx.author)
    if user_id not in db.keys():
        await ctx.send('Your balance is 0. Please make a deposit.')
        return
    try:
        amount = float(args[0])
        balance = float(db[user_id])
        if amount > 500 or amount < 10:
            await ctx.send('Wrong call. Minimum bet is 10 and maximum bet is 500')
            return
        if amount > balance:
            await ctx.send('Wrong call. Make sure to put amount that is larger than your balance.')
            return
    except:
        await ctx.send('Wrong call. Make sure to use the right call. ($crash amount cashout[1.01,99], eg. $crash 10.2 1.20')
        return

    try:
        cashout = float(args[1])
        if cashout < 1.01 or cashout > 99.0:
            await ctx.send('Wrong call. Make sure to use the right call. ($crash amount cashout[1.01,99], eg. $crash 10.2 1.20')
            return 
    except:
        await ctx.send('Wrong call. Make sure to use the right call. ($crash amount cashout[1.01,99], eg. $crash 10.2 1.20')
        return 

    multipliers = []

    def float_range(start, stop, step, copies):
        while start < stop:
            for i in range (0, copies):
                num = start
                multipliers.append(round(num, 2))
                num += step
            start += step

    float_range(1.00, 1.01, 0.01, 350)
    float_range(1.01, 1.10, 0.01, 320)
    float_range(1.10, 1.25, 0.01, 300)
    float_range(1.25, 1.50, 0.01, 5)
    float_range(1.50, 2.00, 0.01, 2)
    float_range(2.0, 30.01, 0.01, 1)
    
    length = len(multipliers) - 1
    i = random.randint(0, length)
    random.shuffle(multipliers)
    multi = multipliers[i]

    if multi >= cashout:
        won_value = amount * cashout - amount 
        my_embed = discord.Embed(
            colour = discord.Colour.green() 
        )
        
        my_embed.set_author(name='Crash ' + str(user_name), icon_url=image)
        my_embed.add_field(name='You won', value=db['currency'] + str(round(won_value)) + ' has been added to your balance', inline=False)
        add_money(user_id, won_value)
        my_embed.add_field(name='Multi', value=str(round(multi,2)), inline=False)
        my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

        await ctx.send(embed=my_embed)  
        return 
    else:
        my_embed = discord.Embed(
            colour = discord.Colour.red() 
        )
        
        my_embed.set_author(name='Crash', icon_url=image)
        my_embed.add_field(name='You lost', value=db['currency'] + str(round(amount)) + ' has been removed from your balance', inline=False)
        sub_money(user_id, amount)
        my_embed.add_field(name='Multi', value=str(round(multi,2)), inline=False)
        my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

        await ctx.send(embed=my_embed)
        return


@client.command()
async def gambleinfo(ctx, *args):
    if len(args) != 0:
        await ctx.send('Wrong call. Make sure to call info by $gambleinfo')
        return 
    
    image = 'https://i.postimg.cc/Sx6gVbD2/all-other.png'
    response_commands = '$coinflip amount head/tails\n' + '$dice amount num\n' + '$roulette amount black/red\n' + '$roulette amount num\n' + '$bj amount\n' + '$crash amount cashout' + '$bal\n'
    response_examples = '$coinflip 10 head\n' + '$dice 100 30\n' + '$roulette 100 black\n' + '$roulette 10 34\n' + '$bj 100\n' + '$crash 10.2 1.3' + '$bal\n'

    my_embed = discord.Embed(
        colour = discord.Colour.gold() 
    )
    
    my_embed.set_author(name='Gamble info', icon_url=image)
    my_embed.add_field(name='Command', value=response_commands, inline=True)
    my_embed.add_field(name='Example', value=response_examples, inline=True)

    await ctx.send(embed=my_embed)
    return


@client.command()
@commands.has_permissions(administrator=True)
async def admincommands(ctx, *args):
    if len(args) != 0:
        await ctx.send('Wrong call. Make sure to call info by $admincommands')
        return    

    image = 'https://i.postimg.cc/Sx6gVbD2/all-other.png'
    response_admin_commands = '$setcurrency emoji\n' + '$removeold\n' + '$addmoney amount @username\n' + '$submoney amount @username\n' + '$removebal @username\n' + '$playerbal @username'
    response_admin_examples = '$setcurrency :dollar\n' + '$removeold\n' + '$addmoney 100 @Apex\n' + '$submoney 100 @Apex\n' + '$removebal @Apex\n' + '$playerbal @Apex'

    my_embed = discord.Embed(
        colour = discord.Colour.gold() 
    )
    
    my_embed.set_author(name='Gamble info admin', icon_url=image)
    my_embed.add_field(name='Admin commands', value=response_admin_commands, inline=True)
    my_embed.add_field(name='Examples', value=response_admin_examples, inline=True)

    await ctx.send(embed=my_embed)
    return


@client.command()
@commands.has_permissions(administrator=True)
async def setcurrency(ctx, *args):
    db['currency'] = str(args[0])
    return

@client.command()
@commands.has_permissions(administrator=True)
async def removeold(ctx, *args):
    if len(args) != 0:
        await ctx.send('Wrong call.Make sure to use the right call. ($removeold)')
        return
    for i in db.keys():
        if i == 'currency':
            pass
        elif float(db[i]) < 1:
            del db[i]


@client.command()
@commands.has_permissions(administrator=True)
async def addmoney(ctx, *args):
    if len(args) != 2:
        await ctx.send('Wrong call. Make sure to use the right call. ($addmoney amount @username')
        return
    try:
        amount = float(args[0])
        if amount <= 0:
            await ctx.send('Wrong call. Make sure that you provided correct amount.')
            return
    except:
        await ctx.send('Wrong call. Make sure that you provided correct amount.')
        return

    image = 'https://i.postimg.cc/Sx6gVbD2/all-other.png'
    user_id = ''
    for s in args[1]:
        if s.isdigit():
            user_id += str(s)
    user_name = await client.fetch_user(int(user_id))
    if user_id in db.keys():
        previous_amount = db[user_id] 
    else:
        previous_amount = 0
    db[user_id] = previous_amount + amount

    my_embed = discord.Embed(
        colour = discord.Colour.gold() 
    )
    
    my_embed.set_author(name='Success ' + str(user_name), icon_url=image)
    my_embed.add_field(name='Previous balance', value=db['currency'] + str(round(previous_amount)), inline=False)
    my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

    await ctx.send(embed=my_embed)
    return


@client.command()
@commands.has_permissions(administrator=True)
async def submoney(ctx, *args):
    if len(args) != 2:
        await ctx.send('Wrong call. Make sure to use the right call. ($submoney amount @username')
        return
    try:
        amount = float(args[0])
        if amount <= 0:
            await ctx.send('Wrong call. Make sure that you provided correct amount.')
            return
    except:
        await ctx.send('Wrong call. Make sure that you provided correct amount.')
        return

    image = 'https://i.postimg.cc/Sx6gVbD2/all-other.png'
    user_id = ''
    for s in args[1]:
        if s.isdigit():
            user_id += str(s)
    user_name = await client.fetch_user(int(user_id))
    if user_id in db.keys():
        previous_amount = db[user_id] 
        db[user_id] = previous_amount - amount
        if db[user_id] < 0:
            db[user_id] = 0
    else:
        previous_amount = 0 
        db[user_id] = 0

    my_embed = discord.Embed(
        colour = discord.Colour.gold() 
    )
    
    my_embed.set_author(name='Success ' + str(user_name), icon_url=image)
    my_embed.add_field(name='Previous balance', value=db['currency'] + str(round(previous_amount)), inline=False)
    my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

    await ctx.send(embed=my_embed)
    return


@client.command()
async def bal(ctx, *args):
    if len(args) != 0:
        await ctx.send('Wrong call. Make sure to use command in the right way. ($bal)')
        return

    image = 'https://i.postimg.cc/Sx6gVbD2/all-other.png'
    user_id = str(ctx.author.id)
    user_name = str(ctx.author)
    if user_id not in db.keys():
        balance = 0
    else:
        balance = db[user_id]

    my_embed = discord.Embed(
        colour = discord.Colour.gold() 
    )
    
    my_embed.set_author(name=user_name, icon_url=image)
    my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(balance)), inline=False)

    await ctx.send(embed=my_embed)
    return


@client.command()
@commands.has_permissions(administrator=True)
async def removebal(ctx, *args):
    if len(args) != 1:
        await ctx.send('Wrong call. Make sure to use the right call. ($removebal @username')
        return

    image = 'https://i.postimg.cc/Sx6gVbD2/all-other.png'
    user_id = ''
    for s in args[0]:
        if s.isdigit():
            user_id += str(s)
    user_name = await client.fetch_user(int(user_id))
    if user_id in db.keys():
        previous_amount = db[user_id]
    else:
        previous_amount = 0

    db[user_id] = 0

    my_embed = discord.Embed(
        colour = discord.Colour.gold() 
    )
    
    my_embed.set_author(name='Success ' + str(user_name), icon_url=image)
    my_embed.add_field(name='Previous balance', value=db['currency'] + str(round(previous_amount)), inline=False)
    my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(db[user_id])), inline=False)

    await ctx.send(embed=my_embed)
    return


@client.command()
@commands.has_permissions(administrator=True)
async def list(ctx, *args):
    for i in db.keys():
        print(str(i) + ' ' + str(db[i]))
    return


@client.command()
@commands.has_permissions(administrator=True)
async def playerbal(ctx, *args):
    if len(args) != 1:
        await ctx.send('Wrong call. Make sure to use the right call. ($playerbal @username')
        return

    image = 'https://i.postimg.cc/Sx6gVbD2/all-other.png'
    user_id = ''
    for s in args[0]:
        if s.isdigit():
            user_id += str(s)
    user_name = await client.fetch_user(int(user_id))
    if user_id not in db.keys():
        balance = 0
    else:
        balance = db[user_id]
    try:
        user_name = await client.fetch_user(user_id)
    except:
        await ctx.send('Couldn\'t find user.')
        return

    my_embed = discord.Embed(
        colour = discord.Colour.gold() 
    )
    
    my_embed.set_author(name=user_name, icon_url=image)
    my_embed.add_field(name='Your current balance', value=db['currency'] + str(round(balance)), inline=False)

    await ctx.send(embed=my_embed)
    return


@client.command()
@commands.has_permissions(administrator=True)
async def custom(ctx, *args):
    l = len(args)
    i = 0
    mes = ''
    while l > 0:
        mes += str(args[i]) + ' '
        print(mes)
        l -= 1
        i += 1
    my_embed = discord.Embed(
        colour = discord.Colour.gold() 
    )
    
    my_embed.add_field(name='Announcement', value=mes, inline=False)

    await ctx.send(embed=my_embed)
    return


TOKEN = os.environ['TOKEN_SECRET']
keep_alive()
client.run(TOKEN)