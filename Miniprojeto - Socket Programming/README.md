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

### GET
```
$ python3 client.py -c GET -f textGET.txt -t outputTextGET.txt
```
```
$ python3 client.py -c GET -f dogGET.jpg -t outputDogGET.jpg
```

### POST
```
$ python3 client.py -c POST -f "POST realizado com sucesso!" -t outputPOST.txt
```

### GETPROG
```
$ python3 client.py -c GETPROG -f inputGETPROG.exe -t outputGETPROG.exe
```

OBS: inputGETPROG.exe é um programa que foi gerado pelo compilador de C e que printa no terminal a mensagem:    
```
Hello World
The program run successfully!
```