from lxml import builder as xmlb
from lxml import etree as xmlt
from lxml.etree import SubElement as xmlse
from untangle import parse as up

gameTypeMap={'GameCube':'01',
'Programs':'02',
'Third-Party':'03',
'VC-Arcade':'04',
'VC-Commodore 64':'05',
'VC-MSX':'06',
'VC-N64':'07',
'VC-NeoGeo':'08',
'VC-NES':'09',
'VC-Sega Genesis':'10',
'VC-SEGA Master System':'11',
'VC-SNES':'12',
'VC-Turbo Grafx 1.6':'13',
'Wii':'14',
'WiiWare':'15'}

xmldocBase=xmlb.ElementMaker()
USBLoaderGX=xmldocBase.USBLoaderGX
Revision=xmldocBase.Revision
Categories=xmldocBase.Categories
GameCategories=xmldocBase.GameCategories

xmldocLayout=USBLoaderGX(
  Revision('1281'),
  Categories(),
  GameCategories()
)

defaultCategory=xmlse(xmldocLayout[1], 'Category')
defaultCategory.set('ID','00')
defaultCategory.set('Name','All')

for gameType,gameID in gameTypeMap.items():
  autogenCategory=xmlse(xmldocLayout[1], 'Category')
  autogenCategory.set('ID',gameID)
  autogenCategory.set('Name',gameType)

wiitdb_xml=up('wiitdb.xml')
for game in wiitdb_xml.datafile.game:
  gameType=''
  if game.type.cdata=='': gameType='Wii'
  elif game.type.cdata=='Channel': gameType='Programs'
  elif game.type.cdata=='Homebrew': gameType='Third-Party'
  elif game.type.cdata=='VC-NEOGEO': gameType='VC-NeoGeo'
  elif game.type.cdata=='CUSTOM': gameType='Third-Party'
  elif game.type.cdata=='VC-C64': gameType='VC-Commodore 64'
  elif game.type.cdata=='VC-MD': gameType='VC-Sega Genesis'
  elif game.type.cdata=='VC-PCE': gameType='VC-Turbo Grafx 1.6'
  elif game.type.cdata=='VC-SMS': gameType='VC-SEGA Master System'
  else: gameType=game.type.cdata
  autogenGame=xmlse(xmldocLayout[2], 'Game')
  autogenGame.set('ID',game.id.cdata)
  try: autogenGame.set('Title',game.locale.title.cdata)
  except: autogenGame.set('Title',game.locale[0].title.cdata)
  autogenGameDefaultCategory=xmlse(autogenGame, 'Category')
  autogenGameDefaultCategory.set('ID','00')
  autogenGameDefaultCategory.set('Name','All')
  autogenGameAutogenCategory=xmlse(autogenGame, 'Category')
  autogenGameAutogenCategory.set('ID',gameTypeMap.get(gameType))
  autogenGameAutogenCategory.set('Name',list(gameTypeMap.keys())[list(gameTypeMap.values()).index(gameTypeMap.get(gameType))])

xmlData=b''.join([b'<?xml version="1.0" encoding="UTF-8"?>\n',xmlt.tostring(xmldocLayout,encoding="UTF-8",xml_declaration=False,pretty_print=True)])
with open('GXGameCategories.xml','wb') as f: f.write(xmlData)