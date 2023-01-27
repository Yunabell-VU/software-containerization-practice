import axios from "axios";

export const post = (url, data = {}) => {
    return new Promise((resolve, reject) => {
        axios.post(url, data, {
            baseURL:"http://127.0.0.1:30020/",
            headers: {
                'Content-Type':'application/json'
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
        axios.get(url, {
            baseURL:"http://127.0.0.1:30020/",
        }).then((response) => {
            resolve(response.data)
        }, err => {
            reject(err)
        })
    })
}
