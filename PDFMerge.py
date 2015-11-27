from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
import argparse
import sys

class Output:
    """Class defined to generate 2 printer friendly pdf files"""
    
    def __init__(self, PagesPerSheet, Debug):
        self.pagesPerSheet = PagesPerSheet
        self.oddFile = PdfFileWriter()
        self.evenFile = PdfFileWriter()
        self.pageCount = 0
        self.sheetCount = 0
        self.debug = Debug
        return

    def isSheetFull(self):
        if self.pageCount % self.pagesPerSheet == 0:
            return True
        else:
            return False

    def getOutputFile(self):
        #
        # Alternate the output files based on what sheet we are on. 
        # Note: if we are doing 2 pages per sheet, we want pages 1,2,5,6... in the odd file
        # and pages 3,4,7,8 in the even file
        #
        # if we are doing 1 page per sheet, we want pages 1,3,5... in the odd file
        # and pages 2,4,6... in the even file
        #
        if self.sheetCount % 2 == 0:
            return self.oddFile
        else:
            return self.evenFile

    #
    # Adds a page to the output. It is smart enough to add the page to
    # either the odd or the even file based on the sheet count
    #
    def addPage(self, page):
        self.getOutputFile().addPage(page)
        self.incrementPageAndSheetCount()

    def incrementPageAndSheetCount(self):
        if self.isSheetFull():
            self.sheetCount = self.sheetCount + 1
        self.pageCount = self.pageCount + 1
        return
            
    def startNewSheet(self):
        print self.debug
        i = 0
        while not self.isSheetFull():
            #
            # The prev. sheet isn't full, but we need to start this page on a new 
            # sheet, fill the current sheet with blank pages to get to the
            # beginning of a new sheet
            #
            self.getOutputFile().addBlankPage()
            self.incrementPageAndSheetCount()
            i = i + 1
        if(self.debug):
            print i, "blank pages added, page count:", self.pageCount
        return

    def getSheetAndPageCount(self):
        return (self.sheetCount, self.pageCount)

    def write(self):
        self.oddFile.write(file("odd.pdf","wb"))
        self.evenFile.write(file("even.pdf","wb"))
        return

    def printState(self):
        print "OutputObj State:"
        print "    PageCount    :", self.pageCount
        print "    SheetCount   :", self.sheetCount
        print "    PagesPerSheet:", self.pagesPerSheet
        return
        
def main():
    parser = argparse.ArgumentParser(description='Joins pdf files and generates an output for odd and even pages')
    parser.add_argument('pdfInput', help='One or more pdf input files', nargs='+')
    parser.add_argument('-d', help='Print debug output from the script run',action = 'store_true') 
    parser.add_argument('-p', type=int, help='Print debug output from the script run', default = 2) 
    
    args = parser.parse_args()

    if args.p == 0:
        print "Pages per sheet cannot be 0"
        sys.exit(1)
    
    pagesPerSheet = args.p
    
    
    debug = args.d
    if(debug):
        print "Debug:", debug
        print "PagesPerSheet:", pagesPerSheet
        print "Input files:",
        print args.pdfInput

    output = Output(pagesPerSheet, debug)
    
    for inPdfFileName in args.pdfInput:
        inFile = PdfFileReader(file(inPdfFileName, "rb"))
        output.startNewSheet()
        if(debug):
            print "Processing file:", inPdfFileName, "with", inFile.getNumPages(), "pages"
            output.printState()
        for page in inFile.pages:
            output.addPage(page)

    output.write()

    print "Wrote ", output.getSheetAndPageCount()[1], "Pages", "in", output.getSheetAndPageCount()[0], "sheets"
    
main()
