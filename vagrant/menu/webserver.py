''' docstring '''
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD operations
# from database_setup import Base, Restaurant, MenuItem, RestaurantMenu
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from database_setup import RestaurantMenu

# create session and connect to DB
# engine = create_engine('sqlite:///restaurantmenu.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()
DB = RestaurantMenu()


class WebServerHandler(BaseHTTPRequestHandler):
    ''' docstring '''
    def do_GET(self):
        ''' docstring '''
        try:
            if self.path.endswith('/edit'):
                restaurant_id = self.path.split("/")[2]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurant = DB.select_restaurant_by_id(restaurant_id)
                if restaurant is None:
                    output = ""
                    output += '<h1>Page is curretnly not available</h1>'
                else:
                    output = ""
                    output += '<h1>Write a new name for the "%s" restaurant</h1>' % restaurant.name
                    output += "<form method = 'POST' enctype='multipart/form-data' action = '%s'>" % self.path
                    output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                    output += "<input type='submit' value='Update'>"
                    output += "</form></body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<b><a href='/restaurants/new'>Create a new restaurant</a></b><br>"
                # for item in session.query(Restaurant).all():
                for item in DB.select_all_restaurants():
                    output += "<b>" + item.name + "</b><br>"
                    output += "<a href='/restaurants/%d/edit'>Update</a><br>" % item.id
                    output += "<a href='/restaurants/%d/delete'>Delete</a><br>" % item.id
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''
                <form method='POST' enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like me to say?</h2>
                    <input name="message" type="text" >
                    <input type="submit" value="Submit">
                </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola</h1>"
                output += '''
                <form method='POST' enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like me to say?</h2>
                    <input name="message" type="text" >
                    <input type="submit" value="Submit">
                </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            else:
                self.send_error(404, '"File Not Found" at path "%s"' % self.path)
        except IOError:
            self.send_error(404, 'Exception: "File Not Found" at path "%s"' % self.path)

    def do_POST(self):
        ''' docstring '''
        try:
            if self.path.endswith('/edit'):
                print 'inside'
                restaurant_id = self.path.split("/")[2]
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                result = DB.update_restaurant(restaurant_id, messagecontent[0])
                if result is False:
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Update is failed, try again later!</h1>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                else:
                    self.send_response(301)
                    self.send_header('Location', '/restaurants')
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                return

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                DB.add_new_restaurant(messagecontent[0])
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            else:
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''
                <form method='POST' enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like me to say?</h2>
                    <input name="message" type="text" >
                    <input type="submit" value="Submit">
                </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except:
            pass


def main():
    ''' docstring '''
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
