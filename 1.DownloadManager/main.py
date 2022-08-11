import requests
import sys
import os
from tqdm import tqdm

def downloader(url):
    chunk_size = 1024

    #naming the file
    local_file = url.split('/')[-1]
    local_file = checkFile(local_file)
    
    data = requests.get(url, stream=True)
    # if there is no content-lenght, don't show progress bar
    if 'content-length' not in data.headers:
        with open(local_file, 'wb')as file:
            file.write(data.content)
    else:
        total_size = int(data.headers['content-length'])
        with open(local_file, 'wb') as file:
            for data_chunks in tqdm(iterable=data.iter_content(chunk_size=chunk_size),total=total_size/chunk_size,unit='KB'):
                file.write(data_chunks)
# chech if there is another file with the same name
def checkFile(file):
    if file in os.listdir():
        option = input("File already exists, choose another filename(r) or overwrite(o): ")
        while option != 'r' and option != 'o':
            option = input("File already exists, choose another filename(r) or overwrite(o): ")
            
        if option == 'r':
            file = input("New filename: ")
    return file

# ask for an url if the user don't put it 
if __name__ == '__main__':
    if len(sys.argv) > 1:
        downloader(sys.argv[1])        
    else:
        sys.argv.append(input("Digite a url do arquivo: "))
        downloader(sys.argv[1])

