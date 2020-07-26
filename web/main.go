/*
 * @Description: 第一次学习golang语法
 * @Author: zyh
 * @Date: 2020-07-17 21:02:06
 * @LastEditTime: 2020-07-26 21:53:34
 * @LastEditors: zyh
 * @FilePath: /web/main.go
 */
package main

import (
	"fmt"
	"time"
)

func main() {
	//第一行
	t1 := time.Now()
	for i := 1; i < 31; i++ {
		test(i)
	}
	end := time.Since(t1)
	fmt.Println(end)

}
func test(n int) int {
	res := 0
	for i := 0; i < 10000000; i++ {
		if i%n == 0 {
			res++
		}
	}
	return res
}
