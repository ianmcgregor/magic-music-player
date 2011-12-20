#import cgi
import webapp2
#import gdata.youtube
import gdata.youtube.service
import gdata.alt.appengine
import os
from google.appengine.ext.webapp import template
#from google.appengine.dist import use_library
#use_library('django', '0.96')

TITLE = 'MAGIC MUSIC PLAYER'
MESSAGE_DEFAULT = 'Enter anything'

class MainPage(webapp2.RequestHandler):
    def get(self):
        """ Initial page waiting for user submission. """
        template_values = {
            'title': TITLE,
            'message': MESSAGE_DEFAULT,
            'messageDefault': MESSAGE_DEFAULT,
            'error':'' 
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

        
class ResultsPage(webapp2.RequestHandler):
    def get(self):
        """ Default get """
        self.redirect("/")
    
    def post(self):
        """ Get user input from submitted form. """
        userInput = self.request.get('inputField')
    #    self.response.out.write(cgi.escape(content))
        if len(userInput) > 0:
            self.search_youtube(userInput)
        else:
            self.redirect("/")
    
    def search_youtube(self, search_terms):
        """ Search YouTube """
        try:
            client = gdata.youtube.service.YouTubeService()
            gdata.alt.appengine.run_on_appengine(client)
            query = gdata.youtube.service.YouTubeVideoQuery()
            query.categories.append('music')
            query.vq = search_terms
            query.orderby = 'relevance' #relevance, viewCount, published, rating
            query.racy = 'include'
            feed = client.YouTubeQuery(query)
            self.check_search_results(feed)
        except Exception, err:
            self.write_error(err)

    def check_search_results(self, feed):
        """ Attempt to find a valid entry in search results. """
        error = ''
        swfURL = ''
        message = ''
        try:
            entries = []
            l = len(feed.entry)
            #self.response.out.write('Number of results:' + str(l))
            if l > 0:
                for entry in feed.entry:
                    try:
                        #entries.append( entry.GetSwfUrl() )
                        if entry.GetSwfUrl() and entry.media.category[0].text == "Music":
                            swfURL = entry.GetSwfUrl()
                            message = "Now playing: " + entry.title.text
                            #self.print_entry_details(entry)
                            break
                        #entries.append( "%s %s %s" % (entry.title.text, entry.id.text, entry.GetSwfUrl()) )
                        #entries.append( "%s %s | %s" % (entry.title.text, entry.rating.average, entry.id.text) )
                    except Exception, err:
                        self.write_error(err)
                        continue
                result = ''
                for i in entries:
                    result += '<div>' + i + '</div>'
                #self.response.out.write(result)
            else:
                message = 'Nothing found. Try again.'
        except Exception, err:
            self.write_error(err)
        
        self.write_page(swfURL, message, error)
        
    def print_entry_details(self, entry):
        """ Print out all details of an entry. """
        try:
            # if entry.GetSwfUrl():
            #     self.response.out.write('<object width="425" height="350">'
            #                             '<param name="movie" value="' + entry.GetSwfUrl() + '"></param>'
            #                             '<embed src="' + entry.GetSwfUrl() + 
            #                             '" type="application/x-shockwave-flash" '
            #                             'width="425" height="350"></embed></object>')
            self.write_attrib('Video title: %s' % entry.media.title.text) #@IndentOk
            self.write_attrib('Video published on: %s ' % entry.published.text)
            self.write_attrib('Video description: %s' % entry.media.description.text)
            self.write_attrib('Video category: %s' % entry.media.category[0].text)
            self.write_attrib('Video tags: %s' % entry.media.keywords.text)
            self.write_attrib('Video watch page: %s' % entry.media.player.url)
            self.write_attrib('Video flash player URL: %s' % entry.GetSwfUrl())
            self.write_attrib('Video duration: %s' % entry.media.duration.seconds)
            # non entry.media attributes
            try:
                self.write_attrib('Video geo location: %s' % entry.geo.location())
            except Exception, err:
                self.write_error(err)
            self.write_attrib('Video view count: %s' % entry.statistics.view_count)
            self.write_attrib('Video rating: %s' % entry.rating.average)
            # show alternate formats
            for alternate_format in entry.media.content:
                if 'isDefault' not in alternate_format.extension_attributes:
                    self.write_attrib('Alternate format: %s | url: %s ' % (alternate_format.type
                                                                  , alternate_format.url))
            # show thumbnails
            for thumbnail in entry.media.thumbnail:
                self.write_attrib('Thumbnail url: %s' % thumbnail.url)
                self.write_attrib('<img src="%s" />' % thumbnail.url)
        except Exception, err:
            self.write_error(err)
    
    def write_page(self, swfURL, message, error):
        """ Write the page out to the screen. """
        template_values = {
            'title': TITLE,
            'swfURL': swfURL,
            'message': message,
            'messageDefault': MESSAGE_DEFAULT,
            'error': error
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

    def write_attrib(self, text):
        """ Write output in an html div. """
        self.response.out.write('<div>')
        self.response.out.write(text)
        self.response.out.write('</div>')
    
    def write_error(self, err):
        """ Write out an error in a div. """
        self.response.out.write('<div class="error">')
        self.response.out.write(err)
        self.response.out.write('</div>')


app = webapp2.WSGIApplication([('/', MainPage),
                              ('/play', ResultsPage)],
                              debug=True)
