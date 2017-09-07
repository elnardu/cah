<template lang="html">
  <div class="form d-flex justify-content-center align-items-center">
    <form @submit.prevent="submit">
      <div class="form-group">
        <label>Имя</label>
        <input type="text" class="form-control" v-model.trim="name"/>
      </div>
      <p class="text-danger">{{error}}</p>
      <button type="submit" name="button" class="btn btn-outline-primary">Войти</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'login',
  props: ['error'],
  data() {
    return {
      name: ""
    }
  },
  methods: {
    submit() {
      if (this.name != "")
        this.$emit('login', this.name);
    }
  }
}
</script>

<style lang="css" scoped>
form {
  /*width: 33%;*/
  /*height: 33%;*/
}
.form {
  width: 100vw;
  height: 100vh;
  margin: 0;
}
</style>
