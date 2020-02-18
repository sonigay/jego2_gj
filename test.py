import discord
import asyncio
import random
import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('jego-972d19158581.json', scope)
client = gspread.authorize(creds)
doc = client.open_by_url('https://docs.google.com/spreadsheets/d/15p6G4jXmHw7Z_iRCYeFwRzkzLxqf-3Pj0c6FeVuFYBM')



client = discord.Client()



@client.event
async def on_ready():
	print("login")
	print(client.user.name)
	print(client.user.id)
	print("----------------")
	await client.change_presence(game=discord.Game(name='재고현황 안내', type=1))




@client.event
async def on_message(message):
	global gc #정산
	global creds	#정산
    
          
	if message.content.startswith('!재고'):
		SearchID = message.content[len('!재고')+1:]
		gc = gspread.authorize(creds)
		wks = gc.open('오전재고').worksheet('시트1')
		wkstime = gc.open('오전재고').worksheet('데이터')
		
		wks.update_acell('A1', SearchID)
		result = wks.acell('B1').value
		result2 = wkstime.acell('A1').value
            
		embed1 = discord.Embed(
			title = ' :calling:  ' + SearchID + ' 재고현황! ',
			description= '**```css\n' + SearchID + ' 재고현황 입니다.\n마지막 데이터 업로드시간은\n'+ result2 + ' 입니다.' + result + '실시간조회가 아니라서 다소 차이가 있을수 있습니다. ```**',
			color=0xff00ff
			)
		embed2 = discord.Embed(
			title = ' :calling: ' + SearchID + ' 재고조회!! ',
			description= '```' "조회자:" + message.author.display_name +"\n거래처:" + message.channel.name + ' ```',
			color=0xff00ff
			)
		await client.send_message(message.channel, embed=embed1)
		await client.send_message(client.get_channel("674838122332291082"), embed=embed2)
            
	if message.content.startswith('!모델명'):
		SearchID = message.content[len('!모델명')+1:]
		gc = gspread.authorize(creds)
		wks = gc.open('오전재고').worksheet('시트2')
		wks.update_acell('A1', SearchID)
		result = wks.acell('B1').value
		
		embed = discord.Embed(
			title = ' :printer:  모델명 코드 리스트 ',
			description= '**```css\n' + SearchID + ' 모델명 코드는 ' + result + '```**',
			color=0x0000ff
			)
		await client.send_message(message.channel, embed=embed)
                        
access_token = os.environ["BOT_TOKEN"]
git_access_token = os.environ["GIT_TOKEN"]
client.run(access_token)
