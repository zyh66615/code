/*
 * @Description: 第一次学习golang语法
 * @Author: zyh
 * @Date: 2020-07-17 21:02:06
 * @LastEditTime: 2020-07-26 13:58:06
 * @LastEditors: zyh
 * @FilePath: /web/main.go
 */
package main

import (
	"fmt"
	"math"
	"strconv"
	"time"
)

func main() {
	//第一行
	t1 := time.Now()
	res := make([]float64, 0, 200000000)
	for i := 0; i < 200000000; i++ {
		res = append(res, math.Sqrt(float64(i)))
	}
	end := time.Since(t1)
	fmt.Println(end)

}
func test(n1, n2 int) []string {
	res := make([]string, n1)
	for i := 0; i < n1; i++ {
		for j := 0; j < n2; j++ {
			res[i] += strconv.Itoa(j + 1)
		}
	}
	return res
}
