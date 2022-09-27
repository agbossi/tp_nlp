import { useParams } from 'react-router-dom'
import {useEffect, useState} from "react";
import apiCalls from "../../services/api/apiCalls";
import {Alert, Button, Carousel, Col, Container, Row} from "react-bootstrap";
import WordsAccordion from "./WordsAccordion";
import BlacklistSideBar from "./BlacklistSideBar";
import {IoBanSharp} from "react-icons/io5";
import UpdateButtonBlock from "./UpdateButtonBlock";

function ResultViewer() {
    const { placeId } = useParams()
    const [place, setPlace] = useState(null)
    const [message, setMessage] = useState("")
    const [error, setError] = useState(false)
    const [summary, setSummary] = useState(null)
    const [loading, setLoading] = useState(true)
    const [index, setIndex] = useState(0);
    const [wordsBlacklist, setWordsBlacklist] = useState([])
    const [barIsOpen, setBarIsOpen] = useState(false)

    const fetchPlace = (id) => {
        apiCalls.getPlaceById(id).then(response => {
            if(response.status === 200) {
                setPlace(response.data)
            }
            else {
                setError(true)
                setMessage(response.data.messageError)
            }
        }).catch(error => {
            setMessage(error.message)
        })
    }

    const getSummary = (id) => {
        apiCalls.getPlaceSummary(id).then(response => {
            if(response.status === 200) {
                setSummary(response.data)
                setMessage("")
            }
            else {
                setError(true)
                setMessage(response.data.messageError)
            }
        }).catch(error => {
            setMessage(error.message)
        })
    }

    const fetchBlacklist = (placeId) => {
        apiCalls.fetchBlacklist(placeId).then(response => {
            if(response.status === 200) {
                setWordsBlacklist(response.data)
                setMessage("")
            }
            else {
                setMessage(response.data.messageError)
            }
        }).catch(error => {
            setMessage(error.message)
        })
    }

    const addReviews = () => {
        setLoading(true)
        apiCalls.addReviews(placeId).then(response => {
            if(response.status === 204) {
                getSummary(placeId)
                setMessage("")
            }
            else {
                setMessage(response.data.messageError)
            }
        }).catch(error => {
            setMessage(error.message)
        })
    }

    const handleSelect = (selectedIndex, e) => {
        setIndex(selectedIndex);
    };

    const handleDelete = (item, index) => {
        apiCalls.deleteWordFromBlacklist(placeId, wordsBlacklist[index].word).then(response => {
            fetchBlacklist(placeId)
        })
    }

    const recompute = () => {
        setLoading(true)
        setSummary(null)
        apiCalls.updateSummary(placeId).then(response => {
            if(response.status === 204)
                getSummary(placeId)
            else {
                setMessage(response.data.messageError)
            }
        }).catch(error => {
            setMessage(error.message)
        })
    }

    const handleWordAdd = (word) => {
        apiCalls.blacklistWord(placeId, {word: word}).then(response => {
            if(response.status === 204)
                fetchBlacklist(placeId)
            else {
                setMessage(response.data.messageError)
            }
        }).catch(error => {
            setMessage(error.message)
        })
    }

    useEffect(() => {
        fetchPlace(placeId)
        getSummary(placeId)
        fetchBlacklist(placeId)
        setLoading(false)
    }, [])

    return (
        <>
            <Container fluid>
                <Row>
                    {barIsOpen && <Col xs={barIsOpen ? 2 : 0}>
                        {!loading && <BlacklistSideBar words={wordsBlacklist}
                                                       removeWord={handleDelete}
                                                       handleAdd={handleWordAdd}/>}
                    </Col>}
                    <Col xs={barIsOpen ? 10 : 12}>
                        <Container>
                            {!loading && place !== null && <h1>{place.name}</h1>}
                            <Row>
                                {summary !== null && <Alert variant="success">
                                    <Row>
                                        <Col>
                                            {"Blacklist:   "}
                                            <IoBanSharp onClick={() => {setBarIsOpen(!barIsOpen)}}/>
                                        </Col>
                                        <Col>
                                            {"Reviews analizadas: " + summary.summary.reviewsAmount}
                                        </Col>
                                        <Col>
                                            {"Oraciones analizadas: " + summary.summary.sentencesAmount}
                                        </Col>
                                    </Row>
                                </Alert>}
                                {!loading && summary !== null && <Carousel activeIndex={index} onSelect={handleSelect}>
                                    <Carousel.Item>
                                        <img
                                            className="d-block w-100"
                                            src={"/summaries/" + placeId + "/POS.png"}
                                            alt="Nube de palabras de lo bueno"
                                        />
                                        <Carousel.Caption>
                                            <h3>Lo bueno</h3>
                                        </Carousel.Caption>
                                    </Carousel.Item>
                                    <Carousel.Item>
                                        <img
                                            className="d-block w-100"
                                            src={"/summaries/" + placeId + "/NEU.png"}
                                            alt="Nube de palabras de lo neutral"
                                        />
                                        <Carousel.Caption>
                                            <h3>Lo meh</h3>
                                        </Carousel.Caption>
                                    </Carousel.Item>
                                    <Carousel.Item>
                                        <img
                                            className="d-block w-100"
                                            src={"/summaries/" + placeId + "/NEG.png"}
                                            alt="Nube de palabras de lo malo"
                                        />
                                        <Carousel.Caption>
                                            <h3>Lo malo</h3>
                                        </Carousel.Caption>
                                    </Carousel.Item>
                                </Carousel>}
                                {summary !== null && <WordsAccordion summary={summary.summary}/>}
                                {(loading || summary === null) && <Alert variant="primary">
                                    <Alert.Heading>Cargando...</Alert.Heading>
                                </Alert>}
                            </Row>
                        </Container>
                    </Col>
                </Row>
            </Container>
            <br/>
            <br/>
            <br/>
            <Row>
                {!loading && summary !== null && <UpdateButtonBlock update={addReviews} recompute={recompute} />}
            </Row>
            <br/>
            {message && (
                <div className="form-group">
                    <div className="alert alert-danger m-3" role="alert">
                        {message}
                    </div>
                </div>
            )}
        </>
    )
}

export default ResultViewer;