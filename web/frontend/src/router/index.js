import VueRouter from 'vue-router'
import book from '@/components/book'
import UploadImage from '@/components/UploadImage'
import menu from '@/components/menu'
import find from '@/components/find'
import community from '@/components/community'
import UploadText from '@/components/UploadText'

export default new VueRouter({
  routes: [
    {
      path: '/',
      components: {
        'book': book,
        'UploadImage': UploadImage,
        'menu': menu,
        'find': find,
        'community': community,
        'UploadText': UploadText
      }
    }
  ]
})
