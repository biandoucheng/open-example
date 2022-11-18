package pkgb

import (
	"go-error-path-example/pkga"

	gperr "github.com/biandoucheng/go-error-path"
)

func FuncB() gperr.ErrorItem {
	err := pkga.FuncA()
	if err != nil {
		return pkgBError.MergeError("FuncB", err)
	}

	return nil
}
