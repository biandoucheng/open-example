package pkgb

import (
	"go-error-path-example/pkga"
)

func FuncB() error {
	err := pkga.FuncA()
	if err != nil {
		return pkgBError.ParsePkgDwtErr("FuncB", err)
	}

	return nil
}
