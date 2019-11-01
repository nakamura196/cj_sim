<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand>CJ: Similar Image Search</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
      </b-collapse>
    </b-navbar>

    <b-container fluid>

      <b-row class="my-5">
        <b-col :cols="6" :sm="1" v-for="(obj, index) in list" :key="index" class="my-2">
          <router-link v-bind:to="{ name: 'home', query: { u: 'https://raw.githubusercontent.com/nakamura196/cj_sim/master/docs/data/'+obj.id+'.json'}}">
            <b-img-lazy rounded fluid :src="'https://cultural-jp.s3.amazonaws.com/'+obj.id+'.jpg'" :alt="obj.id"></b-img-lazy>
          </router-link>
        </b-col>
      </b-row>

      <back-to-top text="Back to top"></back-to-top>
    </b-container>

  </div>
</template>

<script>
import axios from "axios";
import BackToTop from "vue-backtotop";

export default {
  name: "HelloWorld",
  components: {
    BackToTop
  },
  data() {
    return {
      list: []
    };
  },
  created() {
    this.init()
  },
  methods: {
    init(){
      this.list = []
      let u = this.$route.query.u;
      if(!u){
        u = "https://raw.githubusercontent.com/nakamura196/cj_sim/master/docs/data/europeana-07931_diglit_creutzer1931_03_26.json"
      }
      axios
        .get(u)
        .then(response => {
          this.list = response.data
        })
        .catch(err => {
        });
    }
  },
  watch: {
    $route: function() {
      this.init();
    }
  }
};
</script>
