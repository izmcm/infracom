# Executar
## 1. Rodar server
```
$ python3 server.py
```

## 2. Rodar client

#### Argumentos
-c: Comando que será realizado. Pode ser GET ou POST.   
-f: Em GET, arquivo que será transferido (binário ou texto). Em POST, texto que será gravado no arquivo.   
-t: Nome do novo arquivo.   
-h: Ajuda.   

### GET com texto
```
$ python3 client.py -c GET -f file.txt -t outputFile.txt
```

#### GET com arquivos binários
```
$ python3 client.py -c GET -f dog.jpg -t outputDog.jpg
```

#### POST
```
$ python3 client.py -c POST -f "POST realizado com sucesso!" -t 01.txt
```
