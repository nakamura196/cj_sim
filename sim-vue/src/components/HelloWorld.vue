<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand>CJ: Similar Image Search</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav></b-collapse>
    </b-navbar>

    <b-container fluid>
      <b-row class="my-5">
        <b-col :cols="6" :sm="2" v-for="(obj, index) in list" :key="index" class="my-2">
          <a
            :href="'https://nakamura196.github.io/cj2/#/item?id='+obj.id"
          >
            <b-img-lazy
              rounded
              fluid
              :src="'https://cultural-jp.s3.amazonaws.com/'+obj.id+'.jpg'"
              :alt="obj.id"
            ></b-img-lazy>
          </a>
        </b-col>
      </b-row>

      <infinite-loading class="mb-5" @infinite="infiniteHandler" :distance="1"></infinite-loading>

      <back-to-top text="Back to top"></back-to-top>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
import InfiniteLoading from "vue-infinite-loading";
import BackToTop from "vue-backtotop";

export default {
  name: "HelloWorld",
  components: {
    BackToTop,
    InfiniteLoading
  },
  data() {
    return {
      list_all: [],
      list: [],
      page: 0
    };
  },
  created() {
    this.init();
  },
  methods: {
    // setIntervalを使う方法
    sleep(waitSec, callbackFunc) {
      // 経過時間（秒）
      var spanedSec = 0;

      // 1秒間隔で無名関数を実行
      var id = setInterval(function() {
        spanedSec++;

        // 経過時間 >= 待機時間の場合、待機終了。
        if (spanedSec >= waitSec) {
          // タイマー停止
          clearInterval(id);

          // 完了時、コールバック関数を実行
          if (callbackFunc) callbackFunc();
        }
      }, 1000);
    },

    infiniteHandler($state) {

      let list_all = this.list_all;

      if (list_all.length == 0) {
        $state.reset();
        return;
      }

      this.search()
      
      //ポイント
      this.sleep(2, function() {
        $state.loaded();
      });
    },
    search(){
      this.page += 1;
      console.log(this.page)

      let page = this.page;

      let d = 60;

      let start = (page - 1) * d;
      let end = page * d;

      let list_all = this.list_all;

      if (page > 1 && end > list_all.length) {
        end = list_all.length;
        $state.complete();
      }
      for (let i = start; i < end; i++) {
        this.list.push(list_all[i]);
      }
    },
    init() {

      this.page = 0;
      this.list_all = [];
      this.list = [];
      
      let u = this.$route.query.u;
      if (!u) {
        u =
          "https://raw.githubusercontent.com/nakamura196/cj_sim/master/docs/data/europeana-07931_diglit_creutzer1931_03_26.json";
      }
      axios
        .get(u)
        .then(response => {

          let list = response.data;
          let end = 1000;
          if (end > list.length) {
            end = list.length;
          }
          for (let i = 0; i < end; i++) {
            this.list_all.push(list[i]);
          }

          this.search()
        })
        .catch(err => {});
    }
  },
  watch: {
    $route: function() {
      this.init();
    }
  }
};
</script>
