<script>
import Content from "./Content.vue";
import Modal from "./Modal.vue";
import { mapGetters } from "vuex";
import { post } from "../utils/request";

export default {
  components: { Content, Modal },
  data() {
    return {
      isEdit: false,
      isModalVisible: false,
      newModel: {},
    };
  },
  computed: {
    ...mapGetters(["serverResponse", "outlets"]),
  },
  methods: {
    showModal() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isEdit = false;
      this.isModalVisible = false;
    },
    async handleSave() {
      this.newModel.source = "ubereats";
      this.newModel.reviews_nr = 5;
      const payload = JSON.stringify(this.newModel);
      await post(`/insert/outlet/`, payload);
      this.newModel = {};
      this.isModalVisible = false;

      await this.$store.dispatch("setOutlets");
    },
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
    <div class="home-add">
      <div class="add-button" @click="showModal">ADD outlet</div>
    </div>
    <div>
      <Content :outlets="this.outlets" />
    </div>
    <Modal v-show="isModalVisible" @close="closeModal">
      <template #body>
        <div class="modal-body">
          <ul>
            <li class="modal-input">
              <span></span>
              <span> Outlet id:</span>
              <input
                v-model="newModel.id_outlet"
                type="text"
                autocomplete="off"
              />
            </li>
            <li class="modal-input">
              <span></span>
              <span> Outlet name:</span>
              <input v-model="newModel.name" type="text" autocomplete="off" />
            </li>
            <li class="modal-input">
              <span></span>
              <span> Outlet country:</span>
              <input
                v-model="newModel.country"
                type="text"
                autocomplete="off"
              />
            </li>
            <li class="modal-input">
              <span></span>
              <span> Outlet address:</span>
              <input
                v-model="newModel.address"
                type="text"
                autocomplete="off"
              />
            </li>
          </ul>
        </div>
      </template>
      <template #footer>
        <div class="modal-footer">
          <div class="modal-footer__buttons">
            <button @click="closeModal" class="modal-button">cancel</button>
            <button @click="handleSave" class="modal-button">save</button>
          </div>
        </div>
      </template>
    </Modal>
  </div>
</template>

<style scoped>
.home-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.home-header {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100px;
  background-color: rgb(0, 101, 189);
}

.home-header__logo {
  background-color: white;
  width: 90px;
  height: 90px;
}

.home-add {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px 0px;
}

.add-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 200px;
  height: 50px;
  background-color: rgb(247, 159, 7);
  color: black;
  font-size: 20px;
  font-weight: bold;
}

.add-button:hover {
  cursor: pointer;
  color: white;
  background-color: rgb(221, 142, 6);
}

h1 {
  font-weight: 500;
  font-size: 2.6rem;
}

h3 {
  font-size: 1.2rem;
}

.greetings {
  display: flex;
  color: white;
  align-items: center;
  justify-content: center;
}
.greetings h1,
.greetings h3 {
  text-align: center;
}

ul,
li {
  padding: 0;
  margin: 0;
  list-style: none;
}

.modal-input {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.modal-input > span {
  margin-right: 10px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
}

.modal-footer__buttons > button {
  width: 60px;
  height: 30px;
  margin-left: 10px;
  background-color: rgb(247, 159, 7);
  color: black;
  border: none;
  font-weight: bold;
}

.modal-footer__buttons > button:hover {
  cursor: pointer;
  color: white;
  background-color: rgb(221, 142, 6);
}
</style>
