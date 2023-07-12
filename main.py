import os

import firebase_admin
from discord.ext.commands import UserConverter
from firebase_admin import credentials
from firebase_admin import db
import discord
import yfinance as yf
from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
cred = credentials.Certificate("/Users/admin/Desktop/discord/stockbot-88bdf-"
                               "firebase-adminsdk-xuahv-3da974a807.json")
firebase_admin.initialize_app(cred, {'databaseURL':
                                         'https://stockbot-88bdf-default-rtdb.'
                                         'firebaseio.com/'})
ref = db.reference("users")


def get_net_worth(user_id):
    total = 0
    user_ref = ref.child(user_id)
    total = total + int(user_ref.get()["money"])
    stock_dict = user_ref.child("stocks").get()
    for stock in stock_dict:
        stock_obj = yf.Ticker(stock)
        total += int(stock_dict[stock]) * int(stock_obj.info['currentPrice'])
    return total


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'hi':
        await message.channel.send("hello!")
        await message.channel.send(message.author)
        return

    if message.content.startswith("$info"):
        stock_code = message.content.split(" ", 1)[1].upper()
        stock = yf.Ticker(stock_code)
        embed = discord.Embed(title=stock.info['longName'],
                              url=stock.info['website'],
                              description="Current price: "
                                          + str(stock.info['currentPrice']) +
                                          "\nMarket cap: " + str(
                                  stock.info['marketCap']) +
                                          "\nEarnings per share: " +
                                          str(stock.info['forwardEps']) +
                                          "\nDividend yield: " +
                                          str(stock.info['dividendYield']) +
                                          "\nBeta value: " + str(
                                  stock.info['beta']),
                              color=0x00ff00)
        embed.set_image(url=stock.info['logo_url'])
        await message.channel.send(embed=embed)
        return

    if message.content.startswith("$create"):
        user_id = str(message.author.id)
        snapshot = ref.get()
        if user_id in snapshot.keys():
            await message.channel.send("User already created!")
        else:
            newref = ref.child(user_id)
            newref.set({"money": 100000})
            await message.channel.send("User successfully created!")

    if message.content.startswith("$money") or message.content.startswith(
            "$bal"):
        user_id = str(message.author.id)
        snapshot = ref.get()
        if user_id in snapshot.keys():
            newref = ref.child(user_id)
            user = newref.get()
            await message.channel.send("User has $" + str(user['money']))
        else:
            await message.channel.send("No user found.")

    if message.content.startswith("$buy"):
        cmd = message.content.split()
        user_id = str(message.author.id)
        snapshot = ref.get()
        stock_code = cmd[1].upper()
        amount = cmd[2]
        stock = yf.Ticker(stock_code)
        if user_id not in snapshot.keys():
            await message.channel.send("User not found.")
            return
        else:
            newref = ref.child(user_id)
            user = newref.get()
            if user['money'] < int(amount) * int(stock.info['currentPrice']):
                await message.channel.send("Not enough money!")
                return
            if 'stocks' not in user.keys():
                newref.update({"stocks": {stock_code: int(amount)}})
            else:
                user_stocks = newref.child("stocks")
                if stock_code not in user_stocks.get().keys():
                    user_stocks.update({stock_code: int(amount)})
                else:
                    new_amt = int(user_stocks.get()[stock_code]) + int(amount)
                    user_stocks.update({stock_code: new_amt})
            new_money = (int(user['money']) - int(amount) * \
                         int(stock.info['currentPrice']))
            newref.update({"money": new_money})
        await message.channel.send("Stock successfully purchased!")

    if message.content.startswith("$sell"):
        cmd = message.content.split()
        user_id = str(message.author.id)
        snapshot = ref.get()
        stock_code = cmd[1].upper()
        amount = cmd[2]
        stock = yf.Ticker(stock_code)
        if user_id not in snapshot.keys():
            await message.channel.send("User not found.")
            return
        newref = ref.child(user_id)
        user = newref.get()
        if 'stocks' not in user.keys():
            await message.channel.send("You do not have that stock!")
        else:
            user_stocks = newref.child("stocks")
            if stock_code not in user_stocks.get().keys():
                await message.channel.send("You do not have that stock!")
            else:
                amount_owned = user_stocks.get()[stock_code]
                if int(amount) > int(amount_owned):
                    await message.channel.send("You do not have enough!")
                    return
                else:
                    new_amt = int(amount_owned) - int(amount)
                    user_stocks.update({stock_code: new_amt})
                    new_money = (int(user['money']) + int(amount) * \
                                 int(stock.info['currentPrice']))
                    newref.update({"money": new_money})
                    await message.channel.send("Stock successfully sold!")
                    return

    if message.content.startswith("$profile"):
        cmd = message.content.split()
        if len(cmd) == 1:
            user_id = str(message.author.id)
        elif len(cmd) == 2:
            name = cmd[1].split("#")
            members = message.guild.members
            print(members)
            user_in_guild = False
            for member in members:
                if member.name == name[0] and member.discriminator == name[1]:
                    user_id = str(member.id)
                    user_in_guild = True
            if not user_in_guild:
                await message.channel.send("User not in guild!")
                return
        else:
            await message.channel.send("Invalid argument!")
            return
        stock_ref = ref.child(user_id).child('stocks')
        stock_dict = stock_ref.order_by_key().get()
        bal = ref.child(user_id).get()['money']
        stock_str = "Balance: " + str(bal) + "\n"
        net_worth = str(get_net_worth(user_id))
        stock_str = stock_str + "Net worth: " + net_worth + "\n\n"
        for key in stock_dict:
            stock_str = stock_str + key + ": " + str(stock_dict[key]) + '\n'
        embed = discord.Embed(title=message.author, description=stock_str)
        await message.channel.send(embed=embed)

    if message.content.startswith("$help"):
        await message.channel.send(
            "$create to create new account with 100000\n" +
            "$buy <stock code> <amount> purchases the amount of"
            + " stock at current price for stock code\n"
            + "$sell <stock code> <amount> will sell amount of "
            + "stock at current price for stock code\n"
            + "$profile to look at your stocks and balance\n"
            + "$money to look at your current balance")


client.run(TOKEN)
