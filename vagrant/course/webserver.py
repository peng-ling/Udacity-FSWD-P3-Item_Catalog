from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys
import re

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///restaurantmenu.db', echo=True)

Base.metadata.bind = engine

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)

session = DBSession()


class Restaurant(Base):

    __tablename__ = "restaurant"

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)


class MenuItem(Base):

    __tablename__ = "menu_item"

    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    restaurant = relationship(Restaurant)


class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:

            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><head><meta charset='utf-8'></head><body>"
                output += '<a href="/new">Add new restaurant!</a>'
                for r in session.query(Restaurant):
                    output += '<h2>' + r.name.encode('utf-8') + '</h2>'
                    output += '<a charset="utf-8" href="/' + \
                        r.name.encode('utf-8') + '/delete/' + str(r.id) + '">Click to delete ' + \
                        r.name.encode('utf-8') + '</a><br/><br/>'
                    output += '<a charset="utf-8" href="/' + \
                        r.name.encode('utf-8') + '/edit/' + str(r.id) + '">Click to edit ' + \
                        r.name.encode('utf-8') + '</a>'
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if "/delete" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html ; charset=utf-8')
                self.end_headers()

                restId = int(re.search('(?<=\/)[0-9]', self.path).group(0))

                print restId

                restToDeleteName = session.query(Restaurant).\
                        filter_by(id=restId)

                session.commit()

                print  restToDeleteName

                output = ""
                output += "<html><head><meta charset='utf-8'></head><body>"
                output += "<form method='POST' enctype = 'multipart/form-data'>"
                output += "<button name='delete'"
                output += "type='submit' value='%s'>" % restToDeleteName.id
                output += "Click if you are sure you want to delete "\
                    + restToDeleteName.name.encode('utf-8') + "</button>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if "/edit" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html ; charset=utf-8')
                self.end_headers()

                restId = int(re.search('(?<=\/)[0-9]', self.path).group(0))
                print restId

                restQuerry = session(
                    Restaurant).filter_by(id=restId).one()

                restName =  restQuerry.name
                restNameUtf =  restName.encode('utf-8')
                print restName
                print restNameUtf
                #print restName.decode('utf-8')

                if restQuerry != []:
                    output = ""
                    output += "<html><head><meta charset='utf-8'></head><body>"
                    output += "<h1>"
                    output += restQuerry.name
                    output += "</h1>"
                    output += "<form method = 'POST' enctype = 'multipart/form-data'"
                    output += "action=/restaurant/edit/%s >" % restId
                    output += "<input name = 'newRestaurantName' type = 'text'"
                    output += "placeholder = '%s'>" % restName
                    output += "<input type='hidden' name = 'newRestaurantName' value='%s'>" % restQuerry.id
                    output += "<input type='submit' value='rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output.encode('utf-8'))
                    print output
                    return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><head><meta charset='utf-8'></head><body>"
                output += "<form method = 'POST' enctype = 'multipart/form-data'"\
                          "action = 'new'> <h2> Enter the name of the restaurant you want to add</h2>"\
                          "<input name = 'new' type = 'text' > <input type = 'submit'"\
                          "value = 'Submit'>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "file not found %s" % self.path)

    def do_POST(self):
        try:

            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))

            print cgi.parse_header(
                self.headers.getheader('content-type'))
            print "-------------------------------"
            print "ctype:"
            print ctype
            print "-------------------------------"

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)

                if fields.get('new') is not None:
                    messagecontent = fields.get('new')
                    print messagecontent

                    restauranttoadd = Restaurant(name=messagecontent[0])
                    session.add(restauranttoadd)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

                if fields.get('newRestaurantName') is not None:
                    messagecontent = fields.get('newRestaurantName')
                    print messagecontent
                    print messagecontent[1]

                    session.query(Restaurant).filter(Restaurant.id == messagecontent[1] )\
                        .update({Restaurant.name: messagecontent[0]}, synchronize_session=False)

                    session.commit()

                    self.send_response(301)
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

                    self.wfile.write(output)
                    return

                if fields.get('delete') is not None:
                    messagecontent = fields.get('delete')
                    print messagecontent
                    print messagecontent[0]

                    session.query(Restaurant).filter(Restaurant.id == messagecontent[0] )\
                        .delete()

                    session.commit()

                    self.send_response(301)
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

                    self.wfile.write(output)
                    return

            return
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server runing on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping web server.."
        server.socket.close()

if __name__ == '__main__':
    main()
