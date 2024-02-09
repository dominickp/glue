# glue

This is a trivial app implemented in multiple languages. This service returns a CLI response showing the active discussion threads in some SFW 4channel boards using the [4chan-API](https://github.com/4chan/4chan-API). 

## Purpose
Most of the code I've worked on for the past 7 years is not visible to a prospective employer.

The purpose of this repo is to demonstrate my ability to:
- write readable code and create services in multiple languages
- containerize applications using best practices
- provide development containers to facilitate developing "on-container"
- integrate with third-party APIs
- write integration tests and mock out dependencies
- build load/performance tests
- document a project and an API
- use CICD and deploy this app somewhere

## Local example

```sh
# Start the container(s) locally
docker-compose up --build live-python   # python
docker-compose up --build live-go       # go
```
```sh
# View page 2 of Papercraft & Origami (/po/)
curl http://localhost:8001/po/2         # python
curl http://localhost:8002/po/2         # go
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
