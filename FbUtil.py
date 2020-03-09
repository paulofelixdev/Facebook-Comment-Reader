import facebook
import json
from fuzzywuzzy import fuzz
import random
import pyperclip
import requests

class UtilFacebook:

    def __init__(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
            self.FB_TOKEN = data['Facebook']['FB_TOKEN']

        #Criar sessão no facebook
        self.fbGraph = facebook.GraphAPI(access_token=self.FB_TOKEN, version="3.1")
        #Obter id da página
        self.pageId = self.fbGraph.request('me')['id']

    #Obter comentário que presisam de ajuda
    def getCommentsNeedingHelp(self):

        #Carregar palavras chave de ajuda
        with open("helpKeywords.json", encoding="utf-8") as file:
            helpKeyWords = json.load(file)

        posts = self.fbGraph.request('me/posts')
        myData = {"NeedHelp":[], "HelpCount":'', "TotalComments":'', "paging":posts["paging"]}


        #Ler post a post
        for post in posts["data"]:
            comments = self.fbGraph.request(str(post["id"])+'/comments')
            #Ler cada comentário do post
            for comment in comments["data"]:

                #Transformar a string do comentario em palavras separadas
                messageArray = comment["message"].split(" ")
                i=0
                for word in messageArray:
                    #Retirar pontuação do comentário
                    pontuation = ".,;:!?'"
                    for mark in pontuation:
                        if mark in word:
                            messageArray[i] = str(word).replace(mark,"")
                    i+=1

                #ler cada palavra do comentario
                for word in messageArray:
                    #ler cada palavra das helpKeywords
                    for keyWord in helpKeyWords["Keywords"]:
                        #Comparar a palavra do comentário com a keyword
                        ratio = fuzz.ratio(word, keyWord) > 50
                        if ratio:
                            #Adicionar comentário a lista de comentário que presisam de ajuda
                            myData["NeedHelp"].append(comment)


        return myData

    def getLatestPostComments(self):
        postComments = {}
        #Obter id da página
        pageId = self.fbGraph.request('me')['id']
        print("Id da pagina: " + pageId)
        #Ver todos os posts recentes
        posts = self.fbGraph.request('me/posts')

        #Ir buscar o ultimo post
        lastPostId = posts['data'][0]['id'] #Retorna uma string -> 'PAGEID_POSTID'
        lastPostId = lastPostId.split('_')[1]
        print("Id do ultimo post: " + lastPostId)
        query = pageId+'_'+lastPostId+'/comments'

        fbComments = self.fbGraph.request(query)
        #Carregar palavras chave de ajuda
        with open("helpKeywords.json", encoding="utf-8") as file:
            helpKeyWords = json.load(file)

        html = ''
        alreadyAdded = False
        for x in fbComments['data']:
            for keyword in helpKeyWords["Keywords"]:
                alreadyAdded = False
                for commentWord in x['message'].split(" "):
                    if (fuzz.ratio(str(commentWord),str(keyword)) > 80):
                        alreadyAdded = True
                        print("Mensagem: " + x['message'])
                        commentId = x['id'].split('_')[1]
                        #https://www.facebook.com/permalink.php?story_fbid=POST&id=PAGINA&comment_id=COMENTARIO
                        user = x['from']['name']
                        userId = x['from']['id']
                        content = x['message']
                        link = 'https://www.facebook.com/permalink.php?story_fbid='+lastPostId+'&id='+pageId+'&comment_id='+commentId

                        break
            if alreadyAdded: break
        return html

    #Criar e postar mensagens random no feed
    def postRandomPosts(self):

        paragraphs = ['Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus non purus risus. Etiam libero justo, lacinia id nisl malesuada, blandit cursus lacus. Suspendisse efficitur non nulla sit amet vestibulum. Nulla eleifend nisl eu magna interdum volutpat. Pellentesque sem nisi, sagittis id velit eget, blandit aliquet quam. Curabitur faucibus vulputate eros eget aliquam. Nullam ut vehicula magna. Pellentesque posuere at risus ut porttitor. Nulla facilisi. Cras ornare magna ac fringilla facilisis. Ut sed sapien mauris. Nulla in eleifend nulla. Donec suscipit malesuada sapien ac tincidunt. Vivamus et ullamcorper augue.',

                      'Suspendisse scelerisque, augue sit amet pellentesque sollicitudin, ligula turpis fermentum mi, eget porta libero massa ac diam. Suspendisse in rutrum neque. Pellentesque at orci ligula. Mauris quis blandit massa. Mauris in turpis quis elit sagittis convallis nec ac urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In pharetra suscipit auctor. Curabitur sit amet feugiat velit.',

                      'In scelerisque enim in neque aliquam, id vulputate ipsum sagittis. Mauris efficitur laoreet risus, et pretium augue placerat eget. Nam interdum nisl nec bibendum fringilla. Aliquam semper facilisis molestie. Integer blandit, neque a consectetur elementum, mauris urna suscipit enim, et ornare velit ligula eget purus. Suspendisse vulputate diam eget cursus molestie. Donec venenatis justo in augue tempus, sed laoreet orci laoreet. Praesent dapibus ante viverra, facilisis magna id, fermentum orci. Ut lobortis feugiat sem et sodales. Maecenas at malesuada odio, mattis sagittis lacus. Aliquam erat arcu, suscipit gravida porta nec, fringilla et sapien. Pellentesque eleifend dolor ut hendrerit ultrices. Pellentesque finibus libero quis aliquet pharetra. Curabitur blandit eget mi vitae dignissim.',

                      'Sed lorem neque, venenatis vel ex sed, tincidunt bibendum sem. Donec nec erat suscipit, rutrum arcu non, iaculis turpis. Proin id gravida mauris. Proin eleifend justo placerat quam placerat gravida. Donec mi magna, laoreet at velit et, porta lobortis neque. Integer tempus interdum purus, ut venenatis mauris hendrerit sed. Nulla dapibus blandit magna, ac vulputate tellus suscipit ac.',

                      'Praesent gravida laoreet nunc. Mauris sodales diam ut nulla fringilla, et hendrerit augue cursus. Nulla consectetur metus finibus egestas sodales. Aenean elementum id neque vitae luctus. Duis sollicitudin in dui id tristique. Mauris quis facilisis est. Quisque ut arcu imperdiet, vulputate nunc non, consectetur ante. Sed a eleifend dui, quis faucibus dolor. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Morbi mauris diam, facilisis quis justo vitae, sodales volutpat orci. Donec eleifend felis ornare purus lacinia viverra. Aenean hendrerit dolor turpis, in maximus mi facilisis a.',

                      'Sed ut velit aliquet, bibendum ante a, ullamcorper turpis. Ut ipsum tellus, tincidunt nec posuere sit amet, vestibulum imperdiet purus. Suspendisse venenatis sem urna, id gravida ligula lobortis quis. Sed mollis ut libero vitae bibendum. Nulla ut pellentesque nibh. Maecenas a iaculis eros. Maecenas convallis, turpis non egestas pulvinar, tellus justo ullamcorper mauris, et hendrerit magna orci vitae massa. Donec hendrerit pellentesque nulla, condimentum sodales metus pulvinar eu. Etiam in ante vehicula, facilisis ante vel, congue est. Sed vestibulum placerat dictum. Etiam eu ex ac tellus varius sollicitudin ut id felis. Nam sollicitudin nulla nec justo aliquet, sed pulvinar nunc rhoncus. Donec diam libero, sodales consequat pulvinar vitae, gravida quis orci. Nulla gravida dolor non metus porta, sagittis tempus sem efficitur. Morbi fermentum sapien faucibus, lacinia nunc sed, lobortis mi.',

                      'Ut diam elit, facilisis tempus enim at, lacinia feugiat massa. Vivamus euismod lacinia eros, eu porttitor lectus. Donec venenatis id felis vel elementum. Proin eros metus, varius non nisl eget, commodo eleifend turpis. Nulla dictum vulputate mauris. Cras sed tincidunt tellus, ultricies accumsan odio. Nulla finibus risus vitae faucibus elementum.',

                      'Donec efficitur nunc a tellus pellentesque, consectetur suscipit sapien luctus. Praesent cursus urna sed ligula finibus tincidunt. Donec consectetur leo nunc, ac lacinia enim sagittis eget. In ac fringilla enim, sed eleifend augue. Curabitur placerat neque in nulla sollicitudin elementum. Praesent elit nunc, commodo quis fermentum id, blandit quis urna. Sed feugiat commodo gravida. Aliquam rutrum ut sem eu interdum. Nunc leo ex, imperdiet sit amet orci ut, tincidunt bibendum diam. Vivamus varius, justo et rhoncus commodo, orci nibh dapibus metus, in condimentum erat dolor ut mauris. Integer viverra, odio sit amet consectetur molestie, ligula nulla commodo felis, non commodo est lectus in lorem. Aliquam vestibulum eu libero vitae molestie. Proin elementum congue convallis. Etiam posuere risus tincidunt elit dictum interdum.',

                      'Cras lorem ligula, sollicitudin vitae orci ac, elementum cursus erat. Maecenas augue magna, convallis id metus vitae, sagittis luctus nulla. Aliquam commodo ipsum vel mi posuere hendrerit. Aliquam semper orci in feugiat ultricies. In tincidunt dui vel arcu ullamcorper imperdiet. Nam vehicula dapibus ante, sit amet viverra lectus hendrerit id. Donec porttitor, quam rutrum aliquam dignissim, augue orci condimentum justo, euismod varius turpis metus nec urna. Aenean sit amet nibh imperdiet augue varius fringilla. Praesent blandit, nulla posuere venenatis elementum, sem enim suscipit massa, in accumsan quam justo vitae metus. Curabitur vel lorem eu risus venenatis aliquam finibus at dui. Donec tortor orci, dapibus quis pellentesque non, elementum vel lorem. Curabitur malesuada erat rutrum placerat aliquam. Vivamus mauris justo, bibendum at fermentum a, molestie vel nisi. Vivamus tincidunt lectus lorem. Curabitur elementum sed felis at mollis.']
        for x in paragraphs:
            response = self.fbGraph.put_object('me','feed',message=x)
            print(response)

    #Criar comentário random, não da para os publicar.
    def createRandomComments(self, help):
        randomText = [
            {
                "text": "Lorem ipsum"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna et arcu"
            },
            {
                "text": "Lorem ipsum dolor sit amet,"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus."
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing"
            },
            {
                "text": "Lorem ipsum dolor sit amet,"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor."
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus."
            },
            {
                "text": "Lorem ipsum"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna et"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus."
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus."
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec"
            },
            {
                "text": "Lorem ipsum dolor sit"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna et arcu"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec"
            },
            {
                "text": "Lorem ipsum dolor"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor."
            },
            {
                "text": "Lorem ipsum dolor sit"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna et"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor."
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec"
            },
            {
                "text": "Lorem ipsum dolor sit amet,"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna et"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed"
            },
            {
                "text": "Lorem"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer"
            },
            {
                "text": "Lorem"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna et"
            },
            {
                "text": "Lorem ipsum dolor sit"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
            },
            {
                "text": "Lorem ipsum"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor."
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec"
            },
            {
                "text": "Lorem ipsum dolor sit"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus."
            },
            {
                "text": "Lorem"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna et"
            },
            {
                "text": "Lorem ipsum dolor"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus."
            },
            {
                "text": "Lorem ipsum dolor"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna et arcu"
            },
            {
                "text": "Lorem ipsum dolor sit amet,"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus."
            },
            {
                "text": "Lorem ipsum dolor"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus."
            },
            {
                "text": "Lorem"
            },
            {
                "text": "Lorem ipsum dolor sit"
            },
            {
                "text": "Lorem ipsum dolor"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus."
            },
            {
                "text": "Lorem ipsum dolor"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec"
            },
            {
                "text": "Lorem"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna et arcu"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus."
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna et"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing"
            },
            {
                "text": "Lorem ipsum dolor sit"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer"
            },
            {
                "text": "Lorem ipsum"
            },
            {
                "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur sed tortor. Integer aliquam adipiscing lacus. Ut nec urna"
            }
        ]

        randomKeyWords = ['informacao', 'ero', 'ajuda', 'infromacao', 'erro', 'informação']

        #I want 35% of the random text to have keywords

        if help:
            for x in randomText:
                probability = 35 # 0 to 100
                maxRandom = int((randomKeyWords.__len__()*100)/probability)
                num = random.randint(0,maxRandom)
                if num < randomKeyWords.__len__():
                    x["text"] += ' ' + str(randomKeyWords[int(num)])
                    pyperclip.copy(x["text"])
                    input("Clica enter")
        else:
            maxRandom = randomText.__len__()-1
            parar = ''
            while parar == '':
                num = random.randint(0,maxRandom)

                pyperclip.copy(str(randomText[num]["text"]))
                print("\n\n\n")
                print(randomText[num]["text"])
                parar = input("Texto copiado.     Clica enter ou escrever algo para parar")

        return randomKeyWords


