import os
from tornado import ioloop,web, wsgi
from tornado.escape import json_encode
import json

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from extractor import process_url
from app_crypt import hash_password
import config
 


engine = create_engine(('mysql://%s:%s@localhost' %(config.DB_USER,config.DB_PASSWORD )), echo=False)
engine.execute("CREATE DATABASE IF NOT EXISTS octopusDB;") #create db
engine.execute("USE octopusDB") # select new db

Base = declarative_base()

class Word(Base):
	__tablename__ = 'word'
	id = Column(Integer, primary_key=True)
	word = Column(String(30), nullable=False)
	frequency = Column(Integer, nullable=False)
	uid = Column(String(100), primary_key=True)


	def __repr__(self):
	    return "<Word('%s')>" % (self.word)

word_table = Word.__table__


Base.metadata.create_all(engine)

print 'finished creating table....'


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

class IndexHandler(web.RequestHandler):
	def get(self):
		self.render("index.html")

class WordsHandler(web.RequestHandler):
	def get(self):
		words = session.query(Word).order_by(Word.frequency.desc()) #db.stories.find()
		words_list = []
		for row in words:
			words_dict = {}
			words_dict['word'] = row.word
			words_dict['frequency'] = row.frequency
			words_list.append(words_dict)
		self.set_header("Content-Type", "application/json")
		self.write(json.dumps(words_list))
		

	def post(self):
		url_data = json.loads(self.request.body)
		data = process_url(url_data['url'])
		words_list = []
		for  counter, item  in enumerate(data):
			_word =  ''.join(ch for ch in item if ch.isalpha())#.split('\\')[0]
			_frequency = data[item]
			old_word = None
			# counter = 1
			if len(_word)> 1:
				try:
					old_word =  session.query(Word).filter_by(word = _word ).one() 
				except Exception, e:
					pass
				if not old_word:
					h = hash_password(_word)
					new_word = Word(word=_word, frequency=_frequency, uid = h)
					session.add(new_word)
				else:
					old_word.frequency = old_word.frequency + _frequency
					session.add(old_word)
				words_dict = {}
				words_dict['id'] = counter 
				words_dict['word'] = _word
				words_dict['size'] = _frequency
				words_list.append(words_dict)
				
		session.commit()
		self.set_header("Content-Type", "application/json")
		#self.set_status(201)
		self.write(json.dumps(words_list))
		

# class WordHandler(web.RequestHandler):
# 	def get(self , wordId):
# 		word = session.query(word).filter(id = wordId ).one() 
# 		self.set_header("Content-Type", "application/json")
# 		self.write(json.dumps((word),default=json_util.default))


settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
   
    #"xsrf_cookies": True,
}

application = web.Application([
	(r'/', IndexHandler),
	(r'/index', IndexHandler),
	(r'/api/v1/words', WordsHandler),
	
],**settings)

# if __name__ == "__main__":
# 	application.listen(8888)
# 	ioloop.IOLoop.instance().start()

application = wsgi.WSGIAdapter(application)
