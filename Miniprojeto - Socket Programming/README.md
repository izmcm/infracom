# To execute:

### Run server
```
$ python3 server.py
```

### Run client 
#### GET com texto
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