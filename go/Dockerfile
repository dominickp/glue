FROM golang:1.22-alpine as builder
RUN mkdir /app
WORKDIR /app
COPY ./src /app 
RUN CGO_ENABLED=0 GOOS=linux go build -a -tags netgo -o ./service

FROM builder as dev
RUN go get github.com/githubnemo/CompileDaemon
RUN go install github.com/githubnemo/CompileDaemon

FROM alpine:latest
COPY --from=builder /app/service .
ENTRYPOINT [ "./service" ]
