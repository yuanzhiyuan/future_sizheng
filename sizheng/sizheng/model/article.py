__author__ = 'yuan'
import time

from sizheng.model.common import *


class Article(Base):
    __tablename__ = 'sizheng_article'

    id = Column(Integer,primary_key=True)
    categoryid = Column(Integer)
    title = Column(String(127))
    author = Column(String(127))
    content = Column(Text)
    publishTime = Column(Integer,default=0)
    updateTime = Column(Integer)
    state = Column(Integer,default=0) #0:haimeishenhe 1:sizhengzizhan 2:shouye
    views = Column(Integer,default=0)

    def getArticlesBetweenTimestamps(self,formerTime,laterTime):
        articles = session.query(Article).filter(Article.publishTime.between(formerTime,laterTime))
        return articles




    def getAllArticles(self):
        articles = session.query(Article).order_by(desc(Article.id))
        return articles
    def getArticleByCategoryid(self,categoryid):
        articles = session.query(Article).filter(Article.categoryid == categoryid)
        if articles:
            return articles
        else:
            return False
    def getHotArticles(self):
        now = int(time.time())
        oneMonthAgo = now-30*24*3600
        articlesInOneMonth = self.getArticlesBetweenTimestamps(oneMonthAgo,now)
        articles = articlesInOneMonth.order_by(desc(Article.views),desc(Article.id))
        return articles
    def listNewestOfArticles(self,articles):
        handler = articles.order_by(desc(Article.id))
        handledArticles = handler.limit(8).all()
        return handledArticles

    def getArticle(self,id):
        article = session.query(Article).filter(Article.id == id).first()
        if article:
            return article
        else:
            return False

    def getArticleByAuthor(self,author):
        articles = session.query(Article).filter(Article.author == author).order_by(desc(Article.id))
        if articles:
            return articles
        else:
            return False

    def addArticle(self,categoryid,title,content,author):


        article = Article(categoryid = categoryid,title = title,content = content,author = author,updateTime = int(time.time()),publishTime = int(time.time()))
        # print session.query(Article).order_by(desc(Article.id)).first()
        session.add(article)
        session.commit()
        # print session.query(Article).order_by(desc(Article.id)).first().id


    def deleteArticle(self,id):
        article = session.query(Article).filter(Article.id == id).first()
        if article:
            session.delete(article)
            session.commit()
            return True
        else:
            return False

    def updateArticle(self,categoryid,id,title,content,author):
        try:
            session.query(Article).filter(Article.id == id).update({"categoryid":categoryid,"author":author,"title":title,"content":content,"updateTime":int(time.time())})
            session.commit()
            return True
        except Exception,e:
            print str(e)
            return False

    def listAll(self,page=1,pageSize=20):
        handler = session.query(Article).order_by(desc(Article.id))
        pages = handler.count()/pageSize
        articles = handler.limit(pageSize).offset((page-1)*pageSize).all()
        return pages,articles

    def getUnverifiedArticles(self):
        articles = session.query(Article).filter(Article.state == 0)
        if articles:
            return articles
        else:
            return False

    def verify(self,articleid):
        article = session.query(Article).filter(Article.id == articleid)
        if article:
            article.update({"state":1})
            session.commit()
            return True
        else:
            return False


    def cutArticlesAsPages(self,articles,pageSize=20,pageNum=1):
        if articles:
            if articles.count != 0:
                pages = articles.count()/pageSize
                result = articles.limit(pageSize).offset((pageNum-1)*pageSize).all()
                return pages,result
            return False
        return False


# article = Article()
# # article.deleteArticle(0)
# article.addArticle(2,'afa','bbb','ccc')
# list =  article.listNewestOfArticles(article.getAllArticles(),5)
# for a in list:
#     print a.id
# # article.addArticle('afa','bbb','ccc')
# # print article.getArticleByAuthor('ccc')
# # article.listAll()
# article = Article()
# for j in range(10):
#     for i in range(5):
#         article.addArticle(i,'asfasf','agdg','ags')