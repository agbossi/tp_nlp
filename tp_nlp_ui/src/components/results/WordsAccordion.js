import {Accordion} from "react-bootstrap";
import WordAccordion from "./WordAccordion";
import LemAccordion from "./LemAccordion";

function WordsAccordion(props) {

    return (
        <>
            <Accordion>
                <Accordion.Item eventKey="0">
                    <Accordion.Header>Lo bueno</Accordion.Header>
                    <Accordion.Body>
                        <LemAccordion header={"Lematizacion"} body={props.summary.good}/>
                        <WordAccordion header={"Tokens destacados"} body={props.summary.goodTokens}/>
                    </Accordion.Body>
                </Accordion.Item>
                <Accordion.Item eventKey="1">
                    <Accordion.Header>lo malo</Accordion.Header>
                    <Accordion.Body>
                        <WordAccordion header={"Lematizacion"} body={props.summary.bad}/>
                        <WordAccordion header={"Tokens destacados"} body={props.summary.badTokens}/>
                    </Accordion.Body>
                </Accordion.Item>
                <Accordion.Item eventKey="2">
                    <Accordion.Header>lo neutral</Accordion.Header>
                    <Accordion.Body>
                        <WordAccordion header={"Lematizacion"} body={props.summary.neutral}/>
                        <WordAccordion header={"Tokens destacados"} body={props.summary.neutralTokens}/>
                    </Accordion.Body>
                </Accordion.Item>
            </Accordion>
        </>
    )
} export default WordsAccordion;