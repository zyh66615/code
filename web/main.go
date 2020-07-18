/*
 * @Description: 第一次学习golang语法
 * @Author: zyh
 * @Date: 2020-07-17 21:02:06
 * @LastEditTime: 2020-07-17 22:56:06
 * @LastEditors: zyh
 * @FilePath: /web/main.go
 */ 
package main

import (
	"fmt"
	"time"
	"math"
)

func main()  {
	//第一行
	t1:=time.Now()
	sum:=0
	for i:=0;i<int(math.Pow10(8));i++ {
		sum++
	}
	end:= time.Since(t1)
	fmt.Println(end)
	
}