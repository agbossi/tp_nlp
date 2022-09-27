import {Accordion, Col, Row} from "react-bootstrap";
import {useEffect, useState} from "react";

function WordAccordion(props) {

    const [unigrams, setUnigrams] = useState([])
    const [biGrams, setBiGrams] = useState([])

    const formatBody = (body) => {
        let unigrams = []
        let bigrams = []
        let ngrams = body.split("|")
        for (let token in ngrams) {
            console.log(ngrams[token])
            if(ngrams[token].split(" ").length === 2) {
                bigrams.push(ngrams[token])
            } else {
                unigrams.push(ngrams[token])
            }
        }
        setUnigrams(unigrams)
        setBiGrams(bigrams)
    }

    useEffect( () => {
        formatBody(props.body)
    }, [props.body])

    return (
        <>
            <Accordion>
                <Accordion.Item eventKey="0">
                    <Accordion.Header>{props.header}</Accordion.Header>
                    <Accordion.Body>
                        <Row>
                            <Col>
                                <ul>
                                    {unigrams.map((item, index) => {
                                        return <li key={index}>{item}</li>
                                    })}
                                </ul>
                            </Col>
                            <Col>
                                {biGrams.map((item, index) => {
                                    return <li key={index}>{item}</li>
                                })}
                            </Col>
                        </Row>
                    </Accordion.Body>
                </Accordion.Item>
            </Accordion>
        </>
    )
} export default WordAccordion;