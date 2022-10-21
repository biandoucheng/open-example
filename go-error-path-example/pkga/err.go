package pkga

import (
	gperr "github.com/biandoucheng/go-error-path"
)

type PkgAErrorType struct {
	gperr.GoPathErrorType
}

var pkgAError *PkgAErrorType

func init() {
	pkgAError = &PkgAErrorType{}
	pkgAError.Init(pkgAError, "Wrong A")
}
