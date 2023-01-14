<script>
import Home from "./components/Home.vue";
import { mapGetters } from "vuex";

export default {
  name: "App",
  components: { Home },
  computed: {
    ...mapGetters(["serverResponse", "outlets"]),
  },
  async mounted() {
    await this.$store.dispatch("pingServer");
    await this.$store.dispatch("setOutlets");
  },
};
</script>

<template>
  <header>
    <img
      alt="VU logo"
      class="logo"
      src="./assets/logo.png"
      width="125"
      height="125"
    />

    <div class="wrapper">
      <Home :msg="this.serverResponse" />
    </div>
  </header>
  <main>
    <div>
      {{ this.outlets }}
    </div>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
  }
}
</style>
