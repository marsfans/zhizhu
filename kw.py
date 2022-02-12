import requests
import wget
import time
import os
import math
import pprint
from kw_dl import KuWo
from mutagen.mp3 import MP3
from mutagen.apev2 import APEv2File
from mutagen.mp4 import MP4,MP4Cover
from mutagen.flac import FLAC, Picture
import eyed3
from mutagen.id3 import ID3,TIT2,TPE2,TPE1,TALB,APIC,USLT

def tags(song_name,artist,album,formats,pic=None,lrc=None):
	if formats=='mp3':
		m=MP3(artist+'-'+song_name+'.'+formats,ID3=ID3)
		picure=requests.get(pic).content
		m['TIT2']=TIT2(encoding=3,text=song_name)
		m['TPE1'] = TPE1(encoding=3, text=artist)
		m['TPE2'] =TPE2(encoding=3,text=artist)
		m['TALB'] =TALB(encoding=3,text=album)
		m['APIC'] =APIC(encoding=3,mime='image/jpeg',type=3,desc=song_name,data=picure)
		m['USLT']=USLT(encoding=3,lang='eng',text=lrc)
		'''m['artist']=artist
		m['title']=song_name
		m['albumartist']=artist
		m['album']=album'''
		m.save()
	elif formats=='ape':
		m=APEv2File(artist+'-'+song_name+'.'+formats)
		picure=requests.get(pic).content
		m['Title']=song_name
		m['AlbumArtist']=artist
		m['Album']=album
		m['Artist']=artist
		m['Lyrics']=lrc
		m['COVER ART (FRONT)']=picure
		m.save()
	else:
		m = FLAC(artist + '-' + song_name + '.' + formats)
		m['artist'] = artist
		m['title'] = song_name
		m['albumartist'] = artist
		image = Picture()
		image.type = 3
		image.mime = 'image/jpeg'
		image.desc = song_name
		image.data = requests.get(pic).content
		m.add_picture(image)
		m['lyrics']=lrc
		m['album'] = album
		m.save()
