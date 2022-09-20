'''

size of user spce 4 MB - 4096KB, page is 4KB
organised how?

size of page: 4KB
blocks: 250 with varying number of pages

memory management (memory tracking): list 
replacement requests (memory allocation): 
page replacement: 

class - page, blocks


system is using pages of equal size
size of main memory: 4MB
size of page: 4MB
organization of main memory: 
'''
import math
import random

class Page:
    def __init__(self, x, n):
        self._pageId = x
        self._processId = n
        self._pageFrame = False
        #Bit values
        self._presentBit = 0
        self._validBit = 0
        self._modifiedBit = 0
        self._accessedBit = 0

    def getPageId(self):
        return self._pageId

    def getProcessId(self):
        return self._processId
    
    def getPageFrame(self):
        return self._pageFrame

    def setPageFrame(self, x):
        if type(x) != type(True):
            raise(TypeError("Error"))
        else:
            self._pageFrame = x

    pageId = property(getPageId)
    processId = property(getProcessId)
    pageFrame = property(getPageFrame, setPageFrame)

    def __eq__(self, other):
        if self.pageId == other.pageId & self.processId == other.processId:
            return True
        else:
            return False

    def __str__(self):
        output = f"PageId: {self.pageId}, ProcessId: {self.processId}"
        return output

class Block:
    def __init__(self, iD, pg):
        self._blockID = iD
        self._process = None
        self._totalPages = pg
        self._pageUsed = 0
        self._memory = pg*4
        self._occupied = False

    def getBlockId(self):
        return self._blockID

    iD = property(getBlockId)

    def getPageUsed(self):
        return self._pageUsed

    def setPageUsed(self, p):
        self._pageUsed = p

    pageUsed = property(getPageUsed, setPageUsed)

    def getProcess(self):
        return self._processId

    def setProcess(self, pId):
        self._processId = pId

    process = property(getProcess, setProcess)

    


class Process:
    def __init__(self, pId, memReq):
        self._pId = pId
        self._memReq = memReq
        self._state = None
        self._blockLocation = None
        #self._pageFrame = 3
        self._pages = []

    def getpId(self):
        return self._pId

    piD = property(getpId)

    def getMemReq(self):
        return self._memReq
    mem = property(getMemReq)

    def getState(self):
        return self._state

    def setState(self, s):
        self._state = s

    state = property(getState, setState)

    def getBlockLocation(self):
        return self._blockLocation

    def setBlockLocation(self, bL):
        self._blockLocation = bL

    blockLocation = property(getBlockLocation, setBlockLocation)

class MemoryBlock:
    def __init__(self, memory):
        #given in KB
        self._memory = memory
        self._freeMemory = memory
        self._blocks = []
        self._occupiedBlocks = []
        self._internalfrag = 0
        #consists of the process id and the memory required
        self._queue = []
        #number of blocks with 2 pages, 4, 8, 16, 32, 64 pages respectively
        self._numBlocks = [8, 10, 14, 12, 16, 2]


    #creates blocks with specific pages and adds it on the blocks list
    def createMem(self):
        iD = 0
        powerOfTwo = 1
        for i in self._numBlocks:
            for pages in range(i):
                self._blocks.append(Block(iD, 2**powerOfTwo))
                iD += 1
            powerOfTwo += 1

    """First Fit Algorithm"""
    def memoryAllocation(self, requiredMemory, pID):
        #lines 93-94 checks if the requiredMemory is within 0-64 (number of pages); 64 the largest number of pages in a block
        block = math.log(requiredMemory/4, 2)
        if block <= len(self._numBlocks):
            if block%1 == 0:
                pageFind = sum(self._numBlocks[:int(block)-1])
                page = sum(self._numBlocks[:int(block)-1])
            else:
                pageFind = sum(self._numBlocks[:int(block)])
                page = sum(self._numBlocks[:int(block)])

            while page < len(self._blocks):
                if requiredMemory <= self._blocks[page]._memory and self._blocks[page]._occupied == False:
                    if requiredMemory - self._blocks[page]._memory == 0:
                        print(f"Process:{pID}\tBlock:{self._blocks[page].iD}\tNo internal fragmentation")
                    else:
                        self._internalfrag += (self._blocks[page]._memory- requiredMemory)
                        print(f"Process:{pID}\tBlock:{self._blocks[page].iD}\tInternal Fragmentation: {self._blocks[page]._memory- requiredMemory}")
                    self._blocks[page]._occupied = True
                    self._occupiedBlocks.append(self._blocks[page])

                    self._blocks[page].pageUsed = requiredMemory//4
                    self._freeMemory -= requiredMemory
                    return self._blocks[page]
                else:
                    page += 1

            self._queue.append((pID, requiredMemory))
            return False, 1, pID
        else:
            return False, 0

            
    def checkQueue(self):
        if len(self._queue) == 0:
            return
        else:
           pId, reqMem = self._queue[0]
           self.memoryAllocation(reqMem, pId)
           self._queue.pop(0)

    def updateBlock(self, block):
        index = self._occupiedBlocks.index(block)
        self._occupiedBlocks.pop(index)
        #update block
        self._blocks[block.iD]._occupied = False
        self._blocks[block.iD]._process = None
        self.checkQueue()

               
