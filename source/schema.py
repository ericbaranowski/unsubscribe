from sql import commit

def setup():
  commit('''CREATE TABLE unsubs(id INT NOT NULL AUTO_INCREMENT, \
    url VARCHAR(10000), \
    email VARCHAR(150), \
    PRIMARY KEY (id))''')
    
  commit('''CREATE TABLE readmail(id INT NOT NULL AUTO_INCREMENT, \
    email INT, \
    PRIMARY KEY (id))''')
    
  commit('''CREATE TABLE usercount(id INT NOT NULL AUTO_INCREMENT, \
    another INT, \
    PRIMARY KEY (id))''')

def wipe():
  commit('''drop table unsubs''')
  commit('''drop table readmail''')
  commit('''drop table usercount''')
  setup()