FROM golang:1.22-alpine as builder
RUN mkdir /app
WORKDIR /app
COPY ./src /app 
RUN CGO_ENABLED=0 GOOS=linux go build -a -tags netgo -o ./service

FROM builder as dev
# Add curl for healthchecks
RUN apk add curl
RUN go get github.com/githubnemo/CompileDaemon
RUN go install github.com/githubnemo/CompileDaemon

FROM alpine:latest
# Copy the binary from the builder
COPY --from=builder /app/service .
ENTRYPOINT [ "./service" ]
