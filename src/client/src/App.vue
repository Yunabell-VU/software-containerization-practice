<script>
import Home from "./components/Home.vue";
import { get } from "./utils/request";

export default {
  name: "App",
  components: { Home },
  async mounted() {
    async function ping() {
      const result = await get("/");
      const response = result.data;
      console.log("ping server");
    }
    ping();
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
      <Home msg="Front Connected!!" />
    </div>
  </header>
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
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
