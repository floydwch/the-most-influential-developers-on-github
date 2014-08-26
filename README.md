The Most Influential Developers on Github -- Github Data Challenge 2014
=======================================================================

#Under Construction

#Warning
The result is based on limited data(2014/5/23 ~ 2014/8/23) and not on behalf of Github. The rank might be changed if the collected data increased.

#The Result (Tentative)
## Top 25 Influential Developers in General
1. visionmedia
2. sindresorhus
3. mattt
4. daimajia
5. lexrus
6. onevcat
7. stormzhang
8. turingou
9. krzysztofzablocki
10. youxiachai
11. steipete
12. dodola
13. jeresig
14. myell0w
15. Trinea
16. fengmk2
17. romaonthego
18. zenorocha
19. iiiyu
20. andrew
21. paulirish
22. juliangruber
23. sofish
24. 0xced
25. c4milo

## Top 25 Influential Developers in Python
1. fengmk2
2. turingou
3. numbbbbb
4. mitsuhiko
5. kennethreitz
6. lexrus
7. youxiachai
8. Trinea
9. stormzhang
10. rochacbruno
11. clowwindy
12. wong2
13. pydanny
14. yueyoum
15. jezdez
16. daimajia
17. Yonaba
18. jacobian
19. jcarbaugh
20. vinta
21. saghul
22. sofish
23. tangqiaoboy
24. avelino
25. ZoomQuiet

## Top 25 Influential Developers in JavaScript
1. visionmedia
2. sindresorhus
3. paulirish
4. juliangruber
5. MatthewMueller
6. turingou
7. necolas
8. sofish
9. jeresig
10. zenorocha
11. stormzhang
12. cheeaun
13. igrigorik
14. hij1nx
15. fengmk2
16. yyx990803
17. youxiachai
18. tommy351
19. TooTallNate
20. andrew
21. contra
22. soulwire
23. tholman
24. mafintosh
25. jakiestfu

## Top 25 Influential Developers in Go
1. visionmedia
2. c4milo
3. dgryski
4. mreiferson
5. codegangsta
6. mattn
7. Unknwon
8. jeresig
9. rakyll
10. titanous
11. deedubs
12. nebiros
13. crosbymichael
14. juliangruber
15. daaku
16. gjohnson
17. josh
18. igrigorik
19. mitchellh
20. fatih
21. philips
22. miyagawa
23. hsbt
24. turingou
25. cloudhead

## Top 25 Influential Developers in CSS
1. sindresorhus
2. jeresig
3. andrew
4. visionmedia
5. zenorocha
6. c4milo
7. paulirish
8. necolas
9. pengwynn
10. cheeaun
11. turingou
12. daimajia
13. pazguille
14. sofish
15. whoisjake
16. youxiachai
17. umaar
18. fengmk2
19. josh
20. qiao
21. addyosmani
22. mdo
23. passy
24. tommy351
25. lifesinger

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
Every user will get a final score by the sum of all scores which are great than the unit score(1) from repositories the user stars.

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
