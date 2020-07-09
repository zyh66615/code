<template>
  <div style="margin-top: 20px;margin-left: 100px">
    <el-row style="text-align: left">
      <el-col :span="12">
        <el-autocomplete
          class="inline-input"
          v-model="input"
          :fetch-suggestions="querySearch"
          placeholder="请输入内容"
          :trigger-on-focus="false"
          @keypress.enter.native="addBook"
        />
      </el-col>
      <el-button type="primary" round @click="addBook" icon="el-icon-thumb">提交</el-button>
      <el-button type="danger" round @click="delBook" icon="el-icon-delete">删除</el-button>
      <el-button type="success" round @click="show" icon="el-icon-refresh">更新</el-button>
    </el-row>
    <el-row >
      <el-table
        ref="multipleTable"
        :data="books"
        row-style="background-color: #409eff24"
        style="width: 75%; margin-top: 12px;"
        :header-cell-style="{background:'#eef1f6',color:'#606266'}"
        @selection-change="handleSelectionChange">
        <el-table-column
          type="selection"
          v-if="books.length!==0"
          width="30">
        </el-table-column>
        <el-table-column
          prop="id"
          label="编号"
          style="width: 10%">
          <template slot-scope="scope">{{scope.row.pk}}</template>
        </el-table-column>
        <el-table-column
          prop="book_name"
          label="查找的书名"
          style="width: 10%"
          show-overflow-tooltip>
          <template slot-scope="scope">{{scope.row.fields.book_name}}</template>
        </el-table-column>
        <el-table-column
          prop="title"
          label="真实书名"
          style="width: 15%"
          show-overflow-tooltip>
          <template slot-scope="scope">{{title(scope.row.fields.download, scope.row.fields.title)}}</template>
        </el-table-column>
        <el-table-column
          prop="user_name"
          label="用户名"
          style="width: 10%"
          show-overflow-tooltip>
          <template slot-scope="scope">{{scope.row.fields.user_name}}</template>
        </el-table-column>
        <el-table-column
          prop="add_time"
          label="添加时间"
          style="width: 15%"
          show-overflow-tooltip>
          <template slot-scope="scope">{{format(scope.row.fields.add_time)}}</template>
        </el-table-column>
        <el-table-column
          prop="book_state"
          label="书籍状态"
          style="width: 10%">
          <template slot-scope="scope">{{books_state(scope.row.fields.download, scope.row.fields.book_state,
            scope.row.fields.is_upload)}}
          </template>
        </el-table-column>
        <el-table-column
          prop="operations"
          label="操作"
          style="width: 10%">
          <template slot-scope="scope">
            <el-button v-if="scope.row.fields.download==1"
                       @click="download(scope.row.fields.book_name, scope.row.fields.is_upload, scope.row.fields.user_name)"
                       type="text"
                       size="small">下载
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'book',
  data () {
    return {
      input: '',
      multipleSelection: []
    }
  },
  props: {
    books: {
      type: Array,
      default () {
        return []
      }
    },
    msg: {
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
    }
  },
  methods: {
    handleSelectionChange (val) {
      console.log(val)
      this.multipleSelection = val
    },
    querySearch (queryString, cb) {
      if (this.msg !== undefined) {
        let msg = this.msg
        let results = queryString ? msg.filter(this.createFilter(queryString)) : msg
        // 调用 callback 返回建议列表的数据
        cb(results)
      }
    },
    createFilter (queryString) {
      return (msg) => {
        return (msg.value.toLowerCase().indexOf(queryString.toLowerCase()) > -1)
      }
    },
    title (download, name) {
      if (download === 1) {
        return name
      } else {
        return '无'
      }
    },
    books_state (download, num, upload) {
      if (download === 1) {
        if (upload === 1) {
          return '该书为上传的'
        } else {
          if (num === 1) {
            return '爬取完整'
          } else {
            return '爬取有缺'
          }
        }
      } else {
        return '未爬取到'
      }
    },
    download (BookName, upload, name) {
      this.$emit('Download', BookName, upload, name)
    },
    addBook () {
      this.$emit('addbook', this.input)
      this.input = ''
      this.$refs.multipleTable.clearSelection()
    },
    delBook () {
      if (this.input !== '') {
        this.$emit('delbook', this.input)
        this.input = ''
      } else {
        if (this.multipleSelection.length !== 0) {
          this.$emit('delbook', this.multipleSelection)
          this.$refs.multipleTable.clearSelection()
        } else {
          this.$message({
            message: '请输入文本或选择表项',
            center: true
          })
        }
      }
    },
    format (time) {
      time = time.replace(/T/g, '-')
      time = time.replace(/:/g, '-')
      let T = time.split('-', 6)
      let num = parseInt(T[3])
      T[3] = num.toString()
      let s1 = T[0] + '年' + T[1] + '月' + T[2] + '日'
      let s2 = T[3] + '时' + T[4] + '分' + Math.floor(parseFloat(T[5])) + '秒'
      return s1 + ' ' + s2
    },
    show () {
      if (this.login) {
        this.$emit('show')
        this.$refs.multipleTable.clearSelection()
      } else {
        this.$alert('请先登录', '提示信息', {
          confirmButtonText: '确定'
        })
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }
</style>
