<script>
export default {
  props: {
    outlet: {
      type: Object,
    },
  },
  data() {
    return {
      outletId: "",
      name: "",
      country: "",
      address: "",
    };
  },
  mounted() {
    this.outletId = this.outlet.id_outlet;
    this.name = this.outlet.name;
    this.country = this.outlet.country;
    this.address = this.outlet.address;
  },
};
</script>

<template>
  <div class="row-wrapper">
    <div class="row-header">outlet id: {{ this.outletId }}</div>
    <div class="row-content">
      <div class="row-content-item">
        <span class="tag">name: </span>
        <span class="outlet-content">{{ this.name }}</span>
      </div>
      <div class="row-content-item">
        <span class="tag">country: </span>
        <span class="outlet-content">{{ this.country }}</span>
      </div>
      <div class="row-content-item">
        <span class="tag">address: </span>
        <span class="outlet-content">{{ this.address }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.row-wrapper {
  width: 96%;
  height: 100px;
  margin: 10px auto;
  box-shadow: 1px 1px 3px 2px rgba(0, 0, 0, 0.3);
  border-radius: 0px 0px 5px 5px;
}

.row-header {
  display: flex;
  align-items: center;
  padding-left: 5px;
  width: 100%;
  height: 25px;
  background-color: rgb(0, 101, 189);
  color: white;
  font-weight: bold;
  font-size: 13px;
}

.row-content {
  display: flex;
  padding-left: 5px;
  flex-direction: column;
}

.row-content-item {
  display: flex;
  flex-direction: row;
}

.tag {
  display: block;
  width: 100px;
  font-weight: bold;
}
</style>
