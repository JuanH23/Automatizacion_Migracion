import os
from pathlib import Path


class Search:
    def __init__(self):
        super().__init__()

    def buscar_archivo(self,name_file,ruta):
        for root,dirs, files in os.walk(ruta):
            for file in files:
                if file.endswith('.xlsx') and file==name_file:
                    return Path(root)/file
            
            

