import {createStore} from 'vuex'
import { get } from "request";

const store = createStore({
    state: {
        serverResponse: {},
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
            const result = await get("/");
            const response = result.data
            console.log("ping server")
            this.commit('setServerResponse', response)
        },
        async setOutlets() {
            const result = await get("/outlets/brand/fuz")
            this.commit('setOutlets', result.data)
        },
    },
    getters: {
        serverResponse: (state) => {
            return {...state.serverResponse}
        },
        outlets: (state) => {
            return {...state.outlets}
        },
    },
})

export default store