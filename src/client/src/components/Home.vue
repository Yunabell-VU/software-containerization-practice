<script>
import { mapGetters } from "vuex";

export default {
  data() {},
  computed: {
    ...mapGetters(["serverResponse", "outlets"]),
  },
};
</script>

<template>
  <div class="home-wrapper">
    <div class="home-header">
      <div class="greetings">
        <h1>{{ this.serverResponse }}</h1>
      </div>
    </div>
    <div class="home-content"></div>

    <div>
      {{ this.outlets }}
    </div>
  </div>
</template>

<style scoped>
.home-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.home-header {
  height: 100px;
  background-color: rgb(0, 101, 189);
  padding: 5px;
}

.home-header__logo {
  background-color: white;
  width: 90px;
  height: 90px;
}

h1 {
  font-weight: 500;
  font-size: 2.6rem;
}

h3 {
  font-size: 1.2rem;
}

.greetings {
  color: white;
  text-align: center;
}
.greetings h1,
.greetings h3 {
  text-align: center;
}

/* @media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
} */
</style>
