<template>
  <div>
    <el-row>
      <el-upload
        class="upload-demo"
        ref="upload"
        :action="get_target()"
        :limit="5"
        :http-request="Upload"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :on-success="handleSuccess"
        :file-list="fileList"
        :on-exceed="handleExceed"
        :before-upload="beforeAvatarUpload"
        :auto-upload="false">
        <el-button slot="trigger" size="small" type="primary" icon="el-icon-document-add">选取文件</el-button>
        <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload" icon="el-icon-upload">
          上传文件
        </el-button>
        <div slot="tip" class="el-upload__tip">只能上传txt文件，且不超过30MB</div>
      </el-upload>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'UploadText',
  data () {
    return {
      target: '/backend/api/upload_text',
      fileList: []
    }
  },
  props: {
    user: {
      type: String,
      default: ''
    }
  },
  methods: {
    get_target () {
      return this.target
    },
    submitUpload () {
      this.$refs.upload.submit()
    },
    handleRemove (file, fileList) {
      console.log(file, fileList)
    },
    handleSuccess () {
      this.$message.success('上传成功!')
    },
    handlePreview (file) {
      console.log(file)
    },
    handleExceed (files, fileList) {
      this.$message.warning(`当前限制选择 5 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    beforeAvatarUpload (file) {
      const isTXT = file.type === 'text/plain'
      const isLt30M = file.size / 1024 / 1024 < 30
      console.log(file.type)
      if (!isTXT) {
        this.$message.error('上传文件只能是 TXT 格式!')
      }
      if (!isLt30M) {
        this.$message.error('上传文件大小不能超过 30MB!')
      }
      return isTXT && isLt30M
    },
    Upload (obj) {
      let param = new FormData()
      const f = new File([obj.file], obj.file.name)
      param.append('file', f)
      param.append('name', this.user)
      param.append('book_name', obj.file.name.slice(0, -4))
      this.$axios({
        method: 'post',
        url: '/backend/api/upload_text',
        processData: false,
        contentType: false,
        data: param
      }).then(response => {
        let res = response.data
        console.log(res)
        if (res.error_num === 0) {
          console.log('upload ok')
          this.fileList = []
        } else {
          console.log(res.msg)
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
