'''This module is used to store the information of neural network.''' 
from math import tanh
from pysqlite3 import dbapi3 as sqlite

class nnet:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)
        
    def __del__(self):
        self.con.close()

    def table_of_model(self):
        self.con.execute('create table hidden_layer(hnode)')
        self.con.execute('create table word_to_hidden(fromid, toid, weight)')
        self.con.execute('create table hidden_to_url(fromid, toid, weight)')
        self.con.commit()
    
    # Get the connection strength(weight) of one layer in this neural network 
    def get_weight(self, fromid, toid, layer):
        # Two layers of the network
        if layer == 0:
            table = 'word_to_hidden'
        if layer == 1:
            table = 'hidden_to_url'
        # Get the weight of the layer
        result = self.con.execute('select weight from %s \
                where fromid = %d and toid = %d' \
                % (table, fromid, toid)).fetchone()
        # Default weight if each layer
        if result == None:
            if layer == 0: return -0.2
            if layer == 1: return 0.0

        return result[0]

    # Look at if the connection exists, and update the weight of the connection
    def set_weight(self, fromid, toid, layer, weight):
        if layer == 0:
            table = 'word_to_hidden'
        if layer == 1:
            table = 'hidden_to_url'

        result = self.con.execute('select rowid from table = %s \
                where fromid = %d and toid = %d' \
                % (table, fromid, toid)).fetchone()
        if result = None:
            self.con.execute('insert into %s (fromid, toid, weight) \
                    values (%d, %d, %d)' % (table, fromid, toid, weight))
        else:
            rowid = result[0]
            self.con.execute('update %s set weight = %d where rowid = %d' \
                    % (table, weight, rowid)

    # Generate the hidden layer
    def generate_hidden(self, words, urls):
        if len(words) > 3:
            return None
        hnode = '_'.join(sorted([str(wi) for wi in words]) 
        result = self.con.execute('select rowid from hidden_layer \
                where hnode = %s' % (hnode)).fetchone()

        # If hasn't builded the connection
        if result == None:
            cur = self.con.execute('insert into hidden_layer (hnode) \
                    values (%s)' % hnode)
            hid = cur.lastrowid
            
            for w in words:
                self.set_weight(w, hid, 0, 1.0 / len(words))
            for u in urls:
                self.set_weight(hid, u, 1, 0.1)

            self.con.commit()


