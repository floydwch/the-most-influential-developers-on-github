# The Most Influential Developers on Github -- Github Data Challenge 2014

*In Progress*

There are many developers on Github, following influential developers is highly beneficial because they usually spread promising repositories.
You might agree the influential developers have the powers to promote repositories on Github by starring, their followers may star successively. 
This survey employed the well-known PageRank algorithm, the data of watching events from the [GitHub Archive](http://www.githubarchive.org/) and users' following relationships from the Github API to mine the most influential developers on Github.

## Disclaimer
The result is based on limited data (2014/5/23 ~ 2014/8/23) and not on behalf of Github. The rank might be changed in case the collected data increased.

## The Result (Tentative)
* [Top 25 Influential Developers in General](#top-general)
* [Top 25 Influential Developers in Python](#top-python)
* [Top 25 Influential Developers in JavaScript](#top-js)
* [Top 25 Influential Developers in Go](#top-go)
* [Top 25 Influential Developers in Ruby](#top-ruby)
* [Top 25 Influential Developers in PHP](#top-php)
* [Top 25 Influential Developers in CSS](#top-css)
* [Top 25 Influential Developers in C++](#top-cplusplus)
* [Top 25 Influential Developers in Java](#top-java)
* [Top 25 Influential Developers in Objective-C](#top-objc)
* [Top 25 Influential Developers in Swift](#top-swift)

## Data Collection
The watching events data were collected from the [GitHub Archive](http://www.githubarchive.org/) from 2014/5/23 to 2014/8/23, the repository's name, the actor's name and the event issued time were extracted respectively. The users' following relationships were collected from the Github API.
To collect the data, issuing `python task_grab_watch_events`. Please make sure the MongoDB has already started, this task will create a database named `github`.

### Github API User Login
Since the task consumes the Github API, please add robots' login names and passwords respectively in the `config.py` under the same directory. 

## Build Graphs
To build graphs, please make sure the watch events have already collected to MongoDB and issue `python task_gen_events_graphs`.
Every repository's watching event can be represented a 3-tuple vertex likes (event's created time, repository's name, actor's name), each vertex has directed edges with its following users' watching events formed vertices which are also stargazers of the repository   but prior to the user, in the other words, a graph represents the cascade of a repository's watching events. The whole Github's repositories' watching events form many graphs.

### Edge Weighting
Suppose the actor has less possibility to influence followers by time, to diminish the influence by time, the edges are weighted by a Fibonacci function, `1.0 / fib(interval + 2)`, the `fib` is the [Fibonacci series](http://en.wikipedia.org/wiki/Fibonacci_number) from 0 and the unit of interval is a day. Longer the events' interval, lesser the connection is between events.

## Calculate the Influence
Issue `python task_cal_pagerank` then `python task_cal_influence`.
We can score the influence among users by PageRank since the cascade of watching events can be represented as a directed graph, and so forth we can get the influence of a user by combining scores which are the user got from involved graphs. To reduce noise, the score equals the unit `1` were removed before combining.

### PageRank
[PageRank](http://en.wikipedia.org/wiki/PageRank) is a link analysis algorithm and it assigns a numerical weight to each element of a hyperlinked set of documents, such as the World Wide Web, with the purpose of "measuring" its relative importance within the set.
In this survey, the elements are of the watching events and the links are of the following relationship among actors.

### Normalized PageRank
Since the original PageRank is specific to a single graph, we have to find a way to combine PageRanks from multiple graphs, that is, the PageRank has to be normalized. The PageRank can be normalized by dividing the original PageRank by the least PageRank.
There is a gentle introduction to the [Normalized PageRank](https://people.mpi-inf.mpg.de/~kberberi/presentations/2007-www2007.pdf).

## Data Insights
*In Progress*

## Software Prerequisites
* [Python 2.7](https://www.python.org/)
* [MongoDB 2.6](http://www.gevent.org/)
* [PyMongo 2.7](http://api.mongodb.org/python/current/)
* [PyGithub 1.25](http://jacquev6.github.io/PyGithub/v1/introduction.html)
* [graph-tool 2.2](http://graph-tool.skewed.de/)
* [Gevent](http://www.gevent.org/)
* [underscore.py](http://serkanyersen.github.io/underscore.py/)
* [funcy](https://github.com/Suor/funcy)
* [more-itertools](https://pythonhosted.org/more-itertools/api.html)
* [arrow](http://crsmithdev.com/arrow/)


## <a name="top-general"></a> Top 25 Influential Developers in General
1. visionmedia
2. sindresorhus
3. daimajia
4. lexrus
5. mattt
6. onevcat
7. turingou
8. stormzhang
9. youxiachai
10. dodola
11. juliangruber
12. neonichu
13. iiiyu
14. krzysztofzablocki
15. andrew
16. myell0w
17. Trinea
18. goshakkk
19. MatthewMueller
20. xhzengAIB
21. steipete
22. jeresig
23. fengmk2
24. zenorocha
25. dgryski

## <a name="top-python"></a> Top 25 Influential Developers in Python
1. fengmk2
2. jd
3. kennethreitz
4. rochacbruno
5. vinta
6. turingou
7. numbbbbb
8. avelino
9. mitsuhiko
10. lepture
11. osantana
12. pydanny
13. lexrus
14. youxiachai
15. saghul
16. ionelmc
17. stormzhang
18. jezdez
19. wong2
20. Trinea
21. ZoomQuiet
22. joke2k
23. yueyoum
24. clowwindy
25. reduxionist

## <a name="top-js"></a> Top 25 Influential Developers in JavaScript
1. sindresorhus
2. visionmedia
3. juliangruber
4. turingou
5. MatthewMueller
6. paulirish
7. mafintosh
8. cheeaun
9. hij1nx
10. studiomohawk
11. theamarpatel
12. necolas
13. youxiachai
14. mcollina
15. TooTallNate
16. zenorocha
17. andrew
18. azu
19. jeresig
20. fengmk2
21. umaar
22. gdi2290
23. yyx990803
24. hughsk
25. sofish

## <a name="top-go"></a> Top 25 Influential Developers in Go
1. visionmedia
2. dgryski
3. c4milo
4. daaku
5. Unknwon
6. mattn
7. mreiferson
8. lunny
9. codegangsta
10. spf13
11. juliangruber
12. fatih
13. rakyll
14. titanous
15. deedubs
16. nyarla
17. codahale
18. crosbymichael
19. jeresig
20. takuan-osho
21. tcnksm
22. michaelhood
23. mitchellh
24. philips
25. armon

## <a name="top-ruby"></a> Top 25 Influential Developers in Ruby
1. mattt
2. goshakkk
3. JuanitoFatas
4. ankane
5. andrew
6. hsbt
7. flyerhzm
8. krzysztofzablocki
9. miyagawa
10. rkh
11. akitaonrails
12. josh
13. Maimer
14. hanachin
15. ashchan
16. komagata
17. rpanachi
18. amatsuda
19. lexrus
20. kenn
21. fgrehm
22. takkanm
23. joker1007
24. rafalchmiel
25. rmoriz

## <a name="top-php"></a> Top 25 Influential Developers in PHP
1. Zauberfisch
2. GrahamCampbell
3. Ocramius
4. harikt
5. lsmith77
6. pminnieur
7. cfoellmann
8. javiereguiluz
9. nikic
10. drgomesp
11. philsturgeon
12. panique
13. dimensionmedia
14. pippinsplugins
15. Ph3nol
16. norcross
17. Anahkiasen
18. ronanguilloux
19. marcioAlmada
20. Butochnikov
21. graste
22. everzet
23. xboston
24. fprochazka
25. Big-Shark

## <a name="top-css"></a> Top 25 Influential Developers in CSS
1. sindresorhus
2. jeresig
3. andrew
4. zenorocha
5. visionmedia
6. turingou
7. c4milo
8. daimajia
9. paulirish
10. umaar
11. necolas
12. cheeaun
13. addyosmani
14. pazguille
15. pengwynn
16. youxiachai
17. studiomohawk
18. sofish
19. whoisjake
20. goshakkk
21. onevcat
22. fengmk2
23. tommy351
24. josh
25. qiao

## <a name="top-cplusplus"></a> Top 25 Influential Developers in C++
1. r-lyeh
2. BYVoid
3. visionmedia
4. hij1nx
5. JacksonTian
6. juliangruber
7. simongeilfus
8. tmcw
9. zygmuntz
10. springmeyer
11. mcollina
12. patriciogonzalezvivo
13. miloyip
14. procedural
15. turingou
16. iefserge
17. vitaut
18. jwerle
19. daimajia
20. chloerei
21. ofZach
22. Whitetigerswt
23. saghul
24. stormzhang
25. tommy351

## <a name="top-java"></a> Top 25 Influential Developers in Java
1. daimajia
2. dodola
3. stormzhang
4. kyze8439690
5. vbauer
6. jpardogo
7. youxiachai
8. baoyongzhang
9. ManuelPeinado
10. soarcn
11. Trinea
12. sd6352051
13. JakeWharton
14. nostra13
15. jgilfelt
16. wuyexiong
17. snowdream
18. mcxiaoke
19. pedrovgs
20. youmu178
21. hotchemi
22. iPaulPro
23. castorflex
24. malinkang
25. MichaelEvans

## <a name="top-objc"></a> Top 25 Influential Developers in Objective-C
1. xhzengAIB
2. onevcat
3. myell0w
4. lexrus
5. krzysztofzablocki
6. steipete
7. mattt
8. iiiyu
9. neonichu
10. jessesquires
11. 0xced
12. EvgenyKarkan
13. chroman
14. romaonthego
15. supermarin
16. mps
17. mxcl
18. xhacker
19. jamztang
20. leoru
21. fastred
22. jurre
23. JaviSoto
24. sebyddd
25. uzysjung

## <a name="top-swift"></a> Top 25 Influential Developers in Swift
1. mattt
2. lexrus
3. onevcat
4. iiiyu
5. romaonthego
6. neonichu
7. krzysztofzablocki
8. tangqiaoboy
9. soffes
10. hollance
11. indragiek
12. AshFurrow
13. chroman
14. qiaoxueshi
15. myell0w
16. JacksonTian
17. jakemarsh
18. jpsim
19. rnystrom
20. youxiachai
21. jessesquires
22. 0xced
23. andreamazz
24. nixzhu
25. mxcl