class Kernel:
    def __init__(self, memSize):
        self._mem = memSize
        self._memory = MemoryBlock(memSize)
        self._processes = {}
        self._processId = 0
        self._pageFrames = 3
        self._pages = []

        self._memory.createMem()

    def createProcess(self, memReq):
        process = Process(self._processId, memReq)
        self._processes[self._processId] = process
        block = self._memory.memoryAllocation(memReq, self._processId)
        if isinstance(block, Block):
            #a reference to the process
            block.process = process
            process.state = "Ready"
            process.blockLocation = block
            pageId = 0
            #creates pages and stored in the process-pages list
            for pages in range(process.blockLocation.pageUsed):
                process._pages.append(Page(pageId, process.piD))
                pageId += 1
            self._processId += 1
            self._mem -= memReq
            return ((process.piD, len(process._pages)-1))
        else:
            falseStatements = {0: 'Error. Process has not been allocated a memory as the required memory does not fit any block.', 
                            1: "Process was not allocated a memory but added to queue."}
            print(falseStatements[block[1]])


    def freeProcess(self, pId):
        p = self._processes[pId]
        p.state = "Finish"
        self._mem += p.mem
        for page in p._pages:
            del page

        self._memory.updateBlock(p.blockLocation)


    """F I F O"""
    def pageReplacement(self, process, seq):
        #receives a tuple of the process id and the number of pages allocated and then the sequence of the pages as a list to execute
        pId, maxPage = process
        reference = self._processes[pId]._pages
        n = 0   #pointer
        while n < len(seq):

            pg = reference[seq[n]]
            print(f'Accessing page {pg.pageId} from process {pg.processId}')
            if pg.pageFrame == False:
                print("Page Fault")

            if pg.pageFrame:
                print("Page Hit")
            
            if len(self._pages) == self._pageFrames and (pg.pageFrame == False):
                x = self._pages.pop(0)
                x.pageFrame = False
                
            if len(self._pages) < self._pageFrames:# and pg not in self._pages:
                self._pages.append(pg)
                pg.pageFrame = True

            n+= 1
            self.printFifo()   

        self.freeProcess(pId)


    def printFifo(self):
        printRef = ""
        for page in self._pages:
            #printRef += f"{page.pageId} --> "
            printRef += f"{page.pageId} from process {page.processId} --> "

        printRef += "\n"
        print(printRef)

    def getMem(self):
        return self._mem
    
    leftMemory = property(getMem)

    def executeAll(self):
        for process in list(self._processes.keys()):
            p = self._processes[process]
            if p.state == "Ready":
                seq = []
                if len(p._pages) > 8:
                    while len(seq) < 15:
                        seq.append(random.randint(0, len(p._pages)-1))
                else:
                    while len(seq) < 10:
                        seq.append(random.randint(0, len(p._pages)-1))
                
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print(f"Sequence of the process: {seq}")
                self.pageReplacement((p.piD, len(p._pages)-1), seq)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            else:
                self._processes.pop(p.piD)


def test():
    cpu = Kernel(4000)
    p0_Pages = cpu.createProcess(32)
    p1_Pages = cpu.createProcess(233)
    p2_Pages = cpu.createProcess(233)
    p3_Pages = cpu.createProcess(31)
    #returns error1
    cpu.createProcess(230)
    #returns error0
    cpu.createProcess(268)

    cpu.pageReplacement(p0_Pages, [3, 4, 0, 1, 2, 2, 0, 3, 2, 3])
    cpu.pageReplacement(p1_Pages, [4,3,6,5,3,0,6,2,4,5])
    print("****************************************************")
    
    print("****************************************************")
    print(f"CPU has {cpu.leftMemory} KB free memory. {cpu._memory._internalfrag} KB internal fragmentation")
    print("****************************************************")
    print("****************************************************")
    cpu.executeAll()
    
    #print(cpu.leftMemory)


test()