import webapp2
import jinja2
import os
from google.appengine.ext import db

#set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class BlogPost(db.Model):
    title = db.StringProperty(required = True)
    blogtext = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
    """For storing blogposts in the database and inputting new ones"""
    def render_base(self, title="", blogtext="", error=""):
        blogs = db.GqlQuery("SELECT * FROM BlogPost"
                            "ORDER BY created DESC")

        self.render("base.html", title=title, blogtext=blogtext, error=error, blogs = blogs)

    def get(self):
        self.render_base()

    def post(self):
        title = self.request.get("title")
        blogtext = self.request.get("blogtext")

        if title and blogtext:
            b = BlogPost(title = title, blogtext = blogtext)
            b.put()

            self.redirect("/")
        else:
            error = "We need both a title and some content!"
            self.render_base(title, blogtext, error)

    # def post(self):
    #     self.response.write(self.request.POST['blogtext'])
    #



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', MainPage),
    ('/newpost', MainPage)

], debug=True)
