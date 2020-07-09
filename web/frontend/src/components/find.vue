<template>
  <div style="margin-left: 100px">
    <el-row>
      <span style="color: red;float: left">查找所有用户的书籍</span>
      <div align="right">
      <el-button type="primary" @click="open" icon="el-icon-search">查看</el-button>
      <el-button type="success" @click="show" icon="el-icon-refresh">更新</el-button>
      </div>
    </el-row>
    <div style="margin-top: 20px"></div>
    <el-row>
      <el-table
        v-if="is_show"
        :data="books"
        row-style="background-color: #409eff24"
        style="width: 75%;"
        :header-cell-style="{background:'#eef1f6',color:'#606266'}">
        <el-table-column
          prop="id"
          label="编号"
          style="width: 10%">
          <template slot-scope="scope">{{scope.row.pk}}</template>
        </el-table-column>
        <el-table-column
          prop="book_name"
          label="书名"
          style="width: 25%"
          show-overflow-tooltip>
          <template slot-scope="scope">{{ scope.row.fields.title}}</template>
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
          prop="origin"
          label="来源"
          style="width: 10%">
          <template slot-scope="scope">{{judge(scope.row.fields.is_upload)}}</template>
        </el-table-column>
        <el-table-column
          prop="operations"
          label="操作"
          style="width: 10%">
          <template slot-scope="scope">
            <el-button type="text" @click="intro(scope.row.fields.intro)">简介
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>

</template>

<script>
export default {
  name: 'find',
  data () {
    return {
      is_show: true
    }
  },
  props: {
    books: {
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
    judge (upload) {
      if (upload === 1) {
        return '用户上传'
      } else {
        return '网上爬取'
      }
    },
    intro (i) {
      this.$msgbox({
        title: '简介',
        message: i,
        confirmButtonText: '确定'
      })
    },
    open () {
      if (this.login) {
        this.is_show = !this.is_show
      } else {
        this.$message({
          message: '请先登录',
          center: true
        })
      }
      console.log(this.login)
    },
    show () {
      if (this.login) {
        this.$emit('show')
      } else {
        this.$alert('请先登录', '提示信息', {
          confirmButtonText: '确定'
        })
      }
      console.log(this.login)
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
    }
  },
  watch: {
    login () {
      if (this.login === true) {
        this.show()
      }
    }
  }
}
</script>

<style scoped>

</style>
