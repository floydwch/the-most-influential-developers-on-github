# The Most Influential Developers on Github -- Github Data Challenge 2014

*In Progress*

There are many developers on Github, following influential developers is highly beneficial because they usually spread promising repositories.
You might agree the influential developers have the powers to promote repositories on Github by starring, their followers may star successively. 
This survey employed the well-known PageRank algorithm, the data of watching events from the [GitHub Archive](http://www.githubarchive.org/) and users' following relationships from the Github API to mine the most influential developers on Github.

## Disclaimer
The result is based on limited data (2014/1/1 ~ 2014/8/26) and not on behalf of Github. The rank might be changed in case the collected data increased.

## The Result (Tentative)
* [Top 25 Influential Developers in General](#top-general)
* [Top 25 Influential Developers in Python](#top-python)
* [Top 25 Influential Developers in JavaScript](#top-js)
* [Top 25 Influential Developers in Go](#top-go)
* [Top 25 Influential Developers in Ruby](#top-ruby)
* [Top 25 Influential Developers in PHP](#top-php)
* [Top 25 Influential Developers in CSS](#top-css)
* [Top 25 Influential Developers in C](#top-c)
* [Top 25 Influential Developers in C++](#top-cplusplus)
* [Top 25 Influential Developers in Java](#top-java)
* [Top 25 Influential Developers in C#](#top-csharp)
* [Top 25 Influential Developers in Objective-C](#top-objc)
* [Top 25 Influential Developers in Swift](#top-swift)
* [Top 25 Influential Developers in Haskell](#top-haskell)
* [Top 25 Influential Developers in Scala](#top-scala)
* [Top 25 Influential Developers in Clojure](#top-clojure)

## Data Collection
The watching events data were collected from the [GitHub Archive](http://www.githubarchive.org/) from 2014/1/1 to 2014/8/26, the repository's name, the actor's name and the event issued time were extracted respectively. The users' following relationships were collected from the Github API.
To collect the data, issuing `python task_grab_watch_events`. Please make sure the MongoDB has already started, this task will create a database named `github`.

### Github API User Login
Since the task consumes the Github API, please add robots' login names and passwords respectively in the `config.py` under the same directory. 

## Build Graphs
To build graphs, please make sure the watch events have already collected to MongoDB and issue `python task_gen_events_graphs`.
Every repository's watching event can be represented a 3-tuple vertex likes (event's created time, repository's name, actor's name), each vertex has directed edges with its following users' watching events formed vertices who are also stargazers of the repository but prior to the user, in the other words, a graph represents the cascade of a repository's watching events. The whole Github's repositories' watching events form many graphs.

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
### Evolving Graph Animation
Evolving graph animation captures the time series of watching events and their connections, we can then analyze the compactness of a repository's community by observing the forming clusters from animation.

*Evolving graph animation of josephmisiti/awesome-machine-learning*
![](images/awesome-machine-learning%40josephmisiti.gif)
The popular repository `josephmisiti/awesome-machine-learning` was created at `2014-07-15T19:11:19Z`, so the animation can cover its growth. The clusters in the graph might be communities, we can find that there is a main cluster in the center, growing up with the passage of time. There are some frames that most parts of the graph grew up simultaneously perhaps from spread outside the Github. 

*Evolving graph animation of sebyddd/YouAreAwesome*
![](images/YouAreAwesome%40sebyddd.gif)

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
4. steipete
5. andrew
6. mattt
7. Trinea
8. stormzhang
9. lexrus
10. onevcat
11. turingou
12. myell0w
13. youxiachai
14. JakeWharton
15. MatthewMueller
16. jeresig
17. ManuelPeinado
18. igrigorik
19. juliangruber
20. azu
21. xhzengAIB
22. dodola
23. goshakkk
24. jessesquires
25. iiiyu

## <a name="top-python"></a> Top 25 Influential Developers in Python
1. rochacbruno
2. kennethreitz
3. avelino
4. jezdez
5. visionmedia
6. vinta
7. lepture
8. saghul
9. fengmk2
10. dahlia
11. pydanny
12. jd
13. osantana
14. mitsuhiko
15. jefftriplett
16. tonyseek
17. onevcat
18. ionelmc
19. turingou
20. reduxionist
21. ellisonleao
22. numbbbbb
23. jpadilla
24. arthuralvim
25. kkung

## <a name="top-js"></a> Top 25 Influential Developers in JavaScript
1. sindresorhus
2. visionmedia
3. MatthewMueller
4. andrew
5. turingou
6. juliangruber
7. jeresig
8. studiomohawk
9. azu
10. paulirish
11. cheeaun
12. feross
13. mathiasbynens
14. mafintosh
15. fengmk2
16. mcollina
17. eugeneware
18. TooTallNate
19. jwerle
20. igrigorik
21. umaar
22. hij1nx
23. ianstormtaylor
24. hughsk
25. yyx990803

## <a name="top-go"></a> Top 25 Influential Developers in Go
1. visionmedia
2. dgryski
3. mattn
4. Unknwon
5. codegangsta
6. daaku
7. c4milo
8. lunny
9. andrew
10. mreiferson
11. philips
12. rakyll
13. igrigorik
14. spf13
15. samuel
16. crosbymichael
17. pengwynn
18. michaelhood
19. fatih
20. takuan-osho
21. nyarla
22. fgrehm
23. armon
24. bradfitz
25. codahale

## <a name="top-ruby"></a> Top 25 Influential Developers in Ruby
1. andrew
2. mattt
3. ankane
4. JuanitoFatas
5. goshakkk
6. hsbt
7. igrigorik
8. josh
9. amatsuda
10. futoase
11. fgrehm
12. parkr
13. huacnlee
14. flyerhzm
15. miyagawa
16. joker1007
17. pengwynn
18. takkanm
19. jeresig
20. komagata
21. rmoriz
22. rkh
23. akitaonrails
24. luislavena
25. ursm

## <a name="top-php"></a> Top 25 Influential Developers in PHP
1. GrahamCampbell
2. vojtech-dobes
3. Ocramius
4. msurguy
5. lsmith77
6. Zauberfisch
7. taylorotwell
8. harikt
9. pminnieur
10. philsturgeon
11. panique
12. cfoellmann
13. dg
14. Ph3nol
15. barryvdh
16. uzulla
17. jasonlewis
18. fprochazka
19. cordoval
20. JanTvrdik
21. Vrtak-CZ
22. hrach
23. javiereguiluz
24. xboston
25. drgomesp

## <a name="top-css"></a> Top 25 Influential Developers in CSS
1. sindresorhus
2. andrew
3. zenorocha
4. umaar
5. turingou
6. visionmedia
7. jeresig
8. mdo
9. sahat
10. mrmrs
11. gabrielecirulli
12. addyosmani
13. youxiachai
14. mreiferson
15. daimajia
16. studiomohawk
17. vitorbritto
18. jxnblk
19. cheeaun
20. goshakkk
21. joewalnes
22. paulirish
23. tommy351
24. josh
25. JakeWharton

## <a name="top-c"></a> Top 25 Influential Developers in C
1. visionmedia
2. mattn
3. igrigorik
4. jwerle
5. steipete
6. andrew
7. cloudhead
8. clowwindy
9. r-lyeh
10. saghul
11. mattt
12. pengwynn
13. c9s
14. Constellation
15. Trinea
16. daimajia
17. julycoding
18. dgryski
19. rakyll
20. youxiachai
21. JuanitoFatas
22. onevcat
23. stormzhang
24. dodola
25. lexrus

## <a name="top-cplusplus"></a> Top 25 Influential Developers in C++
1. jeresig
2. osteele
3. r-lyeh
4. zcbenz
5. jwerle
6. sindresorhus
7. fabpot
8. andrew
9. hughsk
10. mcollina
11. hij1nx
12. youxiachai
13. satoruhiga
14. visionmedia
15. JacksonTian
16. eugeneware
17. creationix
18. zygmuntz
19. juliangruber
20. BYVoid
21. Constellation
22. daimajia
23. vitaut
24. tmcw
25. springmeyer

## <a name="top-java"></a> Top 25 Influential Developers in Java
1. daimajia
2. stormzhang
3. Trinea
4. JakeWharton
5. ManuelPeinado
6. dodola
7. jgilfelt
8. kyze8439690
9. youxiachai
10. jpardogo
11. mcxiaoke
12. soarcn
13. sd6352051
14. baoyongzhang
15. castorflex
16. snowdream
17. hotchemi
18. wuyexiong
19. vbauer
20. pedrovgs
21. nostra13
22. eveliotc
23. johnkil
24. f2prateek
25. RomainPiel

## <a name="top-csharp"></a> Top 25 Influential Developers in C#
1. shanselman
2. tugberkugurlu
3. leekelleher
4. pierceboggan
5. filipw
6. migueldeicaza
7. mythz
8. Chandu
9. daimajia
10. adamralph
11. punker76
12. indragiek
13. yreynhout
14. Rohansi
15. danielwertheim
16. panesofglass
17. prime31
18. Amrykid
19. codemonkey85
20. hmemcpy
21. nblumhardt
22. joeriks
23. micdenny
24. Redth
25. dbuksbaum

## <a name="top-objc"></a> Top 25 Influential Developers in Objective-C
1. steipete
2. myell0w
3. mattt
4. onevcat
5. lexrus
6. xhzengAIB
7. jessesquires
8. iiiyu
9. romaonthego
10. krzysztofzablocki
11. jamztang
12. supermarin
13. EvgenyKarkan
14. neonichu
15. 0xced
16. chroman
17. cyndibaby905
18. soffes
19. mps
20. indragiek
21. tangqiaoboy
22. nst
23. jpsim
24. xhacker
25. qiaoxueshi

## <a name="top-swift"></a> Top 25 Influential Developers in Swift
1. mattt
2. lexrus
3. onevcat
4. iiiyu
5. romaonthego
6. krzysztofzablocki
7. neonichu
8. tangqiaoboy
9. soffes
10. indragiek
11. AshFurrow
12. hollance
13. chroman
14. myell0w
15. qiaoxueshi
16. rnystrom
17. JacksonTian
18. jessesquires
19. jpsim
20. jakemarsh
21. andreamazz
22. youxiachai
23. supermarin
24. vikmeup
25. mxcl

## <a name="top-haskell"></a> Top 25 Influential Developers in Haskell
1. sdiehl
2. puffnfresh
3. bitemyapp
4. cartazio
5. jfischoff
6. darinmorrison
7. CodeBlock
8. cloudhead
9. rehno-lindeque
10. TimothyKlim
11. egonSchiele
12. rockymadden
13. adinapoli
14. ocharles
15. jonsterling
16. Heather
17. gregwebs
18. tavisrudd
19. taiki45
20. egisatoshi
21. copumpkin
22. robotlolita
23. gelisam
24. kennethreitz
25. myfreeweb

## <a name="top-scala"></a> Top 25 Influential Developers in Scala
1. ryanlecompte
2. xuwei-k
3. jboner
4. softprops
5. ktoso
6. puffnfresh
7. rockymadden
8. mateiz
9. TimothyKlim
10. non
11. milessabin
12. mrdoob
13. hexx
14. dlwh
15. ritschwumm
16. CodeBlock
17. pathikrit
18. rxin
19. krisnal
20. seratch
21. OlegYch
22. hammer
23. velvia
24. tototoshi
25. folone

## <a name="top-clojure"></a> Top 25 Influential Developers in Clojure
1. swannodette
2. yogthos
3. ptaoussanis
4. ztellman
5. mikera
6. michalmarczyk
7. sritchie
8. noprompt
9. nathanmarz
10. mkhoeini
11. brandonbloom
12. mpenet
13. niwibe
14. fogus
15. mkremins
16. magnars
17. alandipert
18. myfreeweb
19. lantiga
20. qerub
21. zcaudate
22. jeluard
23. rockymadden
24. arrdem
25. devn
