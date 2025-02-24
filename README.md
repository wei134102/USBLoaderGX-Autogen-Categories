# USBLoaderGX-Autogen-Categories
A poorly coded python script to auto-generate game categories from a WiiTDB.xml file

## Dependencies
Python 3: `pip install --upgrade lxml untangle`

## How to use
Obtain a copy of `wiitdb.xml` from USBLoaderGX. This can be done by going to it's settings menu, navigating to `Update` on page 3, and clicking `WiiTDB.xml`.<br/><br/>
Mount your drive with the HomeBrew Channel `apps` folder on it into your computer and copy `..\apps\usbloader_gx\wiitdb.xml` into the same folder as the script, run the script, and copy over the newly created `GXGameCategories.xml` to `..\apps\usbloader_gx` and overwrite.<br/><br/>
Done! You now have categories for GameCube, Programs, Third-Party, VC-Arcade, VC-Commodore 64, VC-MSX, VC-N64, VC-NeoGeo, VC-NES, VC-Sega Genesis, VC-SEGA Master System, VC-SNES, VC-Turbo Grafx 1.6, Wii, and WiiWare.


2025年2月24更新
增加游戏类型到每个游戏里面
