import openai
from cosine.cosine import CosineSimilarity
import json

openai.api_key = 'add your OpenAI key'

class chatAI():
    def __init__(self):
        self.initialize()
        self.conversation_stage = 1
        self.temperature = 0.8
        self.state = 0
    
    def initialize(self, ):
        self.messages = []

    def reply(self, message):
        # 대화 단계에 따라 다른 질문을 추가
        if self.conversation_stage == 1:
            print('시작')
            prompt_additions = '안녕하세요! 영화에 대해 이야기해봐요! 선호하는 영화 장르가 무엇인가요?'
            self.conversation_stage = 2
            print('지금 단계는: ', self.conversation_stage)
        elif self.conversation_stage == 2:
            print('영화 감독')
            prompt_additions = '당신이 선호하는 영화 감독이 있나요?'
            self.conversation_stage = 3
            print('지금 단계는: ', self.conversation_stage)
        elif self.conversation_stage == 3:
            print('영화 배우')
            prompt_additions = '그렇다면 선호하는 영화 배우가 있나요?'
            self.conversation_stage = 4
            print('지금 단계는: ', self.conversation_stage)         

        else:
            self.state = 1
            prompt_additions = '당신은 정말 좋은 안목을 가지고 있군요!'
            #prompt_additions = self.movie_recommand()
            #self.messages = []
        
        self.messages.append({'role': 'user', 'content': message})
        self.messages.append({'role': 'system', 'content': prompt_additions})

        chatAnswer = openai.ChatCompletion.create( 
            model = 'gpt-3.5-turbo',
            messages=self.messages,
            n = 1,
            stop = None,
            temperature = self.temperature
            )
        
        result = ''
        for choice in chatAnswer.choices:
            result += choice.message['content']

        self.messages.append({"role": "assistant", "content": result})        
        print(result)

        if self.state == 1:
            prompt_movies = json.loads(self.movie_recommand())
            prompt_movies['texts'] = [result]
            #result += prompt_movies
            #print('prompt_movies: ', prompt_movies)
            result = json.dumps(prompt_movies, ensure_ascii=False)
        else:
            prompt_movies = {}
            prompt_movies['texts'] = [result]
            result = json.dumps(prompt_movies, ensure_ascii=False)
        return result
    
    def movie_recommand(self):
            cosine_similarity = CosineSimilarity()
            user_input = " ".join([cosine_similarity.preprocess(msg['content']) for msg in self.messages if msg['role'] == 'user'])
            print('사용자 입력을 합친 값: ', user_input)
            titles, posters = cosine_similarity.result(user_input)
            print(titles[:4])
            print(posters[:4])
            data = {
                'titles': titles[:4],
                'posters': posters[:4],
                #'text': '당신의 취향에 맞는 영화를 찾았어요!'
            }
            #print(json.dumps(data))
            return json.dumps(data, ensure_ascii=False)