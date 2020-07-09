export default {
  state: {
    name: '',
    is_login: false,
    formLabelWidth: '120px',
    booklist: [],
    booklists: [],
    imageURL: '',
    Data: [],
    msg: []
  },
  mutations: {
    store_msg (state, info) {
      state.msg = info
    },
    store_Data (state, info) {
      state.Data = info
    },
    store_booklist (state, info) {
      state.booklist = info
    },
    store_booklists (state, info) {
      state.booklists = info
    },
    store_name (state, info) {
      state.name = info
    },
    store_login (state, info) {
      state.is_login = info
    },
    store_image (state, pic) {
      state.imageURL = pic
    }
  }
}
