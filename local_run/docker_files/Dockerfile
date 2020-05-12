FROM golang:1.14-alpine

ENV PATH="${GOPATH}/bin:${PATH}"

RUN mkdir -p /go/src/github.com/kaspanet/kaspad

WORKDIR /go/src/github.com/kaspanet/kaspad

RUN apk add --no-cache curl git openssh binutils gcc musl-dev tini bash
# Allow delve to run on Alpine based containers.
RUN apk add --no-cache libc6-compat

RUN go get github.com/derekparker/delve/cmd/dlv

COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .

RUN GOOS=linux go build -gcflags "all=-N" -a -installsuffix cgo -o kaspad .

ENTRYPOINT [ "/sbin/tini", "--" ]
