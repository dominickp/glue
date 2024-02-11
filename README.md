# glue <!-- omit in toc -->

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

## Table of contents <!-- omit in toc -->
- [Purpose](#purpose)
- [Todo](#todo)
- [Deployment](#deployment)
- [Functional testing](#functional-testing)
- [Local example](#local-example)


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
 - Unit tests
 - Performance tests
 - API monitoring
 - Improve this readme and document what is happening here so people don't need to dig into the code to understand

## Deployment
I have an instance of each implementation deployed to my Oracle Cloud Infrastructure (OCI) tenancy. 

```sh
curl https://glue-go.dominick.cc/g      # go
curl https://glue-py.dominick.cc/po/2   # python
curl https://glue-js.dominick.cc/mu     # javascript
```

For those curious, this repo using GitHub Actions to publish [packages](https://github.com/dominickp?tab=packages&repo_name=glue) (the docker images of the applications) to GitHub Container Registry (GHCR) with tag `main` (named after the branch). I'm deploying containers in OCI with [Portainer](https://www.portainer.io/) which pulls prebuilt images from GHCR. I also have a [Watchtower](https://containrrr.dev/watchtower/) container which scans for updates the images in GHCR at the `main` tag, and if detected, will automatically pull and re-deploy the containers. 

<img src="./docs/img/glue-deployment.drawio.png">

Another alternative would be to have GitHub Actions deploy to Portainer directly, which would give me a much more normal CICD pipeline. I didn't do this because currently my Portainer instance is only accessible via my [Tailscale](https://tailscale.com/) network and I'd have to expose it to the Internet to allow GitHub Actions access it. But I'm sure I could whitelist GitHub to access it with network policies.

## Functional testing
This repo includes mock and live functional testing. Some people would instead use these terms: integration testing, API testing, component testing. Regardless, these are external tests of the API via HTTP requests. These types of tests are nice for a project like this because we can write one test and use it on all of the existing implementations (or future ones if I add more languages) since they should provide the exact same API. 

<img src="./docs/img/glue-functional-testing.drawio.png">

The live-functional-tests just do some very basic checks to ensure the live containers are appropriately configured for their dependencies. 

The majority of the logic is tested in the mock-functional-test, where we control everything that the fanout is doing. For example, we can mock out a specific set of data to be returned and write our tests against it. We won't have to worry about data changing in the live dependency that breaks out tests.

Furthermore, we can inject some faults into the system to see how our application reacts when encountering problems. The way I've done it here is to use (abuse?) the "X-Forwarded-For" (XFF) header, which is forwarded to the dependency so they can see the originating IP (sometimes this is required to support rate limiting when proxies are involved). I've configured my "mock-4channel" application to delay its response when it sees the XFF signal `4c-mock-delay=N` with "N" being the number of seconds to delay. This means, the person writing mock-functional-tests can just alter the XFF being sent into the application which allows them easily test the timeout logic.

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
