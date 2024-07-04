import axios from "axios";

export default {
    install(app) {
        app.config.globalProperties.$api = {
            async get(route) {
                try {
                    const response = await axios.get(`http://127.0.0.1:8000/${route}`);
                    return response.data;
                } catch (error) {
                    console.log("There was an error with the GET request:", error);
                }
            },
            async post(route, body) {
                try {
                    const response = await axios.post(`http://127.0.0.1:8000/${route}`, body);
                    return response.data;
                } catch (error) {
                    console.log("There was an error with the POST request:", error);
                }
            },
            async patch(route, body) {
                try {
                    const response = await axios.patch(`http://127.0.0.1:8000/${route}`, body);
                    return response.data;
                } catch (error) {
                    console.log("There was an error with the POST request:", error);
                }
            },
            async delete(route, body) {
                try {
                    const response = await axios.delete(`http://127.0.0.1:8000/${route}`, body);
                    return response.data;
                } catch (error) {
                    console.log("There was an error with the POST request:", error);
                }
            },
        };
    },
};
