# glue

This is a trivial app implemented in multiple languages. This service returns a CLI response showing the active discussion threads in some SFW 4channel boards.

## Purpose
Most of the code I've worked on for the past 7 years is not visible to a prospective employer.

The purpose of this repo is to demonstrate my ability to:
- write readable code in multiple languages
- containerize applications
- structure development containers to develop "on-container"
- integrate with third-party APIs
- write integration tests and mock out dependencies
- document a project
- use CICD and deploy this app somewhere

## Local example

```sh
# Start the container locally
docker-compose up --build live-python
```
```sh
# View page 2 of Papercraft & Origami (/po/)
curl http://localhost:8001/po/2
```
```txt
Page 2: 
 - PAPER PLANES REFUELED (142 replies)
 - I&#039;m making an effigy of a McDonald&#039;s nightmare golem... (96 replies)
 - Low Poly Toucan Papercraft (3 replies)
 - Is there a term for this type of 3D models? I love this one, I&#... (8 replies)
 - The Changs are at it again (25 replies)
 - Paper Cutting General -1 (6 replies)
 - What kind of paper plane is this?... (14 replies)
 - The lack of a good /po/+/ck/ thread is absurd...<br><br>So here ... (4 replies)
 - Simple Origami ideas for Potential Soul Mate (24 replies)
 - Engagement Proposal Origami (4 replies)
 - Making some paper stars. (2 replies)
 - RPG/Wargame Terrain Papercrafts? (3 replies)
 - Chamoo323&#039;s Archives (16 replies)
 - Paperboots (3 replies)
 - I need a noa magazine 202 but i dont have a diyzhan invite, can you guys help me out? (171 replies)
```
