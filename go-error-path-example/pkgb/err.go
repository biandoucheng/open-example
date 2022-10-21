package pkgb

import (
	gperr "github.com/biandoucheng/go-error-path"
)

type PkgBErrorType struct {
	gperr.GoPathErrorType
}

var pkgBError *PkgBErrorType

func init() {
	pkgBError = &PkgBErrorType{}
	pkgBError.Init(pkgBError, "Wrong B")
}
