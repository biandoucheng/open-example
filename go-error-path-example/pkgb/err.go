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
	pkgBError.Init(pkgBError, "对象 B 执行失败", "内部错误 00B")
}
