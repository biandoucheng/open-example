package pkga

import (
	"errors"

	gperr "github.com/biandoucheng/go-error-path"
)

func FuncA() gperr.ErrorItem {
	err := errors.New("faild run func A")
	return pkgAError.ParseError("FuncA", err)
}
