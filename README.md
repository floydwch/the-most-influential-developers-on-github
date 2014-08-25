The Most Influential Developers on Github -- Github Data Challenge 2014
=======================================================================

#Under Construction

#Warning
The result is based on limited data(2014/5/23 ~ 2014/8/23) and not on behalf of Github. The rank might be changed if the collected data increased.

#The Result
## Top 25 Developers in General
1. visionmedia
2. sindresorhus
3. mattt
4. daimajia
5. lexrus
6. onevcat
7. turingou
8. stormzhang
9. youxiachai
10. dodola
11. krzysztofzablocki
12. iiiyu
13. steipete
14. Trinea
15. andrew
16. myell0w
17. jeresig
18. goshakkk
19. neonichu
20. jamiepg1
21. fengmk2
22. romaonthego
23. zenorocha
24. shunwang
25. juliangruber

#Abstract
There are many developers on github, following influential developers is highly beneficial since they spread useful repositories and others.
This survey employed the well-known PageRank algorithm, the data of watching events from the [GitHub Archive](http://www.githubarchive.org/) and users' connections from Github API to mine the most influential developers on Github.

#Data Collection
The watching events data were collected from the [GitHub Archive](http://www.githubarchive.org/) from 2014/5/23 to 2014/8/23 and extracted the repository's name, actor's name and event issued time respectively. The users' connections were collected from the following relationship.
To collect the data, one can issue `python task_grab_watch_events`.

#Build Graphs
Issue `python task_gen_events_graphs`.
In this phrase, every repository's watching event is a 3-tuple(repo, actor, created_time) represented vertex of a directed graph, each vertex direct connects vertices which represent the following users of the vertex which watched the repository relatively early, in the other word, a graph represents the cascade of a repository's watching events. The whole Github's repositories' watching events can form many graphs.

## Edge Weight
To diminish the link effect by time, the edges are weighted by a Fibonacci function, `1.0 / fib(interval + 2)`, the `fib` is the Fibonacci series from 0 and the unit of interval is a day.

#Calculate the Influence
Issue `python task_cal_pagerank` then `python task_cal_influence`.
Every vertex in a graph has a normalized PageRank score, that is, every user can get a score after the user stars a repository, the score will grow up if the user's followers cascading star the repository.
Every user will get a final score by the sum of all scores from repositories the user stars.

## Normalized PageRank
There is a gentle introduction to [Normalized PageRank](https://people.mpi-inf.mpg.de/~kberberi/presentations/2007-www2007.pdf).

# Prerequisites
* [Python 2.7](https://www.python.org/)
* [MongoDB 2.6](http://www.gevent.org/)
* [PyMongo 2.7](http://api.mongodb.org/python/current/)
* [PyGithub 1.25](http://jacquev6.github.io/PyGithub/v1/introduction.html)
* [graph-tool 2.2](http://graph-tool.skewed.de/)
* [Gevent](http://www.gevent.org/)
* [underscore.py](http://serkanyersen.github.io/underscore.py/)
* [more-itertools](https://pythonhosted.org/more-itertools/api.html)
* [arrow](http://crsmithdev.com/arrow/)
