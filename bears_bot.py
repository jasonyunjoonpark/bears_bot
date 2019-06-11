############################################################################
#                                                                          #
#   Script: bears_bot.py                                                   #
#   Written by: Jason Park                                                 #
#   Version: 1.0                                                           #
#   06/10/19                                                               #
#                                                                          #
#   Bears bot that can be called to fetch NWA player rankings from         #
#   Braacket.com or update user role based on their ranking on             #
#   Braacket.com.                                                          #
#                                                                          #
#   Bot command examples:                                                  #
#   .rank wineland                                                         #
#   .updaterole wineland                                                   #
#                                                                          #
############################################################################

###############################
#  Imports                    #
###############################
from config import *
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import re

#Instantiate bot
bot = commands.Bot(command_prefix = '.')

###############################
#  Bot Event Listeners        #
###############################

@bot.event
async def on_ready():
    print('Bot is online.')
    
@bot.event
async def on_member_join(member):
    print('')

@bot.event
async def on_member_remove(member):
    print('')

###############################
#  Bot Commands               #
###############################

@bot.command(aliases = ['rank'])
async def get_rank(ctx, *, player):
    try:
        #Get html
        request = requests.get('https://braacket.com/league/NWAUltimate/player/' + player)
        print('https://braacket.com/league/NWAUltimate/player/' + player)
        soup = BeautifulSoup(request.text, 'html.parser')

        #Parse values
        name = ''
        rank = 0
        points = 0

        #Get name
        name = soup.select('h4.ellipsis')[0].get_text().strip()
        print(name)

        print('Getting rank')
        #Get rank
        ranking_info = soup.select('section div.row div.col-lg-6 div.panel.panel-default.my-box-shadow div.panel-body div.my-dashboard-values-main')[0].stripped_strings
        ranking_info = [text for text in ranking_info]
        rank = int(ranking_info[0])

        #Get points
        points_info = soup.select('section div.row div.col-lg-6 div.panel.panel-default.my-box-shadow div.panel-body div.my-dashboard-values-sub div')

        await ctx.send('Player: ' + name + '\n' + 'Rank: ' + str(rank) + '\n' + 'Points: ' + re.sub('[^0-9]','', str(points_info[1])))
    except:
        await ctx.send('Player input error. Cannot find player.')

@bot.command(aliases = ['updaterole'], pass_context = True)
async def update_role(ctx, *, player):
    try:
        player = player.lower()
        member = ctx.message.author
        top_10 = discord.utils.get(member.guild.roles, name = 'Top 10')
        top_25 = discord.utils.get(member.guild.roles, name = 'Top 25')
        top_50 = discord.utils.get(member.guild.roles, name = 'Top 50')
        top_100 = discord.utils.get(member.guild.roles, name = 'Top 100')


        #Check if sender of message
        if player == member.display_name.lower():

            print('Getting html request')
            #Get html
            request = requests.get('https://braacket.com/league/NWAUltimate/player/' + player)
            soup = BeautifulSoup(request.text, 'html.parser')

            print('Parsing rank value')
            #Parse values
            ranking_info = soup.select('section div.row div.col-lg-6 div.panel.panel-default.my-box-shadow div.panel-body div.my-dashboard-values-main')[0].stripped_strings
            ranking_info = [text for text in ranking_info]
            rank = int(ranking_info[0])

            await member.remove_roles(top_10)
            await member.remove_roles(top_25)
            await member.remove_roles(top_50)
            await member.remove_roles(top_100)

            if 1<= rank <= 10:
                await member.add_roles(top_10)
                await ctx.send('Role updated.')
            if 11 <= rank <= 25:
                await member.add_roles(top_25)
                await ctx.send('Role updated.')
            if 26 <= rank <= 50:
                await member.add_roles(top_50)
                await ctx.send('Role updated.')
            if 51 <= rank <= 100:
                await member.add_roles(top_100)
                await ctx.send('Role updated.')

        elif player != member.display_name.lower():
            await ctx.send('You cannot update roles for other users.')
            return
    except:
        await ctx.send('Error updating user role.')

bot.run(token)
