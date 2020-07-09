<template>
  <div>
    <el-row>
      <el-upload
        class="avatar-uploader"
        :action="get_target()"
        :http-request="Upload"
        :show-file-list="false"
        :before-upload="beforeAvatarUpload">
        <el-button type="primary" style="margin-top: 12px" icon="el-icon-upload">上传头像</el-button>
      </el-upload>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'UploadImage',
  data () {
    return {
      target: '/backend/api/upload_image',
      uploadVisible: false
    }
  },
  props:
    {
      imageUrl: {
        type: String,
        default: ''
      },
      user: {
        type: String,
        default: ''
      }
    },
  methods: {
    get_target () {
      return this.target
    },
    Upload (obj) {
      console.log(obj)
      let param = new FormData()
      const f = new File([obj.file], this.user + '.jpg')
      param.append('file', f)
      param.append('name', this.user)
      this.$axios({
        method: 'post',
        url: '/backend/api/upload_image',
        processData: false,
        contentType: false,
        data: param
      }).then(response => {
        let res = response.data
        if (res.error_num === 0) {
          this.$emit('show_pic')
        } else {
          console.log(res.msg)
        }
      })
    },
    beforeAvatarUpload (file) {
      const isJPG = file.type === 'image/jpeg'
      const isLt4M = file.size / 1024 / 1024 < 4

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt4M) {
        this.$message.error('上传头像图片大小不能超过 4MB!')
      }
      return isJPG && isLt4M
    }
  }
}
</script>

<style scoped>
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }

  .avatar-uploader-icon {
    font-size: 16px;
    color: #8c939d;
    width: 100px;
    height: 100px;
    line-height: 100px;
    text-align: center;
  }

  .avatar {
    width: 100px;
    height: 100px;
    display: block;
  }
</style>
