from sql import commit

def setup():
  commit('''CREATE TABLE unsubs(id INT NOT NULL AUTO_INCREMENT, \
    url VARCHAR(10000), \
    email VARCHAR(150), \
    PRIMARY KEY (id))''')
    
  commit('''CREATE TABLE read(id INT NOT NULL AUTO_INCREMENT, \
    email INT, \
    PRIMARY KEY (id))''')