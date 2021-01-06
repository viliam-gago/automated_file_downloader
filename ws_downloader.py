import re
import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import PySimpleGUI as sg


def download_url(arg):
    """ Function is used in ThreadPoolExecutor.
        Takes link and asset name from input argument, then uses these to download file
        given specific name according to asset_name
        
        !takes 'typ' variable from outer scope to determine reference / source file!"""
        
    link, asset_name = arg
    
    if typ == 'target':
        filename = os.path.join(folder,project_name + asset_name + '.pdf')
        with open(filename, 'wb') as f:
            f.write(requests.get(link).content)
    
    elif typ == 'source':
        filename = os.path.join(folder, 'EN_' + project_name + asset_name + '.pdf')
        with open(filename, 'wb') as f:
            f.write(requests.get(link).content)
        
    

def create_folder(typ):
    """Function creates folder at C for simplicity. If folder already there -> use current one """
    
    # folder = values['-IN2-'] + f'\{typ}'
    folder = r'C:\WS_files'
    if not os.path.exists(folder): 
        os.mkdir(folder)
    
    return folder


def get_page_content(url):
    """link -> web content into soup object ->  text content of site """
    
    response = requests.get(url)
    content = BeautifulSoup(response.text, "html.parser")
    
    return content


def get_project_name(soup_obj):
    """finds project name, does some formatting -> string of project name """
    project_name = soup_obj.find('td', class_='header_page_title').text
    project_name = project_name.split('Task List for Project: ')[1]
    project_name = project_name.replace(' ', '_').replace('(', '_').replace(')', '_')
    
    return project_name


layout = [
    [sg.Text('URL')],
    [sg.Multiline(size=(80, 5), key='textbox')] ,
    [sg.Button('Download')],#sg.Button('Erase URL')],
    [sg.Radio('Source',group_id='my', key='src', default=True), sg.Radio('Target', group_id='my', key='tgt')],
    [sg.Text("Files saved in C:\\WS_files")] #sg.Input(os.getcwd(),key="-IN2-" ,change_submits=True), sg.FolderBrowse(key="-IN-")]
]


window = sg.Window('WS file downloader', layout)
######

while True:
    
    event, values = window.read()
    if event in ('Exit', None):
        break  
    
    
    elif event == 'Download':
        # try:
            # determine source/target according to user choice; get page content (html text)
            typ = 'source' if values['src'] else 'target'
            
            #extract separated links from textbox
            links = values['textbox']
            links_list = [link for link in links.split('\n') if link != '']
            
            #loop over links
            for link in links_list:
                try:
                  pg_content = get_page_content(link)
                  
                 
                  #extract token & project_id - token unique for login to server, project_id for particular project
                  token = re.search(r'token=(\w+)', link).group(1)
                  project_id = re.search(r'project=(\w+)', link).group(1)
                 
                  #create location for download
                  #extract project name & asset names for particular project -> these used to create file's name
                  folder = create_folder(typ)
                  project_name = get_project_name(pg_content)
                  assets = [asset.text for asset in pg_content.find_all('a', href=True, target='popup_viewer')]
                 
                  #scrap links, format them using token and project id, store into iterable
                  links = []
                  for i, link in enumerate(pg_content.find_all('a', href=re.compile(f'stage={typ}'))):
                      link = link.get('href') + f'&token={token}&project={project_id}'
                      links.append(link)
                 
                  #setting arguments for ThreadPoolExecutor (threading used due to download speedup)
                  args = [(a,b) for a,b in zip(links,assets)]
                  with concurrent.futures.ThreadPoolExecutor() as executor:
                      results = executor.map(download_url, args)
                     
                  #clear input window after download
                  window['textbox']('')
                     
                 
                except requests.exceptions.MissingSchema:
                    sg.popup('Unable to load website content from this link.')  
                    continue         
                        
                except AttributeError:
                    sg.popup('Unable to load website content from this link.') 
                    continue
        
window.close()
