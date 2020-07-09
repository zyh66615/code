<template>
  <div style="position: fixed;width: 200px; margin-top: 100px">
    <el-row>
      <el-col>
        <el-menu
          class="el-menu-vertical-demo"
          background-color="#88C6E5"
          text-color="#fff"
          active-text-color="#000"
          default-active="1"
        >
          <el-menu-item
            @click="first" index="1">
            <template slot="title">
              <i class="el-icon-menu"></i>
              <span>找书</span>
            </template>
          </el-menu-item>
          <el-menu-item @click="Find" index="2">
            <template slot="title">
              <i class="el-icon-menu"></i>
              <span>书库</span>
            </template>
          </el-menu-item>
          <el-menu-item @click="Community" index="3">
            <i class="el-icon-menu"></i>
            <span slot="title">社区</span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>

  </div>
</template>

<script>
export default {
  name: 'menu',
  data () {
  },
  methods: {
    first () {
      this.$emit('first')
    },
    Find () {
      this.$emit('Back1', true)
    },
    Community () {
      this.$emit('Back2', true)
    }
  }
}
</script>

<style scoped>
  span {
    font-size: 24px
  }

  template {
    font-size: 24px
  }

</style>
