<script>
export default {
  name: "Modal",
};
</script>

<template>
  <transition name="my-modal-fade">
    <div class="my-modal-backdrop" @click="$emit('close')">
      <div class="my-modal" @click.stop>
        <header class="my-modal-header" id="modalTitle">
          <div>Add a new outlet</div>
        </header>

        <section class="my-modal-body" id="modalDescription">
          <slot name="body"></slot>
        </section>

        <footer class="my-modal-footer">
          <slot name="footer"></slot>
        </footer>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.my-modal-backdrop {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}
.my-modal {
  /* width: 500px; */
  background: white;
  box-shadow: 2px 2px 20px 1px;
  overflow-x: auto;
  display: flex;
  flex-direction: column;
}
.my-modal-header,
.my-modal-footer {
  padding: 15px;
  display: flex;
}
.my-modal-header {
  position: relative;
  background-color: rgb(247, 159, 7);
  color: black;
  font-size: 30px;
  font-weight: bolder;
  justify-content: center;
}
.my-modal-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.3);
  flex-direction: column;
}
.my-modal-body {
  position: relative;
  padding: 20px 10px;
}
.my-modal-fade-enter,
.my-modal-fade-leave-to {
  opacity: 0;
}
.my-modal-fade-enter-active,
.my-modal-fade-leave-active {
  transition: opacity 0.5s ease;
}
</style>
