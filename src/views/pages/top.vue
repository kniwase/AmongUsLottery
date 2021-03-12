<template>
  <div>
    <b-navbar toggleable="xs" type="dark" variant="info">
      <b-navbar-brand>特殊役抽選ツール</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item>
            <router-link class="no-color-change" tag="a" to="/"
              >抽選</router-link
            >
          </b-nav-item>
          <b-nav-item v-if="this.joined">
            <router-link class="no-color-change" tag="a" to="/admin"
              >設定</router-link
            >
          </b-nav-item>
          <b-nav-item>
            <router-link class="no-color-change" tag="a" to="/faq"
              >FAQ</router-link
            >
          </b-nav-item>
          <b-nav-item>
            <router-link class="no-color-change" tag="a" to="/agreements"
              >ご利用について</router-link
            >
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <router-view></router-view>
  </div>
</template>

<script>
module.exports = {
  data: () => {
    return {
      fetchRoomPropsTimerId: null,
    };
  },
  computed: {
    ...Vuex.mapGetters([
      "roomName",
      "members",
      "joined",
      "lotTimestamp",
      "isAdmin",
      "myRole",
    ]),
  },
  methods: {
    fetchRoomProps() {
      axios
        .get(`./api/rooms/${this.roomName}`)
        .then((response) => {
          store.commit("setRoomProps", response.data);
        })
        .catch(() => {
          this.clearFetchRoomPropsTimer();
          store.commit("setRoomProps", {});
        });
    },
    setFetchRoomPropsTimer() {
      this.fetchRoomPropsTimerId = setInterval(this.fetchRoomProps, 2000);
    },
    clearFetchRoomPropsTimer() {
      if (this.fetchRoomPropsTimerId !== null) {
        clearInterval(this.fetchRoomPropsTimerId);
      }
    },
    makeToast(message, variant = null) {
      this.$bvToast.toast(message, {
        title: "通知",
        autoHideDelay: 5000,
        variant: variant,
        solid: true,
      });
    },
  },
  watch: {
    joined(joined, joinedPrev) {
      if (joined !== joinedPrev) {
        if (joined) {
          this.setFetchRoomPropsTimer();
        } else {
          this.clearFetchRoomPropsTimer();
          if (this.$route.path === "/admin") {
            router.push("/");
          }
        }
      }
    },
    isAdmin(isAdmin, isAdminPrev) {
      if (isAdmin !== isAdminPrev && this.joined) {
        if (isAdmin) {
          this.makeToast("管理者になりました", "secondary");
        } else {
          this.makeToast("管理者権限を奪われました", "secondary");
        }
      }
    },
    lotTimestamp(lotTimestamp, lotTimestampPrev) {
      if (lotTimestamp !== lotTimestampPrev && this.joined) {
        if (lotTimestamp) {
          let variant = "info";
          if (this.myRole !== "通常役") {
            variant = "danger";
          }
          this.makeToast(`あなたは ${this.myRole} に選ばれました`, variant);
        } else {
          this.makeToast("抽選結果がリセットされました", "warning");
        }
      }
    },
  },
  mounted() {
    if (this.joined) {
      this.fetchRoomProps();
      this.setFetchRoomPropsTimer();
    }
  },
  destroyed() {
    this.clearFetchRoomPropsTimer();
  },
};
</script>

<style scoped>
a.no-color-change {
  color: white;
}
</style>