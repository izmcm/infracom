#as solicitações que o cliente vai fazer ao servidor
#a class do servidor pode usar esse objeto como resposta ao cliente 
class ArchiveList:
    def __init__(self):
        self.movies = ["toy_story","toy_story_2","toy_story_3", "toy_story_4"]
    
    def getAllArchives(self):
        return self.movies
        
    def solictArchive(self,name):
        for movie in self.movies:
            if name == movie:
                return "serverArchives/" + movie + ".jpg"
        
        return "empty"
        

    

# test = ArchiveList()

# print(test.getAllArchives())
# print(test.solictArchive("toy story 5"))
