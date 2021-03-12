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
      subscription: null,
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
    subscribeRoomPropsUpdate() {
      this.subscription = new EventSource(
        `./api/rooms/${this.roomName}/subscription`
      );
      this.subscription.onmessage = (event) => {
        const roomProps = JSON.parse(event.data);
        console.log(roomProps);
        store.commit("setRoomProps", roomProps);
      };
      this.subscription.onerror = () => {
        this.subscription.close();
        store.commit("setRoomProps", {});
      };
    },
    unsubscribeRoomPropsUpdate() {
      if (this.subscription) {
        this.subscription.close();
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
          this.subscribeRoomPropsUpdate();
        } else {
          this.unsubscribeRoomPropsUpdate();
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
      this.subscribeRoomPropsUpdate();
    }
  },
  destroyed() {
    this.unsubscribeRoomPropsUpdate();
  },
};
</script>

<style scoped>
a.no-color-change {
  color: white;
}
</style>