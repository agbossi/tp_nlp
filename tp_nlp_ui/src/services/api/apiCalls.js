import api from "./index";
import * as paths from "./paths";

const createPlace = async (place) => api.post(paths.PLACE_URL, place);

const getPlaceById = async (id) => api.get(paths.PLACE_URL + "/" + id);

const addReviews = async (placeId) => api.put(paths.PLACE_URL + "/" + placeId);

const getPlaces = async () => api.get(paths.PLACE_URL);

const getPlaceSummary = async (placeId) => api.get(paths.SUMMARY_URL + "?" + paths.ID_QUERY + placeId);

const fetchBlacklist = async (placeId) => api.get(paths.PLACE_URL + "/" + placeId + "/blacklist");

const deleteWordFromBlacklist = async (placeId, word) => api.delete(paths.PLACE_URL + "/" + placeId + "/blacklist?" + paths.WORD_QUERY + word)

const blacklistWord = async (placeId, word) => api.put(paths.PLACE_URL + "/" + placeId + "/blacklist", word)

const updateSummary = async (placeId) => api.put(paths.SUMMARY_URL + "?" + paths.ID_QUERY + placeId);

export default {
    createPlace,
    addReviews,
    getPlaces,
    getPlaceById,
    getPlaceSummary,
    fetchBlacklist,
    deleteWordFromBlacklist,
    blacklistWord,
    updateSummary
}