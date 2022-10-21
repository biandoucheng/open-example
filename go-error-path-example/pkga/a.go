package pkga

import (
	"errors"
)

func FuncA() error {
	err := errors.New("faild run func A")
	return pkgAError.ParsePkgDwtErr("FuncA", err)
}
