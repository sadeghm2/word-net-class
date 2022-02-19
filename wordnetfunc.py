# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 16:39:57 2020

@author: ghaher
"""


from gc import collect
from hazm import Normalizer , SentenceTokenizer
from string import punctuation
from networkx import Graph , write_graphml
from networkx.readwrite.graphml import read_graphml
from xlwt import Workbook



class Wordnet():

    '''(((((((((((((((((((((((preprocess)))))))))))))))))))))))))))'''
    def Preprocess(self , conf, source , dest, text_file_name):
        print ("pre processing ...")
        #normalizer = txtmd.InformalNormalizer()
        with open(source + '\\' + text_file_name, encoding="utf-8") as f, open(conf + '\\ascii-ch.txt' , encoding="utf-8") as asc, open(dest + text_file_name[0:-4] + '-ready.txt', "w" , encoding="utf-8") as rdy:
            asci = asc.readline()
            for line in f:
                print('this is line '+ line)
                #print(type(len(line)))
                for i in range(len(line)):
                    for j in range(len(asci)):
                        if line[i] == asci[j]:
                            #print(i)
                            if line[i] != '\n':
                                rdy.write(line[i])
                            else:
                                if line[i-1] == '.':
                                    rdy.write(line[i])
                                else:
                                    rdy.write('.\n')


        print ("done")
        collect()


    '''((((((((((((((((((((((((((((word list creator))))))))))))))))))))))))))))'''
    #import configparser

    def Wordlistcreator(self , dest , text_file_name):
        print ("word list creating ...")
        normalizer = Normalizer()
        with open(dest + text_file_name[0:-4] + '-ready.txt', encoding="utf-8") as txt, open(dest + text_file_name[0:-4] +"-wordlist.txt", "w", encoding="utf-8") as wl:
            for line in txt :
                text = line.translate(str.maketrans({key: " {0} ".format(key) for key in punctuation}))
                text = normalizer.character_refinement(text)

                for word in text.split() :
                    if (word[-1] == '?' or word[-1] == '؟'):
                        wl.write(word[0:-1])
                        wl.write('\n')
                    else:
                        wl.write(word)
                        wl.write('\n')
        print ("done")
        collect()

    '''((((((((((((((((((((((((((((((((((((((stopword-remover))))))))))))))))))))))))))))))))))))))'''
    def Stopwordremover(self ,conf, dest , text_file_name):
        print ("stop word removing ...")


        with open( conf + '\\stopword.txt' , encoding="utf-8") as sw, open(dest + text_file_name[0:-4] +"-wordlist.txt", encoding="utf-8") as train, open(dest + text_file_name[0:-4] + "-NoStopWords.txt", "w", encoding="utf-8") as no_sw:
            stopwords = sw.readlines()
            no_sw.writelines(line for line in train.readlines() if line not in stopwords)
        print ("done")
        collect()

    '''((((((((((((((((((((((((((((((((((((((tf-idf))))))))))))))))))))))))))))))))))))))'''


    def Tfidf(self ,dest, text_file_name):
        print ("term frequency calculation ...")
        report = Graph()
        #listofWord = []
        #count = []
        #i = 0
        with open(dest + text_file_name[0:-4] + "-NoStopWords.txt", encoding="utf-8") as base:
            for line in base:
                line = line[0:-1]
                if line not in report.nodes():
                    report.add_node(line , num = 1)
                else:# ++ tedad tekrar
                    report.nodes[line]["num"] = report.nodes[line]["num"] + 1
        #for node in report.nodes():
        #    print("tekrar " , node , " = ", report.nodes[node]["num"])


        write_graphml(report, dest + text_file_name[0:-4] + '-node-file.graphml')

        print ("done")
        collect()

    '''((((((((((((((((((((((((((((((word-net-creator))))))))))))))))))))))))))))))))))))))'''

    def Wordnetcreator(self ,dest, text_file_name):
        print ("creating word network ...")
        tokenizer = SentenceTokenizer()
        toktemp = []
        h = read_graphml(dest + text_file_name[0:-4] + '-node-file.graphml')

        temp = ""
        #wlist = list(h.nodes())
        # tashkhis jomallat
        with open(dest + text_file_name[0:-4] + "-NoStopWords.txt" , encoding='utf-8') as strm:
            for line in strm:
                temp = temp + line[0:-1] + ' '

            toktemp = tokenizer.tokenize(temp)


            for k in range(len(toktemp)):
                for x in range(len(toktemp[k].split())-1):
                    #print("this is word = " , toktemp[k].split()[x])
                    g = x+1
                    for g in range(len(toktemp[k].split()) - 1):

                        if toktemp[k].split()[x] != toktemp[k].split()[g]:
                            #print("theis are words = " , toktemp[k].split()[x],"  ", toktemp[k].split()[g])
                            if h.has_edge(toktemp[k].split()[x], toktemp[k].split()[g]):
                                print('weight changed')
                                h[toktemp[k].split()[x]][toktemp[k].split()[g]]['weight'] += 1
                                #print("this is weight " , h[toktemp[k].split()[x]][toktemp[k].split()[g]]['weight'])
                            else:
                                #print('weight changed')
                                h.add_edge(toktemp[k].split()[x], toktemp[k].split()[g], weight = 1 + (1/(g-x)))



        write_graphml(h, dest + text_file_name[0:-4] + '-graph-file.graphml')

        print ("done")
        collect()
    '''(((((((((((((((((((((((((selectiveWornet detection))))))))))))))))))))))))))))))))))))))'''
    def selectiveWornet(self,conf,dest, text_file_name):

        #tokenizer = SentenceTokenizer()
        toktemp = []
        select = Graph()

        graph = read_graphml(dest + text_file_name[0:-4] + "-graph-file.graphml")
        temp = ""
        with open(conf + "\\selectedword.txt" , encoding='utf-8') as strm:
            for line in strm:
                print(line)
                toktemp.append(line[0:-1])
                temp = temp + line[0:-1] + ' '

        #toktemp = tokenizer.tokenize(temp)
        print(toktemp)

        select =graph.subgraph(toktemp)
        print(select)

        write_graphml(select, dest + text_file_name[0:-4] + '-selected-graph-file.graphml')

    '''(((((((((((((((((((((((((bigram detection))))))))))))))))))))))))))))))))))))))'''

    def Bigramdetector(self ,dest, text_file_name):
        print ("bigram detection ...")
        #listofWord = []
        bigrams = []

        temp = ""
        #tokenizer = hz.SentenceTokenizer()
        graph = read_graphml(dest + text_file_name[0:-4] + "-graph-file.graphml")

        with open(dest + text_file_name[0:-4] + "-ready.txt", encoding="utf-8") as base:
            for line in base:
                temp = temp + ' ' +line

        toktemp = temp.split()

        with open(dest + text_file_name[0:-4] + "-bigram.txt", "w", encoding="utf-8") as bgrm:
            for j in range(len(toktemp)):
                try:
                    if graph[toktemp[j]][toktemp[j+1]]['weight'] >= 4:
                         if str(toktemp[j])+' '+str(toktemp[j+1]) not in bigrams and str(toktemp[j+1])+' '+str(toktemp[j]) not in bigrams:
                             bigrams.append(str(toktemp[j])+' '+str(toktemp[j+1]))
                             #print(toktemp[j] , " and " , toktemp[j+1])
                             #temp = listofWord[j] + " and "  listofWord[j+1]
                             bgrm.write(toktemp[j])
                             bgrm.write(" ")
                             bgrm.write(toktemp[j+1])
                             bgrm.write(" ")
                             #bgrm.write(str(h[toktemp[j]][toktemp[j+1]]['weight']))
                             bgrm.write('\n')

                except:
                        pass
        #print(i)


        print ("done")
        collect()

    '''(((((((((((((((((((((((((bigram conceptual network)))))))))))))))))))))))))))'''
    def Bigramwordnet(self ,dest, text_file_name):
        print ("create bigram word network ...")
        tokenizer = SentenceTokenizer()
        toktemp = []
        bgrmtemp = []
        h = read_graphml(dest + text_file_name[0:-4] + '-graph-file.graphml')

        temp = ""
        #wlist = list(h.nodes())
        # tashkhis jomallat
        with open(dest + text_file_name[0:-4] + '-NoStopWords.txt' , encoding='utf-8') as strm , open(dest + text_file_name[0:-4] + "-bigram.txt", encoding="utf-8") as bgrm:
            for line in strm:
                temp = temp + line[0:-1] + ' '

            for line in bgrm:
                bgrmtemp.append(line[0:-1])

        toktemp = tokenizer.tokenize(temp)
        #print("len tok = ", len(toktemp))
        #print(toktemp.split())
        with open(dest + text_file_name[0:-4] + '-bi-report.txt', 'w' , encoding='utf-8') as brpt:
            for k in range(len(toktemp)):
                #print("k = " , k)
                flag = 0
                #print("this is sentence = " , toktemp[k])
                #print("len = " , len(toktemp[k].split()))
                sentemp = toktemp[k].split()
                for x in range(len(sentemp)-1):
                    flag = 0
                    #print("x = " , x)
                    #print("this is word = " , toktemp[k].split()[x])
                    for g in range(x+1,len(sentemp)-1):
                        #print("g = " , g)
                        if sentemp[x] != sentemp[g]:
                            #print('g-x = ', g-x )
                            if (g-x == 1) : #Continuous concept
                                #print('g-x true = ', g-x )
                                strtemp = str(sentemp[x]) + ' ' + str(sentemp[g])
                                for l in range(len(bgrmtemp)):
                                    #print(bgrmtemp[l] , ' and ', strtemp)


                                    if bgrmtemp[l][0:-1] == strtemp :
                                        brpt.write(bgrmtemp[l][0:-1] + 'and' + strtemp + '\n')
                                        #print("###########3 ",bgrmtemp[l] , ' and ', strtemp)
                                        sentemp[g] = strtemp
                                        #print("str is ", sentemp[g])
                                        flag = 1
                                        break
                        if flag == 1:
                            #print("flag=1")
                            break

                        #print("theis are words = " , sentemp[x],"  ", sentemp[g])
                        if h.has_edge(sentemp[x], sentemp[g]):
                            h[sentemp[x]][sentemp[g]]['weight'] += 1
                            #print("this is weight " , h[toktemp[k].split()[x]][toktemp[k].split()[g]]['weight'])
                        else:
                            h.add_edge(sentemp[x], sentemp[g], weight = 1)



        write_graphml(h, dest + text_file_name[0:-4] + '-graph-file-bigram.graphml')

        print ("done")
        collect()

    '''((((((((((((((((((((((((((((((((best sentence)))))))))))))))))))))))))))))))'''


    def Bestsentence(self ,dest , text_file_name):
        print ("best sentence detection ...")
        h = read_graphml(dest + text_file_name[0:-4] + '-graph-file.graphml')

        tokenizer = SentenceTokenizer()
        temp = ''
        with open(dest + text_file_name[0:-4] + '-ready.txt', encoding='utf-8') as txt:
            for line in txt:
                temp = temp + line[0:-1] + ' '

        toktemp = tokenizer.tokenize(temp)
        book = Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Sheet 1")
        sheet1.write(0,0,"text")
        sheet1.write(0,1,"score")
        sheet1.write(0,2,"average score")
        sheet1.write(0,3,"order")
        for k in range(len(toktemp)):
            bufnod = 0
            bufedg = 0
            """sentence len"""
            senlen = len(toktemp[k].split())-1
            #print("this is sentence = " , toktemp[k])
            #print("len = " , len(toktemp[k].split()))
            for x in range(senlen):
                if h.has_node(toktemp[k].split()[x]):
                    bufnod = bufnod + h.nodes[toktemp[k].split()[x]]['num']
                #print("this is word = " , toktemp[k].split()[x])
                g = x+1
                for g in range(len(toktemp[k].split()) - 1):

                    if toktemp[k].split()[x] != toktemp[k].split()[g]:
                        #print("theis are words = " , toktemp[k].split()[x],"  ", toktemp[k].split()[g])
                        if h.has_edge(toktemp[k].split()[x], toktemp[k].split()[g]):
                            bufedg = bufedg + h[toktemp[k].split()[x]][toktemp[k].split()[g]]['weight']
            score = (bufnod * bufedg)/1000
            if senlen != 0:
                avgscore = score/senlen
            #print("sentence : " , toktemp[k], " and score = " ,score)
            if score != 0.0 :
                sheet1.write(k+1,0,toktemp[k])
                sheet1.write(k+1,1,score)
                sheet1.write(k+1,2,avgscore)
                sheet1.write(k+1,3,k)

        book.save(dest + text_file_name[0:-4] + '-sentences.xls')

        print ("done")
        collect()
        '''(((((((((((((((((((((((((((((graph-similarity)))))))))))))))))))))))))))))'''
    def GraphSimilarity(self,a,b):
        self.ndsmlr = 0
        self.edgsmlr = 0
        #a = Graph()
        #b = Graph()
        '''calculate node similarity'''
        for node in a:
            #print(node)
            if b.has_node(node):
                #print(node)
                self.ndsmlr += 1
                #print(ndsmlr)

        '''calculate edge similarity'''
        edg = list(a.edges)
        for i in range(len(edg)):

            if b.has_edge(edg[i][0],edg[i][1]):
                #print (edg[i])
                self.edgsmlr += 1
                #print(edgsmlr)
        self.smlpercent = 0

        if self.ndsmlr != 0 and self.edgsmlr !=0:
            '''node similarity percent'''
            self.ndsmlpercent = (self.ndsmlr/(a.number_of_nodes()+b.number_of_nodes()-self.ndsmlr))*100

            '''edge similarity percent'''
            self.edgsmlpercent = (self.edgsmlr/(a.number_of_edges() + b.number_of_edges() - self.edgsmlr))*100

            '''entire similarity percent'''
            self.smlpercent = (self.ndsmlpercent + 2*self.edgsmlpercent)/3


