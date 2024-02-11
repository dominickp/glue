# glue

This is a trivial app implemented in multiple languages. This service returns a plaintext response showing the active threads in some 4channel discussion boards using [their read-only API](https://github.com/4chan/4chan-API). 

```sh
# Summarize page 5 of Papercraft & Origami (/po/)
curl https://glue-go.dominick.cc/po/5
```
```txt
Page 5: 
 - several pieces. (1 replies)
 - Cybermodels Quake Marine (5 replies)
 - pepakura wisdom (6 replies)
 - Lucky Stars (52 replies)
 - Son of the mask paper craft (4 replies)
 - dirk eisner&#039;s di-excavated octahedron (2 replies)
 - solicitud libro origami pdf, Origami Land- por Tomoko Fuse (202 replies)
 - I&#039;m making a paper gauntlet. My grandmother threw out the o... (16 replies)
 - Please share (34 replies)
 - Hi, I&#039;m looking for this papercraft: (12 replies)
 - Anybody got the files for this Onihime? (4 replies)
 - Printable Origami Paper Patterns (67 replies)
 - hehe, le funny mustache man (20 replies)
 - Looking for for Paper Robots: 25 Fantastic Robots You Can Build ... (2 replies)
 - help with model &amp; general FF bread ig (9 replies)
```

## Purpose
This is a very simple application that could just exist as a [jq](https://jqlang.github.io/jq/) one-liner. For example:
```sh
# Summarize page 5 of Papercraft & Origami (/po/)
curl -s https://a.4cdn.org/po/catalog.json | \
jq -r '.[] | select(.page == 5) | .threads[] |
  " - " + (if .sub == null then .com[:64] else .sub end) +
  " (\(.replies))"'
```

But what this application actually does is not the really point. Most of the code I've worked on for the past 7 years is not visible to a prospective employer. The purpose of this repo is to demonstrate my ability to:
- write readable code and create services in multiple languages
- containerize applications using best practices
- provide development containers to facilitate developing "on-container"
- integrate with third-party APIs
- write integration tests and mock out dependencies
- build load/performance tests
- implement metrics and API monitoring
- document a project and an API
- use CICD and deploy this app somewhere

## Todo
 - Improve logging, code quality
 - Prometheus metrics and grafana dashboard
 - Functional tests, Mocks
 - Unit tests
 - Performance tests
 - API monitoring

## Hosted example

```sh
curl https://glue-go.dominick.cc/g      # go
curl https://glue-py.dominick.cc/po/2   # python
curl https://glue-js.dominick.cc/mu     # javascript
```

## Local example

```sh
# Start the container(s) locally
docker-compose up --build live-python       # python
docker-compose up --build live-go           # go
docker-compose up --build live-javascript   # javascript
```
```sh
# View page 2 of Papercraft & Origami (/po/)
curl http://localhost:8001/po/2             # python
curl http://localhost:8002/po/2             # go
curl http://localhost:8003/po/2             # javascript
```
#### Example output: 
```txt
Page 2
 - PAPER PLANES REFUELED (142)
 - I&#039;m making an effigy of a McDonald&#039;s nightmare golem (96)
 - Low Poly Toucan Papercraft (3)
 - Is there a term for this type of 3D models? I love this one, I&#... (8)
 - The Changs are at it again (25)
 - Paper Cutting General -1 (6)
 - What kind of paper plane is this? (14)
 - The lack of a good /po/+/ck/ thread is absurd...<br><br>So here ... (4)
 - Simple Origami ideas for Potential Soul Mate (24)
 - Engagement Proposal Origami (4)
 - Making some paper stars. (2)
 - RPG/Wargame Terrain Papercrafts? (3)
 - Chamoo323&#039;s Archives (16)
 - Paperboots (3)
 - I need a noa magazine 202 but i dont have a diyzhan invite, can ... (171)
```
