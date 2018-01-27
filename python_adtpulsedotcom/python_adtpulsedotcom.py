from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from seleniumrequests import Firefox
import time
import os
import sys
import config

_LOGGER = logging.getLogger(__name__)

class AdtPulsedotcom(object):
    """
    Access to adtpulse.com partners and accounts.

    This class is used to interface with the options available through
    portal.adtpulse.com. The basic functions of checking system status and arming
    and disarming the system are possible.
    """

	### AdtPulse.com constants ###

	# AdtPulse.com baseURL
	ADTPULSEDOTCOM_URL = 'https://portal.adtpulse.com'

	# AdtPulse.com contextPath
	def adtpulse_version(ADTPULSEDOTCOM_URL):
		"""Determine current ADT Pulse version"""
		resp = requests.get(ADTPULSEDOTCOM_URL)
		parsed = BeautifulSoup(resp.content, html.parser)
		adtpulse_script = parsed.find_all('script', type='text/javascript')[4].string
		if "=" in adtpulse_script:
			param, value = adtpulse_script.split("=",1)
		adtpulse_version = value
		adtpulse_version = adtpulse_version[1:-2]
		return(adtpulse_version)

	ADTPULSEDOTCOM_CONTEXT_PATH = adtpulse_version(ADTPULSEDOTCOM_URL)

	# Page elements on portal.adtpulse.com that are needed
	# Using a dict for the attributes to set whether it is a name or id for locating the field
	LOGIN_URL = ADTPULSEDOTCOM_URL + ADTPULSEDOTCOM_CONTEXT_PATH + '/access/signin.jsp'
	ADTPULSE_USERNAME = ('name', 'usernameForm')
	ADTPULSE_PASSWORD = ('name', 'passwordForm')
	#LOGIN_BUTTON = ('name', 'signin')

	DASHBOARD_URL = ADTPULSEDOTCOM_URL + ADTPULSEDOTCOM_CONTEXT_PATH + '/summary/summary.jsp

	def get_alarm_status():
		url = LOGIN_URL

		display = Display(visible=0, size=(800, 600))
		display.start()

		browser = webdriver.Chrome()
		browser.get(url)

		response = webdriver.request('GET', url)
		_LOGGER.debug('Response status from AdtPulse.com: %s - %s', response.status, response.statusText)

		username = browser.find_element_by_name('usernameForm')
		username.send_keys(config.ADTPULSE_USERNAME)

		password = browser.find_element_by_name('passwordForm')
		password.send_keys(config.ADTPULSE_PASSWORD)

		browser.find_element_by_name('signin').click()

		time.sleep(20)
		html = browser.page_source
		postlogin_url = browser.url
		_LOGGER.debug('Post Login URL from AdtPulse.com: %s ', postlogin_url)

		soup = BeautifulSoup(html, 'lxml')

		currentStatus = soup.findAll('div', { 'id': 'divOrbContent' })
		_LOGGER.debug('Current Alarm Status DIV from AdtPulse.com: %s ', currentStatus )

		if currentStatus:
			for status in currentStatus:
				status_textsummary = status.find_element_by_id('divOrbTextSummary')
				_LOGGER.debug('Status Text DIV from AdtPulse.com: %s - %s', status_textsummary)

		if status_textsummary:
			for text in status_textsummary:
				status_text = status.findAll('span', { 'class': 'p_boldNormalTextLarge'})
				_LOGGER.debug('Status Text DIV from AdtPulse.com: %s - %s', status_text)
		        for string in alarm_status.strings:
                    if "." in string:
                        param, value = string.split(".",1)
                adtpulse_alarmstatus = param
                state = adtpulse_alarmstatus
				
		browser.quit()
		display.stop()

		return state