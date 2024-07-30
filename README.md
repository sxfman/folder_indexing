# folder_indexing
# 文件目录索引工具

Make a HTML index file for any folder you choose, in order to easily accessing sub-folders and files in it.
It can be run under any OS with python ENV.
针对指定的任意目录，生成HTML索引文件，可以快捷访问目录中的所有子目录和文件。

写此程序的起因是好几年前在互联网上偶然下载了一个文件目录制作的小工具，制作的HTML索引很友好，而且也没有广告。但用了几次之后，突然被杀毒软件当病毒给杀掉了，后来到网上再也找不到这个小程序了，因为保留了当时用此软件制作的HTML目录索引文件，所以得以用这个HTML模板自己“复活”了一个当年用过的小工具，也是对那个小工具作者的致敬！如果当年我用过的小工具作者有幸看到我这个项目，觉得HTML索引文件的版面侵犯了您版权，请立即告知我，我诚恳接受您的要求修改或下架。

【Notes】：
1、Running on multi platform: it can be run under win7 and newer windows systems, and systems older than windowsXP( include windowsXP) is not tested. It can run under linux, but the line to set program icon should be commented. Because icon file format on linux differs from windows. And I did not make a special ico file for linux.
2、Packaging: I have tried to package the code by pyinstaller, but it is very annoying. Almost every antivirus software makes virus alert, so I didn't spend much more time on it. 
【说明】：
1、关于跨平台问题：Windows平台Win7之后应该都没问题，XP及之前的系统没试过。Linux系统的图标文件格式与Windows下不同，所以用内置的ico文件无法设置程序图标，我也没精力专门做一个Linux下的图标文件，所以如果想在Linux下运行，把设置图标的那行代码注释掉就行了；
2、打包发布：我使用Pyinstaller打包过此程序，但总是被各种杀毒软件误报为病毒，所以不想再折腾了，如果有人想打包就自己打吧，反正也没啥技术难度。
3、当前界面只支持中文。

【使用界面】：

<img width="301" alt="image" src="https://github.com/user-attachments/assets/cb895bbe-ee92-41db-b124-29ee62123a62">

<img width="629" alt="image" src="https://github.com/user-attachments/assets/d5ecdcfd-3e21-4e4f-857c-9e440faba2a2">
