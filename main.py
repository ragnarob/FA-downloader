import requests
import json
import sys
import os
import shutil

class FAExporter():

	def __init__(self):
		with open('./config.json', 'r') as configfile:
			self.config = json.load(configfile)
		self.header = {'cookie': 'a={}; b={}'.format(self.config['cookie']['a'], self.config['cookie']['b'])}

		self.main()


	def main(self):
		if sys.argv[1] == 'album':
			self.get_albums()
		elif sys.argv[1] == 'search':
			self.search()


	def search(self):
		artists = []

		if not os.path.exists('output'):
			os.makedirs('output')

		with open('ids.txt', 'r') as txtfile:
			for line in txtfile.readlines():
				splitline = line.split(' ', 1)
				artists.append({'artist': splitline[0].replace('_', ''), 'search': splitline[1].strip('\n')})

		for artist_obj in artists:
			self.search_artist(artist_obj)


	def search_artist(self, artist_obj):
		last_page = False
		page_number = 1
		found_submissions = []

		while not last_page:
			url = 'http://www.furaffinity.net/gallery/{}/{}'.format(artist_obj['artist'], page_number)
			print(url)
			response = requests.get(url, headers=self.header)
			response = response.text
			page_number += 1

			# Figure out if last page
			number_of_images = response.count('<figure')
			last_page = number_of_images < 72

			search_word = '<figure'
			while search_word in response:
				response = response[ response.find(search_word)+5 : ]

				this_submission = response[ : response.find('/figure') ]
				submission_id = this_submission[ this_submission.find('/view/')+6 : this_submission.find('/"><img alt') ]
				this_submission = this_submission[ this_submission.find('figcaption') : ]
				submission_title = this_submission[ this_submission.find('title="')+7 : this_submission.find('">') ]
				if artist_obj['search'] in submission_title:
					found_submissions.append({'title': submission_title, 'id': submission_id})
		
		folder_name = artist_obj['artist'] + ' - ' + artist_obj['search']
		folder_name = folder_name.replace(':', '-').replace('/', 'of').replace('\\', 'of').replace('?', 'QMARK').replace('|', '-')
		if not os.path.exists('output/' + folder_name):
			os.makedirs('output/' + folder_name)
			
		if len(found_submissions):
			for index, submission in enumerate(list(reversed(found_submissions))):
				image_num = '0'+str(index) if index<10 else str(index)
				self.get_submission(submission['id'], folder_name, image_num + '-' + submission['title'], '{}/{}'.format(index, len(found_submissions)))
				print('Downloaded file {} of {}'.format(index+1, len(found_submissions)))
			

	def get_albums(self):
		album_urls = []

		# No comic ids specified as params => ids.txt should be filled
		if len(sys.argv) == 2:
			with open('ids.txt', 'r') as txtfile:
				album_urls = [some_id.strip() for some_id in txtfile.readlines() if some_id]
		else:
			album_urls = sys.argv[2:]

		for url in album_urls:
			self.get_album(url)


	def get_album(self, url):
		album_res = requests.get(url, headers=self.header)
		album_res = album_res.text

		album_res = album_res[album_res.find('<div class="submission-list"') : album_res.find('var descriptions')]

		album_title = album_res[ album_res.find('<h3>')+4 : album_res.find('</h3>') ].replace(':', '-').replace('/', 'of').replace('\\', 'of').replace('?', 'QMARK').replace('|', '-')

		# Finding artist name
		artist_substring = album_res[ album_res.find('<figcaption>') : album_res.find('</figcaption>') ]
		artist_substring = artist_substring[ artist_substring.find('<i>by</i>') : ]
		album_artist = artist_substring[ artist_substring.find('/user/')+6 : artist_substring.find('/" title=') ]

		start_string = '<p><a href="/view/'
		stop_string = '/" title="'
		slice_string = '</figure>'
		submission_ids = []

		while start_string in album_res:
			submission_ids.append( album_res[ album_res.find(start_string)+len(start_string) : album_res.find(stop_string) ] )
			album_res = album_res[ album_res.find(slice_string) + 5 : ]

		folder_name = album_artist + ' - ' + album_title
		if not os.path.exists('output/' + folder_name):
			os.makedirs('output/' + folder_name)
		for index, submission_id in enumerate(list(reversed(submission_ids))):
			image_num = '0'+str(index) if index<10 else str(index)
			self.get_submission(submission_id, folder_name, image_num, '{}/{}'.format(index+1, len(submission_ids)))
			print('Downloaded file {} of {}'.format(index+1, len(submission_ids)))


	def get_submission(self, submission_id, output_folder, image_name, progress_string):
		image_name = image_name.replace(':', '-').replace('/', 'of').replace('\\', 'of').replace('?', 'QMARK').replace('|', '-')
		url = 'http://www.furaffinity.net/view/'+submission_id
		print(progress_string, url)
		response = requests.get(url, headers=self.header)
		response = response.text

		image_url = response[response.find('data-fullview-src="')+19 : response.find('" data-preview-src="')]
		filetype = image_url[-3:].replace('peg', 'jpg')
		
		img_request = requests.get('https:'+image_url, headers=self.header, stream=True)
		with open('{}/{}.{}'.format('output/' + output_folder.strip(), image_name, filetype), 'wb') as img_file:
			img_request.raw.decode_content = True
			shutil.copyfileobj(img_request.raw, img_file)
		
FAExporter()