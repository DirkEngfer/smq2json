# Input Data File for script: smq_content.txt
# Output JSON formatted File: smq_content.json


import os, json

def makejson(mygraphLT, graphlen):
   superdoc = {}
   mydoc = {}
   for mytuple in reversed(mygraphLT):
      node, level = mytuple[0], mytuple[1]
      if 0 < level < 6:
         mydoc = superdoc.copy()
         superdoc['subcode'] = mydoc.copy()
         superdoc['code'], superdoc['level'] = node, level
   return superdoc

mypath_smq = os.path.join(os.getcwd(), 'smq_content.txt')
smq_contentfile = open(mypath_smq)
i = -1
codeL = [] # A list of lists, where each sublist contains parent/actual/child smq together with their level (needs to be rewritten: should work also on multiple first level smq + subordinates)
for line in smq_contentfile:
   i = i + 1
   if i > 0:
      smq_code, term_code, level = line.split()
      # Code block 1: works only on a single first level SMQ (needs to be rewritten)
      if i == 1:
         parent_actual_childL = [('', 0), (smq_code, 1), (term_code, 2)]
         if level == '0': codeL.append(parent_actual_childL)
      else:
         for tuplelist in codeL:
            j = -1
            for mytup in tuplelist:
               j = j +1
               if j == 0: parentT = mytup
               if j == 1: actualT = mytup
               if j == 2: childT = mytup
            if smq_code == childT[0]:
               parent_actual_childL =[actualT, (smq_code, childT[1]), (term_code, int(childT[1]) + 1)]
               codeL.append(parent_actual_childL)
               break # => END OF CODE BLOCK 1: At this stage, we have created relationships as graphs (would be nice if SMQs contents file could be delivered as graphs with real bi-directional relationships).
pathLT = []
tempL = []
graphsLT = []
codecopyL = codeL[:]
for nodeLT in codeL:
   for copynodeLT in codecopyL:
      if nodeLT[2][1] <= 2 and nodeLT[2][0] == copynodeLT[0][0] and nodeLT[2][1] == copynodeLT[0][1]:
         pathLT = nodeLT + copynodeLT[1:]
         tempL.append(pathLT)

for nodeLT in tempL:
   found = 0
   for copynodeLT in codecopyL:
      if nodeLT[4][0] == copynodeLT[0][0] and nodeLT[4][1] == copynodeLT[0][1]:
         found = 1
         pathLT = nodeLT + copynodeLT[1:]
         graphsLT.append(pathLT)
   if found == 0:
      graphsLT.append(nodeLT)
graphcopyLT = graphsLT[:]
for graph in graphsLT:
   dobreak = 0
   for copygraph in graphcopyLT:
      if dobreak == 1: break
      if len(graph) < len(copygraph):
         for node, node2 in zip(graph, copygraph):
            if node[0] == node2[0] and node[1] == node2[1]:
               graph = []
               dobreak = 1
               break
jsonpath = os.path.join(os.getcwd(), 'smq_content.json')
jsonfile = open(jsonpath, 'w')
dictL = []
for graphLT in graphsLT:
   graphlen = len(graphLT)
   dictL.append(makejson(graphLT, graphlen))
for item in dictL:
   jsonfile.write(json.dumps(item,indent=4) + '\n')
jsonfile.close()
smq_contentfile.close()
