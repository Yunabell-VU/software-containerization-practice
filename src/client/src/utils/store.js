import {createStore} from 'vuex'
import { get } from "./request";

const store = createStore({
    state: {
        serverResponse: "server: not connected",
        outlets: {},
    },
    mutations: {
        setServerResponse(state, response) {
            state.serverResponse = response;
        },
        setOutlets(state, outlets) {
            state.outlets = outlets
        },
    },
    actions: {
        async pingServer() {
            // const result = await get("/")
            const response = "Restaurants"
            this.commit('setServerResponse', response)
        },
        async setOutlets() {
            const result = await get("/outlets/source/ubereats")
            this.commit('setOutlets', result)
        },
    },
    getters: {
        serverResponse: (state) => {
            return state.serverResponse
        },
        outlets: (state) => {
            return {...state.outlets}
        },
    },
})

export default store