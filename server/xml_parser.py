import xml.etree.ElementTree as ET
import pandas as pd
import os


class XML2DataFrame:
    '''
    A super hacky parser for XML data to get it into a pandas dataframe
    '''

    def __init__(self, analysis_tags={}, text_tag='l', namespace='',title_tag = 'title', error_file='errors.txt', author_tag='persName'):
        # A dictionary of analysis tags as keys and the list of acceptable inputs as values
        self.analysis_tags = analysis_tags

        # If a namespace if used in xml then '{namespace}' precedes each tag in the tagging
        self.namespace = '{' + namespace + '}'
        self.text_tag = self.namespace + text_tag
        self.author_tag = self.namespace + author_tag
        self.title_tag = self.namespace + title_tag
        self.error_file = error_file
        with open(error_file, 'w+') as output:
            output.write("Error Log \n")



    def xmls_to_dataframe(self, directory):
        '''
        Iterates through files in a directory, parsing each one and adding its
        information to a dataframe
        :param directory: the directory containing the poem XMLs
        :return: a dataframe where each row is a poem and the columns are metadata of the poem and the text
        '''
        # Create a list to hold the column names and append the keys of the analysis tags at first
        col_names = list(self.analysis_tags.keys())
        col_names.append('text')
        col_names.append('author')
        col_names.append('title')
        # Create empty dataframe
        dataframe = pd.DataFrame(columns=col_names)

        # iterate through all files in directory
        for filename in os.listdir(directory):
            filename = directory + filename
            if filename.endswith(".xml"):
                poem = self.parse_xml_file(filename)
                if poem is not None:
                    dataframe = dataframe.append(poem, ignore_index=True)


        return dataframe

    def parse_xml_file(self, xml_file):
        '''
        Hack-ily parses an XML file by going through every element in the XML.
        Each element is checked against the analysis tags given or to see if it contains poem text
        :param xml_file: the XML file to be parsed
        :return: a dictionary where keys are metadata labels and values are the corresponding metadata
        '''

        tree = ET.parse(xml_file)
        # create the dictionary that will be returned
        data = {'text': '', 'author':[], 'title': ''}
        # add all of the analysis labels
        [data.update({tag: None}) for tag in self.analysis_tags.keys()]
        # go through each element in the XML
        for element in tree.iter():
            # check to see if the tag corresponds to poem text
            if element.tag == self.text_tag:
                # concatenate text to current text
                if element.text is not None:
                    data['text'] = data['text'] + element.text + '\n'
            elif element.tag == self.author_tag:
                # append author
                if element.text is not None:
                    data['author'].append(element.text)
                else:
                    self.write_error(xml_file, 'Missing author in author tag')
                    return None
            elif element.tag == self.title_tag:
                # append author
                if element.text is not None:
                    data['title'] = element.text
                else:
                    self.write_error(xml_file, 'Missing title in title tag')
                    return None
            # check to see if the element is an analysis tag
            elif element.attrib.get('ana') is not None:
                # remove the # from the tag
                ana = element.attrib['ana'].replace('#', '')
                # check to see if it is in our list of analysis tags
                if ana in self.analysis_tags.keys():
                    # check to see if it matches the corresponding values the tag can take
                    if element.attrib['type'] in self.analysis_tags[ana]:
                        data[ana] = element.attrib['type']
                    else:
                        self.write_error(xml_file, "analysis tag does not contain proper value")
                        return None
        if data['text'] != '':

            return data
        else:
            self.write_error(xml_file, "no text")
            return None

    def write_error(self, xml_file, message):
        with open(self.error_file, 'a') as output:
            output.write(xml_file + ' ' + message  + '\n')

