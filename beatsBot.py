import re
from discordSetup import run
from discordSetup import client
from spotipySetup import addSong,getTopSongByAtistThenTitle,getTopSongByTitle
#
from youtube_title_parse import get_artist_title

# Youtube config
REGEXYT = r"\bhttps:\/\/(www|m)\.youtu(|\.)be[^ ;]*"
SHOWMORE_BUTTON = "more-button style-scope ytd-video-secondary-info-renderer"
#import google_auth_oauthlib.flow
#import googleapiclient.discovery
#import googleapiclient.errors
#scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
#
# Next step : find and click this element
#
#<paper-button id="more" aria-expanded="false" noink="" class="style-scope ytd-expander" role="button" tabindex="0" animated="" elevation="0" aria-disabled="false"><!--css-build:shady-->
#      <yt-formatted-string class="more-button style-scope ytd-video-secondary-info-renderer" slot="more-button" role="button">Show more</yt-formatted-string>
#    <paper-ripple class="style-scope paper-button"><!--css-build:shady-->
#
#    <div id="background" class="style-scope paper-ripple"></div>
#    <div id="waves" class="style-scope paper-ripple"></div>
#</paper-ripple></paper-button>
#
#
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import sys
#
def youtube_fetch_meta(link):
	artist = ''
	song = ''
	browser = webdriver.Chrome(r'/home/pi/Desktop/Discord Beats Bot/chromedriver')
	browser.get(link)
	delay = 10 # seconds
	try:
		xpath = '//yt-formatted-string[contains(text(),"Show more")]'
		button = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
		button.click()
		try:
			xpath = '//yt-formatted-string[@class="style-scope ytd-metadata-row-renderer" and contains(text(),"Artist")]'
			metaTitle = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
			parent = metaTitle.find_element_by_xpath('..').find_element_by_xpath('..')
			if (parent != None):
				artist = parent.text.splitlines()[1]
			xpath = '//yt-formatted-string[@class="style-scope ytd-metadata-row-renderer" and contains(text(),"Song")]'
			metaTitle = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
			parent = metaTitle.find_element_by_xpath('..').find_element_by_xpath('..')
			if (parent != None):
			   song = parent.text.splitlines()[1]
		except TimeoutException:
			print("Finding the meta info took too much time!")
	except TimeoutException:
			print("Clicking the show more tab took too much time!")
	browser.quit()
	return artist,song


@client.event
async def on_message(message):
		channel = message.channel
		rxResult = re.search(REGEXYT, message.content)
		if  rxResult != None:
			VALIDCHARRGX = '[^0-9a-zA-Z., -?/]+'
			YTlink = rxResult.group()
			artist,song = youtube_fetch_meta(YTlink)
			song = re.sub(VALIDCHARRGX, ' ', song)
			artist = re.sub(VALIDCHARRGX, ' ', artist)
			await channel.send(artist + ' - ' + song)
			songID = getTopSongByAtistThenTitle(artist, song)
			if songID != None:
				results = addSong(songID)
				#if results != None:
			#await client.logout()
		if message.content == 'QUIT':
			await client.logout()

run()
