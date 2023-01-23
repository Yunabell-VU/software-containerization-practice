<script>
import Home from "./components/Home.vue";

export default {
  name: "App",
  components: { Home },
  async mounted() {
    await this.$store.dispatch("pingServer");
    await this.$store.dispatch("setOutlets");
  },
};
</script>

<template>
  <div class="wrapper">
    <Home />
  </div>
</template>

<style scoped></style>
