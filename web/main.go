/*
 * @Description: 第一次学习golang语法
 * @Author: zyh
 * @Date: 2020-07-17 21:02:06
 * @LastEditTime: 2020-07-25 20:28:29
 * @LastEditors: zyh
 * @FilePath: /web/main.go
 */
package main

import (
	"fmt"
	"reflect"
	"strconv"
	"time"
)

func main() {
	//第一行
	t1 := time.Now()
	s := test(5, 10)
	fmt.Println(reflect.TypeOf(s))
	for i := 0; i < len(s); i++ {
		fmt.Println(s[i])
	}
	end := time.Since(t1)
	fmt.Println(end)

}
func test(n1, n2 int) []string {
	res := make([]string, n1)
	for i := 0; i < n1; i++ {
		for j := 0; j < n2; j++ {
			res[i] += strconv.Itoa(j+1)
		}
	}
	return res
}
