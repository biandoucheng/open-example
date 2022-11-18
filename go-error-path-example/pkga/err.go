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
	pkgAError.Init(pkgAError, "对象A执行失败", "内部错误 00A")
}
