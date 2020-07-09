<template>
  <div style="margin-left: 100px;">
    <el-input
      type="text"
      placeholder="请输入标题"
      v-model="text"
      maxlength="30"
      show-word-limit
      style="width: 50%;display: block;margin-bottom: 20px"
    >
    </el-input>

    <el-input
      :autosize="{minRows:4,maxRows:30}"
      type="textarea"
      resize="none"
      placeholder="请输入内容"
      v-model="textarea"
      maxlength="500"
      show-word-limit
      style="width: 60%;display: inline-block;float: left;"
    >
    </el-input>
    <el-button style="margin:60px 0 0 120px" type="success" round @click="post" icon="el-icon-thumb">提交</el-button>
    <el-row style="margin-top: 30px">
      <el-table
        :data="tableData"
        row-style="background-color: #409eff24"
        :header-cell-style="{background:'#eef1f6',color:'#606266'}"
        style="width: 75%">
        <el-table-column
          fixed
          prop="user_name"
          label="姓名"
          style="width: 18%">
          <template slot-scope="scope">{{scope.row.fields.user_name}}</template>
        </el-table-column>
        <el-table-column
          prop="title"
          label="标题"
          style="width: 18%"
          show-overflow-tooltip>
          <template slot-scope="scope">{{scope.row.fields.title}}</template>
        </el-table-column>
        <el-table-column
          prop="content"
          label="内容"
          style="width: 20%"
          show-overflow-tooltip>
          <template slot-scope="scope">{{scope.row.fields.content}}</template>
        </el-table-column>
        <el-table-column
          prop="add_time"
          label="时间"
          style="width: 18%"
          show-overflow-tooltip>
          <template slot-scope="scope">{{format(scope.row.fields.add_time)}}</template>
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作"
          style="width: 18%">
          <template slot-scope="scope">
            <el-link v-if="judge(scope.row)" @click="del(scope.row)">删除<i class="el-icon-delete"></i></el-link>
            <el-link @click="reply(scope.row)" icon="el-icon-edit">编辑</el-link>
            <el-link @click="look(scope.row)" v-if="judge1(scope.row)">查看<i class="el-icon-view el-icon--right"></i>
            </el-link>
          </template>
        </el-table-column>
      </el-table>
      <el-dialog @close="clear" title="回复内容" :visible.sync="dialogTableVisible" :modal-append-to-body="false">
        <el-table :data="replyData">
          <el-table-column prop="name" label="姓名" width="150">
            <template slot-scope="scope1">{{scope1.row.name}}</template>
          </el-table-column>
          <el-table-column prop="content" label="内容" width="250">
            <template slot-scope="scope1">{{scope1.row.content}}</template>
          </el-table-column>
          <el-table-column prop="time" label="时间">
            <template slot-scope="scope1">{{scope1.row.time}}</template>
          </el-table-column>
          <el-table-column label="操作" fixed="right" prop="id">
            <template slot-scope="scope1">
              <el-link @click="delreply(scope1.row.id)" v-if="judge2(scope1.row.name)">删除<i class="el-icon-delete"></i>
              </el-link>
            </template>
          </el-table-column>
        </el-table>
      </el-dialog>
    </el-row>
    <el-row style="margin-top: 30px">
      <el-col :span="16">
        <el-input v-if="is_answer!==-1" type="textarea"
                  placeholder="请输入回复内容"
                  v-model="content"
                  maxlength="500"
                  show-word-limit
                  style="width: 80%">
        </el-input>
      </el-col>
      <el-col :span="2" offset="2">
        <el-button v-if="is_answer!==-1" type="success" size="large" circle @click="answer">提交</el-button>
      </el-col>
      <el-col :span="2">
        <el-button v-if="is_answer!==-1" type="primary" size="large" circle @click="clean">取消</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'community',
  data () {
    return {
      text: '',
      textarea: '',
      is_answer: -1,
      content: '',
      dialogTableVisible: false,
      replyData: []
    }
  },
  props: {
    tableData: {
      type: Array,
      default () {
        return []
      }
    },
    login: {
      type: Boolean,
      default () {
        return false
      }
    },
    user: {
      type: String,
      default () {
        return ''
      }
    }
  },
  methods: {
    judge2 (name) {
      if (this.user === name) {
        return true
      } else {
        return false
      }
    },
    delreply (id) {
      this.$emit('del_reply', id)
      this.dialogTableVisible = false
    },
    clean () {
      this.is_answer = -1
      this.content = ''
    },
    format (time) {
      if (time) {
        time = time.replace(/T/g, '-')
        time = time.replace(/:/g, '-')
        let T = time.split('-', 6)
        let num = parseInt(T[3])
        T[3] = num.toString()
        let s1 = T[0] + '年' + T[1] + '月' + T[2] + '日'
        let s2 = T[3] + '时' + T[4] + '分' + Math.floor(parseFloat(T[5])) + '秒'
        return s1 + ' ' + s2
      }
      return ''
    },
    clear () {
      this.dialogTableVisible = false
      this.replyData = []
    },
    look (row) {
      this.replyData = row.fields.Reply
      this.dialogTableVisible = true
    },
    zero () {
      this.is_answer = -1
    },
    judge1 (row) {
      if (Array.isArray(row.fields.Reply) && row.fields.Reply.length > 0) {
        return true
      } else {
        return false
      }
    },
    answer () {
      this.$emit('answer', this.content, this.is_answer)
      this.content = ''
      this.is_answer = -1
    },
    reply (row) {
      this.is_answer = row.pk
    },
    judge (row) {
      if (this.user === row.fields.user_name) {
        return true
      } else {
        return false
      }
    },
    del (row) {
      if (row) {
        this.$emit('del', row)
      }
    },
    post () {
      if ((typeof this.text === 'undefined' || this.text === null || this.text === '' || this.text.trim().length === 0) ||
        (typeof this.textarea === 'undefined' || this.textareat === null || this.textarea === '' || this.textarea.trim().length === 0)) {
        this.$alert('请输入正确', '提示信息', {
          confirmButtonText: '确定'
        })
      } else {
        this.$emit('post', this.text, this.textarea)
      }
      this.textarea = ''
      this.text = ''
    },
    show () {
      if (this.login) {
        this.$emit('show')
      }
    }
  },
  mounted () {
    this.show()
  },
  watch: {
    'login': 'show'
  }
}
</script>

<style scoped>

</style>
