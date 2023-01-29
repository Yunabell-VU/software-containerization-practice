import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:30020/"

export const post = (url, data = {}) => {
    return new Promise((resolve, reject) => {
        axios.post(url, data, {
            headers: {
                'Content-Type':'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }).then((response) => {
            resolve(response.data)
        }, err => {
            reject(err)
        })
    })
}

export const get = (url) => {
    return new Promise((resolve, reject) => {
        axios.get(url).then((response) => {
            resolve(response.data)
        }, err => {
            reject(err)
        })
    })
}
