# Sample solution
# Author: Vijaya Kumar V

import os
import re
import shutil
try:
    import unittest2 as unittest
except ImportError:
    import unittest
    

from subprocess import Popen, PIPE
from bs4 import BeautifulSoup 
import bs4

paragraph_text1 = """
April is the cruellest month, breeding
Lilacs out of the dead land, mixing
Memory and desire, stirring 
Dull roots with spring rain ...
"""

paragraph_text2 = """
The Chair she sat in, like a burnished throne,
Glowed on the marble, where the glass
Held up by standards wrought with fruited vines
From which a golden Cupidon peeped out
(Another hid his eyes behind his wing)
Doubled the flames of sevenbranched candelabra ...
"""

def stripper(text):
    """ Sripper takes a string as input. It 
    removes (1) all manner of whitespace 
    (2) commas (3) periods (4) different kinds
    of br tags and (5) p tags. This is useful
    for checking if the text content of 
    a p or h1-6 matches another while ignoring
    whitespace. 
    
    Should be redone at somepoint with regexp
    to be robust to style attributes and remove
    more internal tags.
    """
    return text.lower().replace('\n',''
                      ).replace('\f',''
                      ).replace('\v',''                      
                      ).replace('\t',''
                      ).replace('\r',''
                      ).replace(' ',''
                      ).replace('</br>',''
                      ).replace('<br/>',''
                      ).replace('<br>',''
                      ).replace(',',''
                      ).replace('.',''
                      ).replace('<p>',''
                      ).replace('</p>',''
                      )

 
class TestProblem2(unittest.TestCase):
        @classmethod
        def setUp(cls):
            """ Function that loads up the html file
            for testing. The file is processed
            using BeautifulSoup and made available
            to the testing through the soup variable.
            """
            cls.html = None
            with open("index.html") as fid:
                cls.html = fid.read()
                cls.soup = BeautifulSoup(cls.html)
            if not cls.html:
                raise Exception('File not read')
                
            
        @classmethod
        def tearDown(cls):
            """ Function for cleaning up after tests:
            You could delete index.html but
            not neccessary
            """
            pass

        # Fill in the tests below. For the ones you are checking
        # for specific content, you should probably "lower"-case
        # your string and the target string so case won't matter,
        # and use the stripper function to take out un-nessary tags

        def test_open_close_html(self):
         try:
		   links = self.soup		
		   print type(links)
		   paragraphs = []
		   for x in links:
    			paragraphs.append(str(x))
		   # converting to str for using it in re			
		   newStr = ''.join(paragraphs)	
		   matchObj = re.search( r'^<html>', newStr)
		   #print matchObj.group()   		
		   self.assertEqual( matchObj.group() , '<html>')
         except AssertionError, e:
           raise Exception("HTML Tag is missing!")
            
	    try:
                assert len(self.soup.find_all('html')) == 1
            except AssertionError, e:
                raise Exception("More than One <html> tag")

        def test_head_in_html(self):
            try:
               self.assertNotEqual(self.soup.html.find("head") , None)
            except AssertionError, e:
                raise Exception("Head is missing!")
            
	    try:
                assert len(self.soup.html.find_all('head')) == 1
            except AssertionError, e:
                raise Exception("More than One <head> tag")

	    
            
        def test_body_in_html(self):
            try:
               self.assertNotEqual(self.soup.html.find("body") , None)
            except AssertionError, e:
                raise Exception("body is missing!")
            
	    try:
                assert len(self.soup.html.find_all('body')) == 1
            except AssertionError, e:
                raise Exception("More than One <body> tag")


        def test_meta(self):
            try:
               self.assertNotEqual(self.soup.html.find("meta") , None)
            except AssertionError, e:
                raise Exception("meta tag is missing!")
	    
            try:
               self.assertEqual(self.soup.html.meta["charset"] , 'UTF-8')
            except KeyError, e:
                raise Exception("UTF-8 is missing!")
	    
            
	    try:
                assert len(self.soup.html.find_all('meta')) == 1
            except AssertionError, e:
                raise Exception("More than One <meta> tag")

                        
        def test_title(self):
            try:
               self.assertEqual(self.soup.html.head.title.string , 'Text Example')
            except AssertionError, e:
                raise Exception("Its not Text Example")


        def test_for_correct_doctype(self):
            try:
               self.assertNotEqual(self.soup.contents[0] , None)
            except AssertionError, e:
                raise Exception("Doctype Not Available")
	   
            

            

        def test_h1_good_contents(self):
            try:
                assert len(self.soup.html.body.find_all('h1')) == 1
            except AssertionError, e:
                raise Exception("More than One <h1> tag")

	    try:
               self.assertEqual(self.soup.html.body.h1.string , 'Text Example')
            except AssertionError, e:
                raise Exception("Its not Text Example")


        def test_h2_good_contents(self):
            try:
                assert len(self.soup.html.body.find_all('h2')) == 1
            except AssertionError, e:
                raise Exception("More than One <h2> tag")

	    try:
               self.assertEqual(self.soup.html.body.h2.string , 'T. S. Eliot: THE WASTE LAND')
            except AssertionError, e:
                raise Exception("Incorrect text")


        def test_h3_good_contents(self):
            
	    try:
		    links = self.soup.html.body.find_all('h3')
                    self.assertEqual(links[0].get_text() , 'I. THE BURIAL OF THE DEAD')
		    self.assertEqual(links[1].get_text() , 'II. A GAME OF CHESS')
		    
            except AssertionError as e:
                raise Exception("Incorrect Text or H3 tag not available")

            
        def test_p1_good_contents(self):
            try:		
		links = self.soup.html.body.find_all('p')           	
		self.assertNotEqual(links[0].get_text() , stripper(paragraph_text1))
			
	    except AssertionError as e:
                raise Exception("Paragraph error")
 


        def test_p2_good_contents(self):
            try:		
		links = self.soup.html.body.find_all('p')           	
		self.assertNotEqual(links[1].get_text() , stripper(paragraph_text2))
			
	    except AssertionError as e:
                raise Exception(e)

        

        def test_breaks(self):
            try:
		
		englpattern = re.compile(r'()' , re.DOTALL)
		links = self.soup.html.body.find_all('p')
		paragraphs = []
		for x in links[0]:
    			paragraphs.append(str(x))
		
		newStr = ''.join(paragraphs)
		assert 'mixing<br>' in newStr != True
		assert 'breeding<br>' in newStr != True
		assert 'stirring <br>' in newStr != True
		pass
		
            except AssertionError as e:
                raise Exception(e)
             
	    try:
		
		englpattern = re.compile(r'()' , re.DOTALL)
		links = self.soup.html.body.find_all('p')
		paragraphs = []
		for x in links[1]:
    			paragraphs.append(str(x))
		
		newStr = ''.join(paragraphs)
		print newStr
		assert 'throne,<br>' in newStr != True
		assert 'glass<br>' in newStr != True
		assert 'vines<br>' in newStr != True
		assert 'out<br>' in newStr != True
		assert 'wing)<br>' in newStr != True
		pass
		
            except AssertionError as e:
                raise Exception(e)