key=input('请输入歌名：')
url='http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key='+key+'&pn=1&rn=10'
headers={
	'Cookie': '_ga=GA1.2.1897142952.1639460786; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1640077078,1640149603,1640486246,1640825524; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1640825524; _gid=GA1.2.467871692.1640825524; _gat=1; kw_token=X7O936HRC8E',
	'csrf': 'X7O936HRC8E',
	'Host': 'www.kuwo.cn',
	'origin': 'https://www.kuwo.cn/',
	'Referer': 'https://www.kuwo.cn/',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
}
headers1={
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
}
response=requests.get(url=url,headers=headers)
json_data=response.json()
data_list=json_data['data']['list']
#print(data_list)
for data in data_list:
	song_name=data['name'].replace('&nbsp;',' ')
	singer_name=data['artist'].replace('&nbsp;',' ')
	album=data['album'].replace('&nbsp;',' ')
	rid=data['rid']
	pic=data['pic'].replace('120','1000')
	if '-' in song_name:
		song_name=song_name.split('-')[0]
	else:
		pass
	lrc_url='https://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId='+str(rid).replace('MUSIC_','')
	lrc_json=requests.get(lrc_url,headers=headers1).json()
	lrc=''
	for item in lrc_json['data']['lrclist']:
		text=item['lineLyric']
		times=item['time']
		mc=int(float(str(math.modf(float(times))[0])[0:4])*1000)
		t=time.strftime('%M:%S',time.gmtime(float(times)))
		lrc+='['+str(t)+'.'+str(mc)[0:2]+']'+text+'\n'
	print(rid)
	#print(lrc)
	print(singer_name+'\t'+song_name+'\t'+album)
	#f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=convert_url3&br=320kmp3'
	tys=input('请输入要下载的音质(1.128k;2.192k;3.224k;4.256k;5.320k;6.ape;7.flac;quit为退)：')
	if tys=='1':
		music_info_url=f'https://antiserver.kuwo.cn/anti.s?type=convert_url&format=mp3&response=url&rid='+str(rid)+'&br=128kmp3'	
		play_url=requests.get(music_info_url,headers=headers1).text
		#music_json=requests.get(music_info_url,headers=headers).json()
		#play_url=music_json['data']['url']
		if os.path.exists(singer_name+'-'+song_name+'.mp3')==True:
			continue
		else:
			wget.download(play_url,singer_name+'-'+song_name+'.mp3')
		tags(song_name,singer_name,album,'mp3',pic=pic,lrc=lrc)
		print('\n')
	elif tys=='2':
		music_info_url=f'https://antiserver.kuwo.cn/anti.s?type=convert_url&format=mp3&response=url&rid='+str(rid)+'&br=192kmp3'	
		play_url=requests.get(music_info_url,headers=headers1).text
		#music_json=requests.get(music_info_url,headers=headers).json()
		#play_url=music_json['data']['url']
		if os.path.exists(singer_name+'-'+song_name+'.mp3')==True:
			continue
		else:
			wget.download(play_url,singer_name+'-'+song_name+'.mp3')
		tags(song_name, singer_name, album,'mp3', pic=pic,lrc=lrc)
		print('\n')
	elif tys=='3':
		music_info_url=f'https://antiserver.kuwo.cn/anti.s?type=convert_url&format=mp3&response=url&rid='+str(rid)+'&br=224kmp3'	
		play_url=requests.get(music_info_url,headers=headers1).text
		#music_json=requests.get(music_info_url,headers=headers).json()
		#play_url=music_json['data']['url']
		if os.path.exists(singer_name+'-'+song_name+'.mp3')==True:
			continue
		else:
			wget.download(play_url,singer_name+'-'+song_name+'.mp3')
		tags(song_name, singer_name, album,'mp3', pic=pic,lrc=lrc)
		print('\n')
	elif tys=='4':
		music_info_url=f'https://antiserver.kuwo.cn/anti.s?type=convert_url&format=mp3&response=url&rid='+str(rid)+'&br=256kmp3'	
		play_url=requests.get(music_info_url,headers=headers1).text
		#music_json=requests.get(music_info_url,headers=headers).json()
		#play_url=music_json['data']['url']
		if os.path.exists(singer_name+'-'+song_name+'.mp3')==True:
			continue
		else:
			wget.download(play_url,singer_name+'-'+song_name+'.mp3')
		tags(song_name, singer_name, album,'mp3', pic=pic,lrc=lrc)
		print('\n')
	elif tys=='5':
		music_info_url=f'https://antiserver.kuwo.cn/anti.s?type=convert_url&format=mp3&response=url&rid='+str(rid)+'&br=320kmp3'	
		play_url=requests.get(music_info_url,headers=headers1).text
		#music_json=requests.get(music_info_url,headers=headers).json()
		#play_url=music_json['data']['url']
		if os.path.exists(singer_name+'-'+song_name+'.mp3')==True:
			continue
		else:
			wget.download(play_url,singer_name+'-'+song_name+'.mp3')
		tags(song_name, singer_name, album,'mp3', pic=pic,lrc=lrc)
		print('\n')
	elif tys=='6':
		ape=KuWo('1000kape',str(rid))
		if ape=='':
			pass
		else:
			wget.download(ape,singer_name+'-'+song_name+'.ape')
			tags(song_name, singer_name, album,'ape', pic=pic,lrc=lrc)
			print('\n')
	elif tys=='7':
		flac=KuWo('2000kflac',str(rid))
		if flac=='':
			pass
		else:
			wget.download(flac,singer_name+'-'+song_name+'.flac')
			tags(song_name, singer_name, album,'flac', pic=pic,lrc=lrc)
			print('\n')
	elif tys=='quit':
		break
	else:
		continue
	