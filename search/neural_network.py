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
            # Set the default weight for the new connections
            for w in words:
                self.set_weight(w, hid, 0, 1.0 / len(words))
            for u in urls:
                self.set_weight(hid, u, 1, 0.1)

            self.con.commit()

    # Get the all related hidden nodes with the querywords and result urls 
    def get_hnode(self, wordids, urlids):
        res = dict()
        # Select from word_to_hidden
        for wid in wordids:
            cur = self.con.execute('select toid from word_to_hidden \
                    where fromid = %d' % wid)
            for row in cur:
                res.setdefault(row[0], 1)
        # Select from the hidden_to_url
        for uid in urlids:
            cur = self.con.execute('select fromid from hidden_to_url \
                    where toid = %d' % uid)
            for row in cur:
                res.setdefault(row[0], 1)

        return res.keys()

    # Get the neural network info from the database
    def get_nn_info(self, wordids, urlids):
        self.wordids = wordids
        self.urlids = urlids
        self.hiddenids = self.get_hnode(wordids, urlids)
        
        # Output of each layer(input, hidden, out)
        self.word_out = [1.0] * len(wordids)
        self.hidden_out = [1.0] * len(self.hiddenids)
        self.url_out = [1.0] * len(urlids)

        # Matrix of weights from word layer to hidden layer
        self.mat_wh = [[self.get_weight(w, h, 0) for h in self.hiddenids] \
                for w in self.wordids]
        # Matrix of weights from hidden layer to url layer
        self.mat_hu = [[self.get_weight(h, u, 1) for u in self.urlids] \
                for h in self.hiddenids]
    
    # Using feeding forward to get the output
    def get_ff_out(self):
        for i in range(len(self.wordids)):
            self.word_out[i] = 1.0
        # The 1st step to get the hidden out
        for j in range(len(self.hiddenids)):
            res = 0.0
            for i in range(len(self.wordids)):
                res += self.word_out[i] * self.mat_wh[i][j]
            self.hidden_out[j] = tanh(res)
        # The 2nd step to get the url layer out
        for j in range(len(self.hiddenids)):
            res = 0.0
            for i in range(len(self.hiddenids)):
                res += self.hidden_out[i] * self.mat_hu[i][j]
            self.url_out[j] = tanh(res)

        return self.url_out[:]

    # Build the nn model
    def build_nn_model(self, wordids, urlids):
        self.get_nn_info(wordids, urlids)
        return self.get_ff__out()

