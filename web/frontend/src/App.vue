<template>
  <div id="app">
    <el-container>
      <el-header style="height: 60px;width: 100%">
        <el-row v-if="user.is_login">
          <el-col :span="2" :offset="17" style="margin-top: 12px">
            <el-button type="info" @click="logout">退出</el-button>
          </el-col>
          <el-col :span="1">
            <el-avatar v-if="imageURL" fit="cover" :size="70" :src="imageURL" lazy></el-avatar>
            <el-avatar v-else :size="70" icon="el-icon-user-solid"></el-avatar>
          </el-col>
          <el-col :span="1">
            <p style="color: red;font-size: 26px;margin-top: 12px;">{{user.name}}</p>
          </el-col>
          <el-col :span="1">
            <router-view @show_pic="show_pic" :user="this.user.name" name="UploadImage"></router-view>
          </el-col>
        </el-row>
        <el-row v-else>
          <el-col :span="4" offset="20" style="margin-top: 12px">
            <el-button style="margin-left: 60px" type="primary" @click="dialogFormVisible = true">登录</el-button>
            <el-dialog @close="clear" title="登录" :visible.sync="dialogFormVisible">
              <el-form :model="form">
                <el-form-item label="用户名" :label-width="formLabelWidth">
                  <el-input
                    v-model="form.name"
                    placeholder="请输入中文，字母，数字的组合"
                    autocomplete="off"
                    @keypress.enter.native.stop="login"
                  />
                </el-form-item>
                <el-form-item label="密码" :label-width="formLabelWidth">
                  <el-input
                    show-password
                    v-model="form.password"
                    placeholder="请输入字母，数字的组合"
                    autocomplete="off"
                    @keypress.enter.native.stop="login"
                  />
                </el-form-item>
              </el-form>
              <div slot="footer" class="dialog-footer">
                <el-button type="success" @click="clear">取 消</el-button>
                <el-button type="primary" @click="login">确 定</el-button>
              </div>
            </el-dialog>
            <el-button
              style="margin-right: -20px"
              type="success"
              @click="dialogFormVisible1 = true"
            >注册</el-button>
            <el-dialog @close="clear1" title="注册" :visible.sync="dialogFormVisible1">
              <el-form :model="form1">
                <el-form-item label="用户名" :label-width="formLabelWidth">
                  <el-input
                    v-model="form1.name"
                    placeholder="请输入中文，字母，数字的组合"
                    autocomplete="off"
                    @keypress.enter.native="register"
                  />
                </el-form-item>
                <el-form-item label="密码" :label-width="formLabelWidth">
                  <el-input
                    show-password
                    v-model="form1.password"
                    autocomplete="off"
                    placeholder="请输入字母，数字的组合"
                    @keypress.enter.native="register"
                  />
                </el-form-item>
              </el-form>
              <div slot="footer" class="dialog-footer">
                <el-button type="success" @click="clear1">取 消</el-button>
                <el-button type="primary" @click="register">确 定</el-button>
              </div>
            </el-dialog>
          </el-col>
        </el-row>
      </el-header>
      <el-container>
        <el-aside width="200px" style="margin-top: 120px">
          <router-view
            name="menu"
            @first="first"
            :find="is_find"
            :cty="is_community"
            @Back1="fnd"
            @Back2="cty"
          />
          <el-button style="position:fixed" type="primary" @click="download_images">每日下载</el-button>
        </el-aside>
        <el-main style="margin-top: 70px">
          <img src="./assets/logo.png" width="30%" />
          <router-view
            v-if="is_find"
            name="find"
            :login="this.user.is_login"
            @show="show_books"
            :books="booklists"
          />
          <router-view
            ref="community"
            v-if="is_community"
            @answer="reply"
            :user="this.user.name"
            @del="del_post"
            @del_reply="del_reply"
            :login="this.user.is_login"
            :tableData="Data"
            name="community"
            @post="Post"
            @show="show_post"
          />
          <router-view
            v-if="is_first"
            @addbook="add_book"
            @delbook="del_book"
            name="book"
            @Download="download"
            :books="booklist"
            :msg="msg"
            :login="this.user.is_login"
            @show="show_book"
          />
          <el-row v-if="is_first&&user.is_login">
            <el-col :span="12" style="margin-top: 12px; text-align: left">
              <router-view name="UploadText" :user="this.user.name" />
            </el-col>
          </el-row>
        </el-main>
      </el-container>
      <div>
        <el-button
          @click="go_top"
          style="position: fixed;bottom: 60px;right: 180px"
          id="to_top"
          type="success"
          size="small"
          icon="el-icon-caret-top"
        ></el-button>
      </div>
      <el-footer id="footer">
        <div align="right">
          <span style="font-size: 12px">make by 张宇华------Carter</span>
        </div>
        <div align="right">
          <span style="font-size: 12px">
            github地址：
            <a href="https://github.com/zyh66615" style="font-size: 12px">zyh66615</a>
          </span>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      dialogFormVisible: false,
      dialogFormVisible1: false,
      is_find: false,
      is_community: false,
      is_first: true,
      form: {
        name: "",
        password: ""
      },
      form1: {
        name: "",
        password: ""
      },
      user: {
        name: "",
        is_login: false
      },
      formLabelWidth: "120px",
      booklist: [],
      booklists: [],
      msg: [],
      imageURL: "",
      Data: [],
      count: 300
    };
  },
  created() {
    if (sessionStorage.getItem("userMsg")) {
      this.$store.replaceState(
        Object.assign(
          {},
          this.$store.state,
          JSON.parse(sessionStorage.getItem("userMsg"))
        )
      );
      console.log(JSON.parse(sessionStorage.getItem("userMsg")));
      this.user.name = JSON.parse(sessionStorage.getItem("userMsg")).App.name;
      this.user.is_login = JSON.parse(
        sessionStorage.getItem("userMsg")
      ).App.is_login;
      this.booklist = JSON.parse(
        sessionStorage.getItem("userMsg")
      ).App.booklist;
      this.booklists = JSON.parse(
        sessionStorage.getItem("userMsg")
      ).App.booklists;
      this.imageURL = JSON.parse(
        sessionStorage.getItem("userMsg")
      ).App.imageURL;
      this.Data = JSON.parse(sessionStorage.getItem("userMsg")).App.Data;
      this.msg = JSON.parse(sessionStorage.getItem("userMsg")).App.msg;
    }
    let timer = setInterval(() => {
      this.count--;
    }, 1000);
    window.addEventListener("beforeunload", () => {
      if (this.count > 0) {
        sessionStorage.setItem("userMsg", JSON.stringify(this.$store.state));
      } else {
        this.logout();
      }
      clearInterval(timer);
    });
    this.load();
  },
  methods: {
    set(word, keyStr) {
      keyStr = keyStr || "zyh666isthebest!";
      var key = this.CryptoJS.enc.Utf8.parse(keyStr); // Latin1 w8m31+Yy/Nw6thPsMpO5fg==
      var srcs = this.CryptoJS.enc.Utf8.parse(word);
      var encrypted = this.CryptoJS.AES.encrypt(srcs, key, {
        mode: this.CryptoJS.mode.ECB,
        padding: this.CryptoJS.pad.Pkcs7
      });
      return encrypted.toString();
    },
    // 解密
    get(word, keyStr) {
      keyStr = keyStr || "zyh666isthebest!";
      var key = this.CryptoJS.enc.Utf8.parse(keyStr); // Latin1 w8m31+Yy/Nw6thPsMpO5fg==
      var decrypt = this.CryptoJS.AES.decrypt(word, key, {
        mode: this.CryptoJS.mode.ECB,
        padding: this.CryptoJS.pad.Pkcs7
      });
      return this.CryptoJS.enc.Utf8.stringify(decrypt).toString();
    },
    go_top() {
      scrollTo(0, 0);
    },
    download_images() {
      this.$axios({
        method: "get",
        url: "/backend/api/download_images"
      }).then(response => {
        console.log("后台开始下载");
      });
    },
    download(input, upload, name) {
      this.$axios({
        method: "post",
        url: "/backend/api/download",
        data: {
          book_name: input,
          is_upload: upload,
          name: name
        }
        // onDownloadProgress: function (ProgressEvent) {
        //   console.log(ProgressEvent)
        //   const load = ProgressEvent.loaded
        //   const total = ProgressEvent.total
        //   const progress = (load / total) * 100
        //   console.log(progress)
        // }
      }).then(response => {
        if (response.data.error_num === -2) {
          this.$alert(response.data.msg, "提示信息", {
            confirmButtonText: "确定"
          });
          this.timeout();
        } else {
          if (response.data.error_num === -1) {
            console.log("下载失败");
          } else {
            var eleLink = document.createElement("a");
            eleLink.download = input + ".txt";
            eleLink.style.display = "none";
            // 字符内容转变成blob地址
            // var blob = new Blob([response.data])
            eleLink.href = response.data.url;
            // 触发点击
            document.body.appendChild(eleLink);
            eleLink.click();
            // 然后移除
            document.body.removeChild(eleLink);
          }
        }
      });
    },
    fresh() {
      window.location.reload();
    },
    load() {
      const loading = this.$loading({
        lock: true,
        customClass: "my-el-custom-spinner",
        spinner: "sp"
      });
      setTimeout(() => {
        loading.close();
      }, 500);
    },
    del_reply(id) {
      this.$axios({
        method: "post",
        url: "/backend/api/del_reply",
        data: {
          id: id,
          name: this.user.name
        }
      }).then(response => {
        let res = response.data;
        if (response.data.error_num === -2) {
          this.$alert(response.data.msg, "提示信息", {
            confirmButtonText: "确定"
          });
          this.timeout();
        } else {
          if (res.error_num === 0) {
            this.Data = res["list"];
            if (this.Data !== undefined && this.Data.length > 0) {
              this.$store.commit("store_Data", this.Data);
            }
          } else {
            this.$alert("失败", "提示信息", {
              confirmButtonText: "确定"
            });
          }
        }
      });
    },
    reply(content, id) {
      this.$axios({
        method: "post",
        url: "/backend/api/reply",
        data: {
          name: this.user.name,
          id: id,
          content: content
        }
      }).then(response => {
        let res = response.data;
        if (response.data.error_num === -2) {
          this.$alert(response.data.msg, "提示信息", {
            confirmButtonText: "确定"
          });
          this.timeout();
        } else {
          if (res.error_num === 0) {
            this.Data = res["list"];
            if (this.Data !== undefined && this.Data.length > 0) {
              this.$store.commit("store_Data", this.Data);
            }
          } else {
            this.$alert("失败", "提示信息", {
              confirmButtonText: "确定"
            });
          }
        }
      });
    },
    del_post(row) {
      this.$axios({
        method: "post",
        url: "/backend/api/del_post",
        data: {
          id: row.pk,
          name: this.user.name
        }
      }).then(response => {
        let res = response.data;
        if (response.data.error_num === -2) {
          this.$alert(response.data.msg, "提示信息", {
            confirmButtonText: "确定"
          });
          this.timeout();
        } else {
          if (res.error_num === 0) {
            this.Data = res["list"];
            if (this.Data !== undefined && this.Data.length > 0) {
              this.$store.commit("store_Data", this.Data);
            }
            console.log(this.Data);
          } else {
            this.$alert("失败", "提示信息", {
              confirmButtonText: "确定"
            });
          }
        }
      });
    },
    show_post() {
      if (this.user.is_login) {
        this.$axios({
          method: "post",
          url: "/backend/api/show_post",
          data: {
            name: this.user.name
          }
        }).then(response => {
          let res = response.data;
          if (response.data.error_num === -2) {
            this.$alert(response.data.msg, "提示信息", {
              confirmButtonText: "确定"
            });
            this.timeout();
          } else {
            if (res.error_num === 0) {
              this.Data = res["list"];
              if (this.Data !== undefined && this.Data.length > 0) {
                this.$store.commit("store_Data", this.Data);
              }
            } else {
              this.$alert("失败", "提示信息", {
                confirmButtonText: "确定"
              });
            }
          }
        });
      } else {
        this.$alert("请先登录", "提示信息", {
          confirmButtonText: "确定"
        });
      }
    },
    Post(title, input) {
      if (this.user.is_login) {
        this.$axios({
          method: "post",
          url: "/backend/api/post",
          data: {
            name: this.user.name,
            title: title,
            input: input
          }
        }).then(response => {
          let res = response.data;
          if (response.data.error_num === -2) {
            this.$alert(response.data.msg, "提示信息", {
              confirmButtonText: "确定"
            });
            this.timeout();
          } else {
            if (res.error_num === 0) {
              console.log("post success");
              this.show_post();
            } else {
              this.$alert("失败", "提示信息", {
                confirmButtonText: "确定"
              });
            }
          }
        });
      } else {
        this.$alert("请先登录", "提示信息", {
          confirmButtonText: "确定"
        });
      }
    },
    first() {
      this.is_first = true;
      this.is_find = false;
      this.is_community = false;
    },
    fnd() {
      this.is_first = false;
      this.is_find = true;
      this.is_community = false;
    },
    cty() {
      this.is_first = false;
      this.is_find = false;
      this.is_community = true;
    },
    logout() {
      this.$axios({
        method: "get",
        url: "/backend/api/logout",
        params: {
          name: this.user.name
        }
      }).then(response => {
        let res = response.data;
        if (res.error_num === 0) {
          console.log(res.msg);
          this.user.name = "";
          this.user.is_login = false;
          this.booklist = [];
          this.booklists = [];
          this.Data = [];
          this.imageURL = "";
          this.msg = [];
          this.$store.commit("store_Data", this.Data);
          this.$store.commit("store_image", this.imageURL);
          this.$store.commit("store_name", this.user.name);
          this.$store.commit("store_login", this.user.is_login);
          this.$store.commit("store_booklist", this.booklist);
          this.$store.commit("store_booklists", this.booklists);
          this.$store.commit("store_msg", this.msg);
          if (this.is_community) {
            this.$refs.community.zero();
          }
        } else {
          this.$alert("退出失败，请重试", "提示信息", {
            confirmButtonText: "确定"
          });
        }
      });
    },
    timeout() {
      this.user.name = "";
      this.user.is_login = false;
      this.booklist = [];
      this.booklists = [];
      this.Data = [];
      this.imageURL = "";
      this.msg = [];
      this.$store.commit("store_Data", this.Data);
      this.$store.commit("store_image", this.imageURL);
      this.$store.commit("store_name", this.user.name);
      this.$store.commit("store_login", this.user.is_login);
      this.$store.commit("store_booklist", this.booklist);
      this.$store.commit("store_booklists", this.booklists);
      this.$store.commit("store_msg", this.msg);
      if (this.is_community) {
        this.$refs.community.zero();
      }
    },
    clear() {
      this.form.name = "";
      this.form.password = "";
      this.dialogFormVisible = false;
    },
    clear1() {
      this.form1.name = "";
      this.form1.password = "";
      this.dialogFormVisible1 = false;
    },
    login() {
      let reg = /^[\u4e00-\u9fa5A-Za-z0-9]+$/;
      // 用户名
      let reg1 = /^[a-zA-Z0-9]+$/;
      // 密码
      if (reg1.test(this.form.password) && reg.test(this.form.name)) {
        this.Login(this.form.name, this.form.password);
      } else {
        this.$alert("请正确输入", "提示信息", {
          confirmButtonText: "确定"
        });
      }
      this.form.name = "";
      this.form.password = "";
    },
    Login(name, pwd) {
      this.$axios({
        method: "get",
        url: "/backend/api/user_login",
        params: {
          name: name,
          password: this.set(pwd)
        }
      }).then(response => {
        let res = response.data;
        if (res.error_num === 0) {
          this.dialogFormVisible = false;
          this.user.name = res.name;
          this.user.is_login = true;
          this.$store.commit("store_name", this.user.name);
          this.$store.commit("store_login", this.user.is_login);
          this.clear();
          this.show_book();
          this.show_pic();
        } else if (res.error_num === 3) {
          this.$alert("用户不存在或密码错误", "提示信息", {
            confirmButtonText: "确定"
          });
        } else {
          this.$alert(res.msg, "提示信息", {
            confirmButtonText: "确定"
          });
          console.log(res.msg);
        }
      });
    },
    register() {
      let reg = /^[\u4e00-\u9fa5A-Za-z0-9]+$/;
      // 用户名
      let reg1 = /^[a-zA-Z0-9]+$/;
      // 密码
      if (reg1.test(this.form1.password) && reg.test(this.form1.name)) {
        this.Register();
      } else {
        this.$alert("请正确输入", "提示信息", {
          confirmButtonText: "确定"
        });
        this.clear1();
      }
    },
    Register() {
      this.$axios({
        method: "get",
        url: "/backend/api/register",
        params: {
          name: this.form1.name,
          password: this.set(this.form1.password)
        }
      }).then(response => {
        let res = response.data;
        if (res.error_num === 0) {
          console.log(this.form1);
          this.$message({
            message: "注册成功",
            type: "success"
          });
          this.Login(this.form1.name, this.form1.password);
          this.dialogFormVisible1 = false;
          this.clear1();
        } else if (res.error_num === 4) {
          this.$alert("用户名已存在", "提示信息", {
            confirmButtonText: "确定"
          });
          this.form1.name = "";
          this.form1.password = "";
        } else {
          this.$alert("注册失败，请重试", "提示信息", {
            confirmButtonText: "确定"
          });
          this.form1.name = "";
          this.form1.password = "";
          console.log(res.msg);
        }
      });
    },
    show_pic() {
      this.$axios({
        method: "post",
        url: "backend/api/show_pic",
        data: {
          name: this.user.name
        }
      }).then(response => {
        let res = response.data;
        if (response.data.error_num === -2) {
          this.$alert(response.data.msg, "提示信息", {
            confirmButtonText: "确定"
          });
          this.timeout();
        } else {
          if (res.error_num === 0) {
            if (res.img !== "") {
              this.imageURL = res.img + "?=" + Math.random();
              this.$store.commit("store_image", this.imageURL);
            }
          } else {
            this.$alert("未正确获取图片");
          }
          console.log(res.msg);
        }
      });
    },
    show_book() {
      if (this.user.is_login) {
        this.$axios({
          method: "post",
          dataType: "JSON",
          // 接口地址  api-代理+接口端口号之后的其余地址
          url: "/backend/api/show_book",
          data: {
            name: this.user.name
          }
        }).then(response => {
          // 验证数据是否获取到
          let res = response.data;
          if (response.data.error_num === -2) {
            this.$alert(response.data.msg, "提示信息", {
              confirmButtonText: "确定"
            });
            this.timeout();
          } else {
            if (res.error_num === 0) {
              this.booklist = res["list"];
              this.msg = [];
              for (let j = 0, len = this.booklist.length; j < len; j++) {
                this.msg.push({
                  value: this.booklist[j]["fields"]["book_name"]
                });
              }
              if (this.booklist.length > 0) {
                this.$store.commit("store_booklist", this.booklist);
                this.$store.commit("store_msg", this.msg);
              }
            } else {
              this.$alert("显示失败", "提示信息", {
                confirmButtonText: "确定"
              });
              console.log(res.msg);
            }
          }
        });
      }
    },
    show_books() {
      if (this.user.is_login) {
        this.$axios({
          method: "post",
          dataType: "JSON",
          // 接口地址  api-代理+接口端口号之后的其余地址
          url: "/backend/api/show_books",
          data: {
            name: this.user.name
          }
        }).then(response => {
          // 验证数据是否获取到
          let res = response.data;
          let data = [];
          if (response.data.error_num === -2) {
            this.$alert(response.data.msg, "提示信息", {
              confirmButtonText: "确定"
            });
            this.timeout();
          } else {
            if (res.error_num === 0) {
              for (let j = 0, len = res["list"].length; j < len; j++) {
                if (res["list"][j]["fields"]["title"] !== "") {
                  data.push(res["list"][j]);
                }
              }
              this.booklists = data;
              if (this.booklists !== undefined && this.booklists.length > 0) {
                this.$store.commit("store_booklists", this.booklists);
              }
            } else {
              this.$alert("显示失败", "提示信息", {
                confirmButtonText: "确定"
              });
              console.log(res.msg);
            }
          }
        });
      }
    },
    add_book(input) {
      if (this.user.is_login) {
        let reg = /^[\u4e00-\u9fa5A-Za-z0-9,.，。]+$/;
        if (reg.test(input)) {
          this.$axios({
            method: "post",
            url: "/backend/api/add_book",
            data: {
              book_name: input,
              name: this.user.name
            }
          }).then(response => {
            let res = response.data;
            if (response.data.error_num === -2) {
              this.$alert(response.data.msg, "提示信息", {
                confirmButtonText: "确定"
              });
              this.timeout();
            } else {
              if (res.error_num === 0) {
                this.show_book();
              } else if (res.error_num === 1) {
                this.$alert("已存在该书", "提示信息", {
                  confirmButtonText: "确定"
                });
                this.show_book();
              } else {
                this.$alert("添加失败", "提示信息", {
                  confirmButtonText: "确定"
                });
                console.log(res.msg);
              }
            }
          });
        } else {
          this.$alert("请正确输入", "提示信息", {
            confirmButtonText: "确定"
          });
        }
      } else {
        this.$alert("请先登录", "提示信息", {
          confirmButtonText: "确定"
        });
      }
    },
    del_book(input) {
      if (this.user.is_login) {
        if (Array.isArray(input)) {
          let books = {};
          for (let j = 0, len = input.length; j < len; j++) {
            books[input[j]["fields"]["book_name"]] =
              input[j]["fields"]["is_upload"];
          }
          this.$axios({
            method: "post",
            url: "/backend/api/del_book",
            data: {
              book_name: books,
              name: this.user.name
            }
          }).then(response => {
            let res = response.data;
            if (response.data.error_num === -2) {
              this.$alert(response.data.msg, "提示信息", {
                confirmButtonText: "确定"
              });
              this.timeout();
            } else {
              if (res.error_num === 0) {
                this.booklist = res["list"];
                this.msg = [];
                for (let j in this.booklist) {
                  this.msg.push({
                    value: this.booklist[j]["fields"]["book_name"]
                  });
                }
                if (this.booklist !== undefined && this.booklist.length > 0) {
                  this.$store.commit("store_booklist", this.booklist);
                  this.$store.commit("store_msg", this.msg);
                }
              } else {
                this.$alert("删除失败", "提示信息", {
                  confirmButtonText: "确定"
                });
                console.log(res.msg);
              }
            }
          });
        } else {
          let reg = /^[\u4e00-\u9fa5a-zA-Z0-9,.，。]+$/;
          if (reg.test(input)) {
            this.$axios({
              method: "post",
              url: "/backend/api/del_book",
              data: {
                book_name: input,
                name: this.user.name
              }
            }).then(response => {
              let res = response.data;
              if (response.data.error_num === -2) {
                this.$alert(response.data.msg, "提示信息", {
                  confirmButtonText: "确定"
                });
                this.timeout();
              } else {
                if (res.error_num === 0) {
                  this.booklist = res["list"];
                  this.msg = [];
                  for (let j in this.booklist) {
                    this.msg.push({
                      value: this.booklist[j]["fields"]["book_name"]
                    });
                  }
                  if (this.booklist !== undefined && this.booklist.length > 0) {
                    this.$store.commit("store_booklist", this.booklist);
                    this.$store.commit("store_msg", this.msg);
                  }
                } else {
                  this.$alert("删除失败", "提示信息", {
                    confirmButtonText: "确定"
                  });
                  console.log(res.msg);
                }
              }
            });
          } else {
            this.$alert("请正确输入", "提示信息", {
              confirmButtonText: "确定"
            });
          }
        }
      } else {
        this.$alert("请先登录", "提示信息", {
          confirmButtonText: "确定"
        });
      }
    }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
  background-size: 100% 100%;
  overflow-x: scroll;
  overflow-y: scroll;
}

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-thumb {
  background-color: #b4b4b4;
  border-radius: 3px;
}

::-webkit-scrollbar-corner,
::-webkit-scrollbar-track,
::-webkit-scrollbar-track-piece {
  background-color: #ebffed;
}

.my-el-custom-spinner {
  background: url("../static/images/loading.gif");
  background-size: cover;
}

/*element鼠标滑过高亮显示的颜色也太淡*/
.el-table--enable-row-hover .el-table__body tr:hover > td {
  background-color: #004eff1f;
}

.el-upload-list {
  background-color: #ffe265;
}

a:link {
  text-decoration: none;
  color: #b4b4b4;
}

a:hover {
  color: red;
  text-decoration: underline;
}
</style>
