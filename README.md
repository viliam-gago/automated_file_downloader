# Automated File Downloader

At the time this script was created, I work as a Localization Engineer. We manipulate a lot of files on daily basis. I've noticed one specific procedure, that occured 
quite regulary. This task is just downloading multiple files from a server. The whole thing is executed manually - you move the cursor, click on download and wait
for the file to be pulled into local machine. That procedure itself isn't such problem, but sometimes (rather often) comes bigger project, containing hundreds of files in total. Then,
clicking through the whole list can quickly become exhausting (and can take even hours to get through !). 

So I sat down and opened IDE - decided to save my colleague's carpal tunnels, I came up with an idea to automate this task using my modest Python skills.

**This file is executable only when acces to mentioned server is granted.** However, I would like to publish for later inspiration or use.

## What does the script do:
#### - Uses BeautifulSoup library to get links of files to be downloaded

#### - Downloads all the files of particular project

#### - Uses threading to get all the files even faster

#### - Provides GUI to allow simple use without need to code anything

#### - Runs from .exe file for quick & easy acces

## How to use:
To get required files, just paste the URL of particular project (or multiple project URLs) into text box, choose required file type and press download. This version 
saves all the files into the folder where the .exe file is located (into newly created folder.)

Although this script isn't much complex, it proved itself quite useful. Me and even  my colleagues are using it on daily basis, saving hours and hours of exhausting work.

![alt text](https://github.com/viliam-gago/automated_file_downloader/blob/master/img/pic.png?raw=true)
