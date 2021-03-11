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
          <b-nav-item v-if="this.$store.getters.joined">
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
</script>

<style scoped>
a.no-color-change {
  color: white;
}
</style>