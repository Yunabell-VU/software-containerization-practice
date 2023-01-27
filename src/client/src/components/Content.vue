<script>
import Row from "./Row.vue";

export default {
  components: { Row },
  props: {
    outlets: {
      type: [],
    },
  },
  data() {},
};
</script>

<template>
  <div class="reverse">
    <div v-for="(outlet, index) in outlets" :key="index">
      <Row :outlet="outlet" />
    </div>
  </div>
</template>

<style scoped>
.reverse {
  display: flex;
  flex-direction: column-reverse;
}
</style>
