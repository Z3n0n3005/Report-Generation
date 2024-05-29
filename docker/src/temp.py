import jsonpickle
from tasks.paper import Paper

papers = []
for i in range(0, 5):
    paper = Paper()
    papers.append(jsonpickle.encode(paper))

paper = Paper()
encoded = jsonpickle.encode(papers, unpicklable=False)
print(encoded)
print(jsonpickle.decode(encoded))