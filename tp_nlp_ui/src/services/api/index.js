import axios from 'axios';
import { create } from 'apisauce';
import applyCaseMiddleware from 'axios-case-converter';
import {BASE_URL} from "./paths";

const options = {}

const api = applyCaseMiddleware(axios.create({
    baseURL: BASE_URL
}), options);

export default create({ axiosInstance: api });